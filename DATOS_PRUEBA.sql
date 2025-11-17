INSERT INTO CLIENTE (nombre, telefono, correo, fecha_nacimiento) VALUES
('Carlos Hernández', '5551234567', 'carlos.h@gmail.com', '1990-03-12'),
('Lucía Torres', '5559876543', 'lucia.t@gmail.com', '1985-07-22'),
('Miguel Sánchez', '5557418529', 'miguel.s@example.com', '1992-11-05'),
('Ana Pérez', '5553692584', 'ana.p@gmail.com', '1998-04-18'),
('Sofía Morales', '5557531594', 'sofia.m@example.com', '2000-06-09'),
('José Ramírez', '5551112233', 'jose.r@example.com', '1982-02-02'),
('Fernando Ríos', '5552223344', 'fer.rios@example.com', '1995-09-15'),
('Mariana Vega', '5553334455', 'mariana.v@example.com', '1999-01-28'),
('Elena Duarte', '5554445566', 'elena.d@example.com', '1987-10-10'),
('Pablo Mendoza', '5555556677', 'pablo.m@example.com', '1993-08-17'),
('Ricardo Castillo', '5556667788', 'ricardo.c@example.com', '1980-12-30'),
('Guillermo Lara', '5557778899', 'guillermo.l@example.com', '1997-05-04'),
('Daniela Flores', '5558889900', 'daniela.f@example.com', '2001-09-27'),
('Laura Reyes', '5559990011', 'laura.r@example.com', '1994-03-14'),
('Iván Campos', '5551002003', 'ivan.c@example.com', '1996-07-06'),
('Claudia Rivas', '5552003004', 'claudia.r@example.com', '1991-11-19'),
('Jorge Estrada', '5553004005', 'jorge.e@example.com', '1989-08-01'),
('Brenda Núñez', '5554005006', 'brenda.n@example.com', '1997-12-11'),
('Rafael Luna', '5555006007', 'rafael.l@example.com', '1995-04-24'),
('Patricia Silva', '5556007008', 'paty.s@example.com', '1984-06-02'),
('Héctor Márquez', '5557008009', 'hector.m@example.com', '1990-01-08'),
('Karina Soto', '5558009001', 'karina.s@example.com', '1992-12-20'),
('Andrés Cruz', '5559001002', 'andres.c@example.com', '1998-07-17'),
('Fabiola Peña', '5550102030', 'fabiola.p@example.com', '1999-09-09'),
('Erick Bravo', '5550203040', 'erick.b@example.com', '1991-05-21'),
('Teresa Pineda', '5550304050', 'teresa.p@example.com', '1986-03-03'),
('Adrián Mejía', '5550405060', 'adrian.m@example.com', '1994-10-25'),
('Silvia Calderón', '5550506070', 'silvia.c@example.com', '1988-11-11'),
('Omar Vázquez', '5550607080', 'omar.v@example.com', '1997-02-14'),
('Paola Navarro', '5550708090', 'paola.n@example.com', '1993-12-01');

INSERT INTO MESA (capacidad, ubicacion) VALUES
(2, 'Terraza'),
(4, 'Terraza'),
(4, 'Centro'),
(6, 'Centro'),
(2, 'Esquina'),
(4, 'Esquina'),
(6, 'Ventana'),
(2, 'Ventana'),
(8, 'Privado');

INSERT INTO PROVEEDOR (nombre, telefono, correo) VALUES
('Distribuidora del Norte', '5558881122', 'contacto@norte.com'),
('Bebidas MX', '5557773311', 'ventas@bebidasmx.com'),
('La Cervecera', '5556664411', 'pedidos@cervecera.com'),
('Vinos Selectos', '5555558822', 'ventas@vinosselectos.com'),
('Refrescos Plus', '5554449933', 'info@refrescosplus.com'),
('Carnes Premium', '5553332211', 'ventas@carnespremium.com'),
('Snacks Unidos', '5552221133', 'snacks@unidos.com'),
('Gourmet House', '5551112244', 'contacto@gourmethouse.com'),
('Café Central', '5559992233', 'ventas@cafecentral.com'),
('Panadería Fina', '5558883344', 'pan@fina.com');

