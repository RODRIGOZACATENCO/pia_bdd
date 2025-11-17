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

select * from producto;