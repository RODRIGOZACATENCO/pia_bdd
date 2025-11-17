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