INSERT INTO TURNO (nombre_turno, hora_inicio, hora_fin, cantidad_empleados) VALUES
('Mañana', '08:00:00', '14:00:00', 5),
('Tarde', '14:00:00', '20:00:00', 7),
('Noche', '20:00:00', '02:00:00', 8);

INSERT INTO MARCA (nombre) VALUES
('Corona'),
('Modelo'),
('Coca-Cola'),
('Pepsi'),
('Bacardi'),
('Absolut'),
('Herradura'),
('Jack Daniels'),
('Red Bull'),
('Monster');

INSERT INTO TIPO_PRODUCTO (nombre) VALUES
('Cerveza'),
('Refresco'),
('Tequila'),
('Vodka'),
('Whisky'),
('Energético'),
('Snack'),
('Vino'),
('Café'),
('Postre');

INSERT INTO PRODUCTO (nombre, marca_id, tipo_producto_id, precio, stock) VALUES
('Corona Ligera 355ml', 1, 1, 25.00, 200),
('Modelo Especial 355ml', 2, 1, 28.00, 180),
('Coca-Cola 600ml', 3, 2, 18.00, 250),
('Pepsi 600ml', 4, 2, 17.00, 240),
('Tequila Herradura Reposado', 7, 3, 850.00, 20),
('Vodka Absolut 1L', 6, 4, 420.00, 25),
('Whisky Jack Daniels', 8, 5, 750.00, 15),
('Red Bull 250ml', 9, 6, 40.00, 100),
('Monster 455ml', 10, 6, 42.00, 90),
('Papas Fritas', 7, 7, 25.00, 120),
('Pistaches', 7, 7, 45.00, 80),
('Nueces', 7, 7, 48.00, 70),
('Vino Tinto Reserva', 4, 8, 320.00, 35),
('Café Americano', 9, 9, 30.00, 150),
('Café Cappuccino', 9, 9, 40.00, 140),
('Pastel de Chocolate', 10, 10, 55.00, 40),
('Cheesecake', 10, 10, 60.00, 35),
('Cerveza Corona Mega', 1, 1, 35.00, 150),
('Modelo Negra', 2, 1, 29.00, 150),
('Coca-Cola Light 600ml', 3, 2, 20.00, 200),
('Pepsi Light 600ml', 4, 2, 19.00, 200),
('Tequila Blanco Herradura', 7, 3, 700.00, 18),
('Absolut Raspberry', 6, 4, 450.00, 20),
('Whisky Old Parr', 8, 5, 890.00, 10),
('Chips Picantes', 7, 7, 26.00, 110),
('Galletas Saladas', 7, 7, 22.00, 130),
('Vino Blanco', 4, 8, 280.00, 30),
('Café Latte', 9, 9, 38.00, 160),
('Café Espresso', 9, 9, 32.00, 180),
('Brownie', 10, 10, 48.00, 50),
('Flan Napolitano', 10, 10, 45.00, 45),
('Cerveza Ultra', 2, 1, 27.00, 170),
('Coca-Cola Zero 600ml', 3, 2, 19.00, 220),
('Pepsi Zero 600ml', 4, 2, 18.00, 210),
('Vodka Absolut Citron', 6, 4, 430.00, 22),
('Red Bull Sugar Free', 9, 6, 41.00, 90),
('Monster Ultra', 10, 6, 43.00, 85),
('Chicharrones', 7, 7, 28.00, 100),
('Mix de Semillas', 7, 7, 50.00, 75);

INSERT INTO PUESTO (nombre) VALUES
('Mesero'),
('Cocinero'),
('Cajero'),
('Administrador'),
('Limpieza');

