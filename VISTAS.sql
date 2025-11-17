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