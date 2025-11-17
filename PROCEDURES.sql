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