INSERT INTO EMPLEADO (turno_id, puesto_id, nombre, salario) VALUES
(1, 1, 'Juan López', 9000),
(1, 2, 'Pedro García', 11000),
(1, 5, 'Marta Ruiz', 7500),
(2, 1, 'Luis Fernández', 9200),
(2, 3, 'Andrea Gómez', 9500),
(2, 4, 'César Morales', 15000),
(3, 1, 'Diego Castro', 9500),
(3, 2, 'Esteban Ríos', 11500),
(3, 5, 'Rosa López', 7800);

INSERT INTO USUARIO (puesto_id, tipo_usuario) VALUES
(4, 'Admin'),
(3, 'Cajero'),
(1, 'Mesero'),
(2, 'Cocinero'),
(5, 'Limpieza');

INSERT INTO ORDEN_COMPRA (proveedor_id, fecha_suministro, total_pago) VALUES
(1, '2024-01-12', 3500),
(3, '2024-01-18', 5200),
(2, '2024-02-05', 4100),
(4, '2024-02-14', 7200),
(5, '2024-02-20', 1800);

INSERT INTO PROMOCION (nombre, fecha_inicio, fecha_fin) VALUES
('Promo Cerveza Enero', '2024-01-01', '2024-01-31'),
('Promo Energéticos Febrero', '2024-02-01', '2024-02-29'),
('Promo Snacks 2x1', '2024-03-01', '2024-03-15');

INSERT INTO DETALLE_PROMOCION (promocion_id, producto_id, precio_oferta) VALUES
(1, 1, 22.00),
(1, 2, 24.00),
(2, 8, 35.00),
(2, 9, 36.00),
(3, 10, 15.00);

INSERT INTO VENTA (cliente_id, empleado_id, mesa_id, total_venta) VALUES
(1, 1, 1, 120.00),
(2, 4, 3, 250.00),
(5, 7, 2, 180.00),
(10, 1, 5, 340.00),
(12, 4, 7, 90.00);

INSERT INTO ORDEN (venta_id, producto_id, promocion_id, cantidad, precio_al_vender) VALUES
(1, 1, 1, 2, 22.00),
(1, 10, NULL, 1, 25.00),
(2, 7, NULL, 1, 750.00),
(2, 3, NULL, 3, 18.00),
(3, 8, 2, 2, 35.00),
(4, 13, NULL, 1, 320.00),
(4, 16, NULL, 1, 55.00),
(5, 3, NULL, 1, 18.00);

-- --- Asignar usuarios y contraseñas (hasheadas) ---
-- Inserción de usuarios en la nueva tabla USUARIO_SISTEMA
-- Las contraseñas están hasheadas con PBKDF2-SHA256 (iter=100000)

-- Rol Admin (César Morales, empleado_id = 6)
-- user: admin, pass: admin
INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) VALUES
(6, 'admin', '2b01e34b413c1b61c11e403d211f6c4b69327d5ab8537c355c707d81b312702b', 'salt_for_admin_123');

-- Rol Sales (Juan López, empleado_id = 1)
-- user: sales, pass: sales
INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) VALUES
(1, 'sales', '9948c2635c4a7f051c1448bb574d7f50a80e15f3a1dff5c9c8553f19114d5673', 'salt_for_sales_456');

-- Rol Query (Pedro García, empleado_id = 2)
-- user: query, pass: query
INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) VALUES
(2, 'query', '4f0dabe01b7a69c1186b8641a27e7d91e6b8a8b8d03f0b2a7589254c0001851e', 'salt_for_query_789');

-- Rol Sales (Andrea Gómez, empleado_id = 5)
-- user: cajero, pass: 123
INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) VALUES
(5, 'cajero', '14e91f1118120619a9f4e242b58c7f99965f81f81d113c2f0f59b6c0e5e34778', 'salt_for_cajero_123');

-- Rol Sales (Luis Fernández, empleado_id = 4)
-- user: mesero2, pass: 123
INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) VALUES
(4, 'mesero2', '02b483c6f1166a0d24c3e80d4638a5b7c768f51178c187f5817f54c9c10f5127', 'salt_for_mesero2_123');