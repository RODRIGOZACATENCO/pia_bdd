DROP DATABASE IF EXISTS BAR;
CREATE DATABASE BAR;
USE BAR;

CREATE TABLE CLIENTE(
	cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100),
    fecha_nacimiento DATE
);
CREATE TABLE MESA(
	mesa_id INT AUTO_INCREMENT PRIMARY KEY,
    capacidad INT CHECK(capacidad > 0),
    ubicacion VARCHAR(50)
);

CREATE TABLE PROVEEDOR(
	proveedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100)
);

CREATE TABLE TURNO(
	turno_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_turno VARCHAR(100) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    cantidad_empleados INT CHECK(cantidad_empleados >= 0)
);

CREATE TABLE MARCA(
	marca_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE TIPO_PRODUCTO(
	tipo_producto_id INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50)
);


CREATE TABLE PRODUCTO(
	producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    marca_id INT,
    tipo_producto_id INT,
    precio DECIMAL(10,2) CHECK(precio > 0),
    stock INT CHECK(stock >= 0),
    FOREIGN KEY (tipo_producto_id) REFERENCES TIPO_PRODUCTO(tipo_producto_id),
    FOREIGN KEY (marca_id) REFERENCES MARCA(marca_id)
);

CREATE TABLE PUESTO(
	puesto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE EMPLEADO(
	empleado_id INT AUTO_INCREMENT PRIMARY KEY,
    turno_id INT,
    puesto_id INT,
    nombre VARCHAR(100),
    salario DECIMAL(10,2) CHECK(salario > 0),
    FOREIGN KEY (turno_id) REFERENCES TURNO(turno_id),
    FOREIGN KEY(puesto_id) REFERENCES PUESTO(puesto_id)
);
CREATE TABLE USUARIO_SISTEMA(
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    password_salt VARCHAR(64) NOT NULL,
    FOREIGN KEY (empleado_id) REFERENCES EMPLEADO(empleado_id) ON DELETE CASCADE
);
CREATE TABLE USUARIO(
	usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    puesto_id INT,
    tipo_usuario VARCHAR(50),
    FOREIGN KEY (puesto_id) REFERENCES PUESTO(puesto_id)
);

CREATE TABLE ORDEN_COMPRA(
	orden_compra_id INT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id INT,
    fecha_suministro DATE,
    total_pago DECIMAL(10,2) CHECK(total_pago >= 0),
    FOREIGN KEY (proveedor_id) REFERENCES PROVEEDOR(proveedor_id)
);

CREATE TABLE DETALLE_ORDEN_COMPRA(
	detalle_orden_compra_id INT AUTO_INCREMENT PRIMARY KEY,
    orden_compra_id INT,
    producto_id INT,
    precio_compra DECIMAL(10,2) CHECK(precio_compra > 0),
    cantidad_comprada INT CHECK(cantidad_comprada > 0),
    FOREIGN KEY (orden_compra_id) REFERENCES ORDEN_COMPRA(orden_compra_id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTO(producto_id)
);

CREATE TABLE PROMOCION(
	promocion_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

CREATE TABLE DETALLE_PROMOCION(
	detalle_promocion_id INT AUTO_INCREMENT PRIMARY KEY,
    promocion_id INT,
    producto_id INT,
	precio_oferta DECIMAL(10,2) CHECK(precio_oferta > 0),
    FOREIGN KEY (promocion_id) REFERENCES PROMOCION(promocion_id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTO(producto_id)
);

CREATE TABLE VENTA(
	venta_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    empleado_id INT,
    mesa_id INT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_venta DECIMAL(10,2) CHECK(total_venta >= 0),
    FOREIGN KEY (cliente_id) REFERENCES CLIENTE(cliente_id),
    FOREIGN KEY (empleado_id) REFERENCES EMPLEADO(empleado_id),
    FOREIGN KEY (mesa_id) REFERENCES MESA(mesa_id)
);

CREATE TABLE ORDEN(
	orden_id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,      
    producto_id INT NOT NULL,   
	promocion_id INT,  
    cantidad INT CHECK(cantidad > 0),
    precio_al_vender DECIMAL(10,2) CHECK(precio_al_vender > 0),    
    FOREIGN KEY (venta_id) REFERENCES VENTA(venta_id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTO(producto_id),
	FOREIGN KEY (promocion_id) REFERENCES PROMOCION(promocion_id)
);

CREATE TABLE LOG_CAMBIOS (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada VARCHAR(100) NOT NULL,
    operacion VARCHAR(10) NOT NULL, -- 'INSERT', 'UPDATE' o 'DELETE'
    registro_id INT,
    usuario_actual VARCHAR(100),
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT
);

-- -----------------------------------------------------
-- Muestra el producto con el nombre de su marca y tipo.
-- -----------------------------------------------------
USE BAR;
DROP VIEW IF EXISTS VISTA_CATALOGO_PRODUCTOS;
CREATE VIEW VISTA_CATALOGO_PRODUCTOS AS
SELECT
    p.producto_id,
    p.nombre AS nombre_producto,
    m.nombre AS nombre_marca,
    tp.nombre AS tipo_producto,
    p.precio,
    p.stock
FROM PRODUCTO p
LEFT JOIN MARCA m ON p.marca_id = m.marca_id
LEFT JOIN TIPO_PRODUCTO tp ON p.tipo_producto_id = tp.tipo_producto_id;

-- -----------------------------------------------------
-- Muestra los empleados con su puesto y turno.
-- -----------------------------------------------------
DROP VIEW IF EXISTS VISTA_PERSONAL;
CREATE VIEW VISTA_PERSONAL AS
SELECT
    e.empleado_id,
    e.nombre AS nombre_empleado,
    p.nombre AS puesto,
    e.salario,
    t.nombre_turno,
    t.hora_inicio,
    t.hora_fin
FROM EMPLEADO e
LEFT JOIN PUESTO p ON e.puesto_id = p.puesto_id
LEFT JOIN TURNO t ON e.turno_id = t.turno_id;


-- -----------------------------------------------------
-- Muestra el rendimiento de cada empleado.
-- -----------------------------------------------------
DROP VIEW IF EXISTS VISTA_RESUMEN_VENTAS_EMPLEADO;
CREATE VIEW VISTA_RESUMEN_VENTAS_EMPLEADO AS
SELECT
    e.empleado_id,
    e.nombre AS nombre_empleado,
    p.nombre AS puesto,
    COUNT(DISTINCT v.venta_id) AS numero_ventas_atendidas,
    SUM(v.total_venta) AS total_generado
FROM VENTA v
JOIN EMPLEADO e ON v.empleado_id = e.empleado_id
LEFT JOIN PUESTO p ON e.puesto_id = p.puesto_id
GROUP BY e.empleado_id, e.nombre, p.nombre
ORDER BY total_generado DESC;

-- -----------------------------------------------------
-- Muestra una lista limpia de clientes.
-- -----------------------------------------------------
DROP VIEW IF EXISTS VISTA_CLIENTES;
CREATE VIEW VISTA_CLIENTES AS
SELECT
    cliente_id,
    nombre,
    telefono,
    correo,
    fecha_nacimiento
FROM CLIENTE;

USE BAR;
DELIMITER //

-- -----------------------------------------------------
-- Triggers para la tabla PRODUCTO
-- -----------------------------------------------------

CREATE TRIGGER trg_producto_insert
AFTER INSERT ON PRODUCTO
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PRODUCTO', 'INSERT', NEW.producto_id, CURRENT_USER(),
            CONCAT('Nuevo producto: ', NEW.nombre, ', Precio: ', NEW.precio, ', Stock: ', NEW.stock));
END;
//

CREATE TRIGGER trg_producto_update
AFTER UPDATE ON PRODUCTO
FOR EACH ROW
BEGIN
    DECLARE desc_cambio TEXT;
    SET desc_cambio = CONCAT('Producto ID: ', OLD.producto_id, ' actualizado. ');
    
    IF OLD.nombre <> NEW.nombre THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Nombre: ', OLD.nombre, ' -> ', NEW.nombre, '. ');
    END IF;
    IF OLD.precio <> NEW.precio THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Precio: ', OLD.precio, ' -> ', NEW.precio, '. ');
    END IF;
    IF OLD.stock <> NEW.stock THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Stock: ', OLD.stock, ' -> ', NEW.stock, '. ');
    END IF;

    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PRODUCTO', 'UPDATE', OLD.producto_id, CURRENT_USER(), desc_cambio);
END;
//

CREATE TRIGGER trg_producto_delete
AFTER DELETE ON PRODUCTO
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PRODUCTO', 'DELETE', OLD.producto_id, CURRENT_USER(),
            CONCAT('Producto eliminado: ', OLD.nombre, ', Precio: ', OLD.precio));
END;
//

-- -----------------------------------------------------
-- Triggers para la tabla EMPLEADO
-- -----------------------------------------------------

CREATE TRIGGER trg_empleado_insert
AFTER INSERT ON EMPLEADO
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('EMPLEADO', 'INSERT', NEW.empleado_id, CURRENT_USER(),
            CONCAT('Nuevo empleado: ', NEW.nombre, ', Puesto ID: ', NEW.puesto_id, ', Salario: ', NEW.salario));
END;
//

CREATE TRIGGER trg_empleado_update
AFTER UPDATE ON EMPLEADO
FOR EACH ROW
BEGIN
    DECLARE desc_cambio TEXT;
    SET desc_cambio = CONCAT('Empleado ID: ', OLD.empleado_id, ' actualizado. ');

    IF OLD.puesto_id <> NEW.puesto_id THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Puesto ID: ', OLD.puesto_id, ' -> ', NEW.puesto_id, '. ');
    END IF;
    IF OLD.salario <> NEW.salario THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Salario: ', OLD.salario, ' -> ', NEW.salario, '. ');
    END IF;
    IF OLD.nombre <> NEW.nombre THEN
        SET desc_cambio = CONCAT(desc_cambio, 'Nombre: ', OLD.nombre, ' -> ', NEW.nombre, '. ');
    END IF;

    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('EMPLEADO', 'UPDATE', OLD.empleado_id, CURRENT_USER(), desc_cambio);
END;
//

CREATE TRIGGER trg_empleado_delete
AFTER DELETE ON EMPLEADO
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('EMPLEADO', 'DELETE', OLD.empleado_id, CURRENT_USER(),
            CONCAT('Empleado despedido: ', OLD.nombre, ', Puesto ID: ', OLD.puesto_id));
END;
//

-- -----------------------------------------------------
-- Triggers para la tabla CLIENTE
-- -----------------------------------------------------

CREATE TRIGGER trg_cliente_insert
AFTER INSERT ON CLIENTE
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('CLIENTE', 'INSERT', NEW.cliente_id, CURRENT_USER(),
            CONCAT('Nuevo cliente: ', NEW.nombre, ', Correo: ', IFNULL(NEW.correo, 'N/A')));
END;
//

CREATE TRIGGER trg_cliente_update
AFTER UPDATE ON CLIENTE
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('CLIENTE', 'UPDATE', OLD.cliente_id, CURRENT_USER(),
            CONCAT('Datos antiguos: ', OLD.nombre, ', ', IFNULL(OLD.correo, 'N/A'), '. Datos nuevos: ', NEW.nombre, ', ', IFNULL(NEW.correo, 'N/A')));
END;
//

CREATE TRIGGER trg_cliente_delete
AFTER DELETE ON CLIENTE
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('CLIENTE', 'DELETE', OLD.cliente_id, CURRENT_USER(),
            CONCAT('Cliente eliminado: ', OLD.nombre));
END;
//

-- -----------------------------------------------------
-- Triggers para la tabla VENTA
-- -----------------------------------------------------

CREATE TRIGGER trg_venta_insert
AFTER INSERT ON VENTA
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('VENTA', 'INSERT', NEW.venta_id, CURRENT_USER(),
            CONCAT('Nueva venta: ', NEW.venta_id, ', Cliente ID: ', NEW.cliente_id, ', Total: ', NEW.total_venta));
END;
//

CREATE TRIGGER trg_venta_update
AFTER UPDATE ON VENTA
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('VENTA', 'UPDATE', OLD.venta_id, CURRENT_USER(),
            CONCAT('Venta modificada. Total anterior: ', OLD.total_venta, ', Total nuevo: ', NEW.total_venta));
END;
//

CREATE TRIGGER trg_venta_delete
AFTER DELETE ON VENTA
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('VENTA', 'DELETE', OLD.venta_id, CURRENT_USER(),
            CONCAT('VENTA ELIMINADA. ID: ', OLD.venta_id, ', Cliente ID: ', OLD.cliente_id, ', Total: ', OLD.total_venta));
END;
//

-- -----------------------------------------------------
-- Triggers para la tabla ORDEN
-- -----------------------------------------------------

CREATE TRIGGER trg_orden_insert
AFTER INSERT ON ORDEN
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('ORDEN', 'INSERT', NEW.orden_id, CURRENT_USER(),
            CONCAT('Nueva orden (detalle) para Venta ID: ', NEW.venta_id, ', Producto ID: ', NEW.producto_id, ', Cant: ', NEW.cantidad));
END;
//

CREATE TRIGGER trg_orden_update
AFTER UPDATE ON ORDEN
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('ORDEN', 'UPDATE', OLD.orden_id, CURRENT_USER(),
            CONCAT('Orden (detalle) modificada. Venta ID: ', OLD.venta_id, '. Cantidad: ', OLD.cantidad, ' -> ', NEW.cantidad));
END;
//

CREATE TRIGGER trg_orden_delete
AFTER DELETE ON ORDEN
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('ORDEN', 'DELETE', OLD.orden_id, CURRENT_USER(),
            CONCAT('Orden (detalle) ELIMINADA. Venta ID: ', OLD.venta_id, ', Producto ID: ', OLD.producto_id, ', Cant: ', OLD.cantidad));
END;
//

-- -----------------------------------------------------
-- Triggers para la tabla PROVEEDOR
-- -----------------------------------------------------

CREATE TRIGGER trg_proveedor_insert
AFTER INSERT ON PROVEEDOR
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PROVEEDOR', 'INSERT', NEW.proveedor_id, CURRENT_USER(),
            CONCAT('Nuevo proveedor: ', NEW.nombre, ', Telefono: ', IFNULL(NEW.telefono, 'N/A')));
END;
//

CREATE TRIGGER trg_proveedor_update
AFTER UPDATE ON PROVEEDOR
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PROVEEDOR', 'UPDATE', OLD.proveedor_id, CURRENT_USER(),
            CONCAT('Proveedor actualizado: ', OLD.nombre, ' -> ', NEW.nombre));
END;
//

CREATE TRIGGER trg_proveedor_delete
AFTER DELETE ON PROVEEDOR
FOR EACH ROW
BEGIN
    INSERT INTO LOG_CAMBIOS (tabla_afectada, operacion, registro_id, usuario_actual, descripcion)
    VALUES ('PROVEEDOR', 'DELETE', OLD.proveedor_id, CURRENT_USER(),
            CONCAT('Proveedor eliminado: ', OLD.nombre));
END;
//

DELIMITER ;

USE BAR;

DROP PROCEDURE IF EXISTS sp_get_catalogo_productos;
DELIMITER //
CREATE PROCEDURE sp_get_catalogo_productos()
BEGIN
    SELECT
        p.nombre AS nombre_producto,
        m.nombre AS nombre_marca,
        tp.nombre AS tipo_producto,
        p.precio,
        p.stock
    FROM PRODUCTO p
    LEFT JOIN MARCA m ON p.marca_id = m.marca_id
    LEFT JOIN TIPO_PRODUCTO tp ON p.tipo_producto_id = tp.tipo_producto_id
    ORDER BY nombre_producto;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_personal;
DELIMITER //
CREATE PROCEDURE sp_get_personal()
BEGIN
    SELECT
        e.empleado_id,
        e.nombre AS nombre_empleado,
        p.nombre AS puesto,
        e.salario,
        t.nombre_turno,
        t.hora_inicio,
        t.hora_fin
    FROM EMPLEADO e
    LEFT JOIN PUESTO p ON e.puesto_id = p.puesto_id
    LEFT JOIN TURNO t ON e.turno_id = t.turno_id
    ORDER BY nombre_empleado;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_resumen_ventas_empleado;
DELIMITER //
CREATE PROCEDURE sp_get_resumen_ventas_empleado()
BEGIN
    SELECT
        e.empleado_id,
        e.nombre AS nombre_empleado,
        p.nombre AS puesto,
        COUNT(DISTINCT v.venta_id) AS numero_ventas_atendidas,
        SUM(v.total_venta) AS total_generado
    FROM VENTA v
    JOIN EMPLEADO e ON v.empleado_id = e.empleado_id
    LEFT JOIN PUESTO p ON e.puesto_id = p.puesto_id
    GROUP BY e.empleado_id, e.nombre, p.nombre
    ORDER BY total_generado DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_clientes;
DELIMITER //
CREATE PROCEDURE sp_get_clientes()
BEGIN
    SELECT
        cliente_id,
        nombre,
        telefono,
        correo
    FROM VISTA_CLIENTES
    ORDER BY nombre;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_get_most_sold_by_product;
DELIMITER //
CREATE PROCEDURE sp_get_most_sold_by_product(IN limit_val INT)
BEGIN
    SELECT
        p.nombre AS nombre_producto,
        SUM(o.cantidad) AS total_sold
    FROM ORDEN o
    JOIN PRODUCTO p ON o.producto_id = p.producto_id
    GROUP BY p.nombre
    ORDER BY total_sold DESC
    LIMIT limit_val;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_most_sold_by_brand;
DELIMITER //
CREATE PROCEDURE sp_get_most_sold_by_brand(IN limit_val INT)
BEGIN
    SELECT
        m.nombre AS nombre_marca,
        SUM(o.cantidad) AS total_sold
    FROM ORDEN o
    JOIN PRODUCTO p ON o.producto_id = p.producto_id
    LEFT JOIN MARCA m ON p.marca_id = m.marca_id
    GROUP BY m.nombre
    ORDER BY total_sold DESC
    LIMIT limit_val;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_most_sold_by_type;
DELIMITER //
CREATE PROCEDURE sp_get_most_sold_by_type(IN limit_val INT)
BEGIN
    SELECT
        tp.nombre AS tipo_producto,
        SUM(o.cantidad) AS total_sold
    FROM ORDEN o
    JOIN PRODUCTO p ON o.producto_id = p.producto_id
    LEFT JOIN TIPO_PRODUCTO tp ON p.tipo_producto_id = tp.tipo_producto_id
    GROUP BY tp.nombre
    ORDER BY total_sold DESC
    LIMIT limit_val;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_proveedores;
DELIMITER //
CREATE PROCEDURE sp_get_proveedores()
BEGIN
    SELECT proveedor_id, nombre, telefono, correo 
    FROM PROVEEDOR 
    ORDER BY nombre;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_search_proveedor;
DELIMITER //
CREATE PROCEDURE sp_search_proveedor(IN p_nombre VARCHAR(100))
BEGIN
    SELECT proveedor_id, nombre, telefono, correo 
    FROM PROVEEDOR 
    WHERE nombre LIKE p_nombre
    ORDER BY nombre;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_promociones;
DELIMITER //
CREATE PROCEDURE sp_get_promociones()
BEGIN
    SELECT promocion_id, nombre, fecha_inicio, fecha_fin 
    FROM PROMOCION 
    ORDER BY fecha_inicio DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_turnos;
DELIMITER //
CREATE PROCEDURE sp_get_turnos()
BEGIN
    SELECT turno_id, nombre_turno, hora_inicio, hora_fin, cantidad_empleados 
    FROM TURNO 
    ORDER BY turno_id;
END //
DELIMITER ;