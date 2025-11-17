import mysql.connector

import sys
import datetime

from auth_utils import hash_password, verify_password
from mysql.connector import Error, IntegrityError


def get_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                continue
            if max_value is not None and value > max_value:
                continue
            return value
        except ValueError:
            print("Integer error")
            pass


def get_float(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                continue
            if max_value is not None and value > max_value:
                continue
            return value
        except ValueError:
            print("Float error")
            pass


class Table:
    def __init__(self, table_id, capacity, table_name, employee_id):
        self.table_id = table_id
        self.capacity = capacity
        self.table_name = table_name
        self.employee_id = employee_id
        self.client_id = 0
        self.is_occupied = False
        self.sale_id = 0

    def occupy_table(self, client_id, sale_id):
        self.client_id = client_id
        self.sale_id = sale_id
        self.is_occupied = True

    def free_table(self):
        self.client_id = 0
        self.sale_id = 0
        self.is_occupied = False

    def __str__(self):
        return f"Mesa {self.table_id}, Ocupada: {self.is_occupied}, Cliente: {self.client_id}"


class BarDB:
    def __init__(self):
        self.host = None
        self.user = None
        self.password = None
        self.database_name = None
        self.connection = None
        self.tables = []
        self.employee_id = 1

    def search_client(self, client_name):
        active_client_ids = [table.client_id for table in self.tables if table.is_occupied and table.client_id != 0]
        query = "SELECT cliente_id, nombre, telefono, correo from CLIENTE WHERE (nombre LIKE %s OR telefono LIKE %s OR correo LIKE %s)"
        params = [f"%{client_name}%", f"%{client_name}%", f"%{client_name}%"]

        if active_client_ids:
            placeholders = ', '.join(['%s'] * len(active_client_ids))
            query += f" AND cliente_id NOT IN ({placeholders})"
            params.extend(active_client_ids)

        result = self.execute_query(query, tuple(params), fetch=True)
        return result

    def authenticate_user(self, username, password):
        query_user = """
            SELECT empleado_id, password_hash, password_salt 
            FROM USUARIO_SISTEMA 
            WHERE username = %s
        """
        params_user = (username,)
        user_data = self.execute_query(query_user, params_user, fetch=True)

        if not user_data:
            print("Error: User not found.")
            return None, None

        empleado_id, db_hash, db_salt = user_data[0]

        if not verify_password(db_hash, db_salt, password):
            print("Error: Incorrect password.")
            return None, None

        query_role = """
            SELECT e.nombre, p.nombre 
            FROM EMPLEADO e
            JOIN PUESTO p ON e.puesto_id = p.puesto_id
            WHERE e.empleado_id = %s
        """
        params_role = (empleado_id,)
        role_data = self.execute_query(query_role, params_role, fetch=True)

        if role_data:
            employee_name = role_data[0][0]
            position_name = role_data[0][1]
            return employee_name, position_name
        else:
            print("Error: Employee not found for user.")
            return None, None

    def get_employees_without_user_account(self):
        query = """
            SELECT e.empleado_id, e.nombre, p.nombre 
            FROM EMPLEADO e
            JOIN PUESTO p ON e.puesto_id = p.puesto_id
            WHERE e.empleado_id NOT IN (
                SELECT empleado_id FROM USUARIO_SISTEMA
            )
            ORDER BY e.nombre
        """
        try:
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching employees without account: {e}")
            return []

    def create_system_user(self, empleado_id, username, password):
        try:
            salt_hex, hash_hex = hash_password(password)
            query = """
                INSERT INTO USUARIO_SISTEMA (empleado_id, username, password_hash, password_salt) 
                VALUES (%s, %s, %s, %s)
            """
            params = (empleado_id, username, hash_hex, salt_hex)

            user_id = self.execute_query(query, params)
            if user_id:
                return True, "User created successfully."
            else:
                return False, "Unknown error creating user."

        except IntegrityError as e:
            if e.errno == 1062:
                return False, "That username already exists."
            else:
                return False, f"Database error: {e}"
        except Error as e:
            print(f"Error creating system user: {e}")
            return False, f"Error: {e}"

    def start_connection(self, host, user, password, database_name):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            if self.connection.is_connected():
                print(f"Successfully connected to database '{self.database_name}'")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            sys.exit(1)
        query = """
        SELECT * FROM MESA
        """
        tables_data = self.execute_query(query, fetch=True)
        for table_data in tables_data:
            self.tables.append(Table(table_data[0], table_data[1], table_data[2], self.employee_id))

    def assign_table(self, table_id, client_id):
        query = """
        INSERT INTO VENTA (cliente_id, empleado_id, mesa_id, total_venta, fecha) 
        VALUES (%s, %s, %s, %s, %s)
        """

        # --- FIX ---
        # Changed datetime.date.today() to datetime.datetime.now()
        params = (client_id, self.employee_id, table_id, 0, datetime.datetime.now())
        # --- END FIX ---

        sale_id = self.execute_query(query, params)
        table = self.get_table_by_id(table_id)
        if table:
            table.occupy_table(client_id, sale_id)

    def register_order_cli(self):
        print("--REGISTER ORDER--")
        for table in self.tables:
            if table.is_occupied:
                print(table)
        table_num = int(input("Table number: ")) - 1
        product_name = input("Product ordered: ")
        quantity = int(input("Quantity ordered: "))
        table = self.tables[table_num]
        if table.is_occupied:
            product_data = self.check_product_availability_cli(product_name, quantity)
            if product_data:
                product_id, _, price = product_data
                self.register_order_gui(table.sale_id, product_id, quantity, price, None)
                print("Order registered")

    def register_client_cli(self):
        print("REGISTER CLIENT")
        name = input("name: ")
        phone_num = input("phone: ")
        email = input("email: ")
        dob = input("dob:")
        self.register_client_gui(name, phone_num, email, dob)

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def execute_query(self, query, params=None, fetch=False, use_transaction=False):
        cursor = None
        try:
            if use_transaction and self.connection.in_transaction:
                cursor = self.connection.cursor()
            else:
                cursor = self.connection.cursor()

            if params:
                if query.strip().upper().startswith("CALL"):
                    cursor.callproc(query.strip()[5:].split('(')[0], params)
                else:
                    cursor.execute(query, params)
            else:
                if query.strip().upper().startswith("CALL"):
                    cursor.callproc(query.strip()[5:].split('(')[0])
                else:
                    cursor.execute(query)

            if fetch:
                if query.strip().upper().startswith("CALL"):
                    results = []
                    for result in cursor.stored_results():
                        results.extend(result.fetchall())
                    return results
                else:
                    results = cursor.fetchall()
                    return results
            else:
                if not use_transaction:
                    self.connection.commit()
                return cursor.lastrowid

        except Error as e:
            print(f"Error executing query: {e}")
            if use_transaction:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def check_product_availability_cli(self, product: str, quantity: int) -> str:
        try:
            query = "SELECT * FROM PRODUCTO WHERE nombre LIKE %s"
            params = (f"%{product}%",)
            result = self.execute_query(query, params, fetch=True)
            print(result)
            if len(result) == 1:
                result = result[0]
                if result[5] >= quantity:
                    return result[0], result[1], result[4]
                else:
                    print("Not enough product in stock for the order")
                    return False

            else:
                print("Invalid product")
                return False
        except Error as e:
            print(e)
            return False

    def get_table_by_id(self, table_id):
        for table in self.tables:
            if table.table_id == table_id:
                return table
        return None

    def register_client_gui(self, name, phone, email, dob):
        query = """
        INSERT INTO CLIENTE(nombre,telefono,correo,fecha_nacimiento)
            VALUES(%s,%s,%s,%s)
        """
        params = (name, phone, email, dob)
        new_id = self.execute_query(query, params)
        return new_id

    def finalize_sale(self, sale_id):
        query_sum = "SELECT SUM(cantidad * precio_al_vender) FROM ORDEN WHERE venta_id = %s"
        params_sum = (sale_id,)
        result = self.execute_query(query_sum, params_sum, fetch=True)
        total = 0
        if result and result[0][0] is not None:
            total = float(result[0][0])

        query_update = "UPDATE VENTA SET total_venta = %s WHERE venta_id = %s"
        params_update = (total, sale_id)
        self.execute_query(query_update, params_update)

        for table in self.tables:
            if table.sale_id == sale_id:
                table.free_table()
                break
        return total

    def search_product_gui(self, product_name):
        query = """
            SELECT
                p.producto_id,
                p.nombre,
                p.precio AS precio_regular,
                p.stock,
                dp.precio_oferta,
                pr.promocion_id
            FROM PRODUCTO p
            LEFT JOIN DETALLE_PROMOCION dp ON p.producto_id = dp.producto_id
            LEFT JOIN PROMOCION pr ON dp.promocion_id = pr.promocion_id
                AND CURDATE() BETWEEN pr.fecha_inicio AND pr.fecha_fin
            LEFT JOIN MARCA m ON p.marca_id = m.marca_id
            WHERE (p.nombre LIKE %s OR m.nombre LIKE %s) AND p.stock > 0
        """
        params = (f"%{product_name}%", f"%{product_name}%")

        db_results = self.execute_query(query, params, fetch=True)

        final_results = []
        if db_results:
            for row in db_results:
                (prod_id, nombre, precio_reg, stock, precio_oferta, promo_id) = row

                if precio_oferta and promo_id:
                    precio_a_vender = precio_oferta
                    promocion_id_final = promo_id
                else:
                    precio_a_vender = precio_reg
                    promocion_id_final = None

                final_results.append((prod_id, nombre, precio_a_vender, stock, promocion_id_final))

        return final_results

    def check_product_availability_gui(self, product_id, quantity):
        query = "SELECT stock FROM PRODUCTO WHERE producto_id = %s"
        params = (product_id,)
        result = self.execute_query(query, params, fetch=True)
        if result and result[0][0] >= quantity:
            return True
        return False

    def register_order_gui(self, sale_id, product_id, quantity, price_at_sale, promocion_id):
        if self.check_product_availability_gui(product_id, quantity):
            query = """
            INSERT INTO ORDEN (venta_id, producto_id, promocion_id, cantidad, precio_al_vender) 
            VALUES (%s,%s,%s,%s,%s)
            """
            params = (sale_id, product_id, promocion_id, quantity, price_at_sale)
            self.execute_query(query, params)

            query_update = """
            UPDATE PRODUCTO
            SET stock = stock - %s
            WHERE producto_id = %s
            """
            params_update = (quantity, product_id)
            self.execute_query(query_update, params_update)
            return True
        else:
            return False

    def get_total_orders_today(self):
        try:
            query = "SELECT COUNT(*) FROM VENTA WHERE DATE(fecha) = %s"
            params = (datetime.date.today(),)
            result = self.execute_query(query, params, fetch=True)
            if result and result[0][0] is not None:
                return int(result[0][0])
            return 0
        except Error as e:
            print(f"Error fetching total orders: {e}")
            return 0

    def get_sales_between_dates(self, start_date, end_date):
        try:
            query = """
                SELECT v.venta_id, c.nombre, e.nombre, v.total_venta, v.fecha 
                FROM VENTA v
                LEFT JOIN CLIENTE c ON v.cliente_id = c.cliente_id
                LEFT JOIN EMPLEADO e ON v.empleado_id = e.empleado_id
                WHERE DATE(v.fecha) BETWEEN %s AND %s 
                ORDER BY v.fecha DESC
            """
            params = (start_date, end_date)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error fetching sales between dates: {e}")
            return []

    def get_most_sold_by_product(self, limit=20):
        try:
            query = "CALL sp_get_most_sold_by_product(%s)"
            params = (limit,)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error fetching most sold items by product: {e}")
            return []

    def get_most_sold_by_brand(self, limit=20):
        try:
            query = "CALL sp_get_most_sold_by_brand(%s)"
            params = (limit,)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error fetching most sold items by brand: {e}")
            return []

    def get_most_sold_by_type(self, limit=20):
        try:
            query = "CALL sp_get_most_sold_by_type(%s)"
            params = (limit,)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error fetching most sold items by type: {e}")
            return []

    def get_vista_clientes(self):
        try:
            query = "CALL sp_get_clientes()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching client view: {e}")
            return []

    def get_vista_productos(self):
        try:
            query = "CALL sp_get_catalogo_productos()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching product view: {e}")
            return []

    def get_vista_personal(self):
        try:
            query = "CALL sp_get_personal()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching personal view: {e}")
            return []

    def get_vista_resumen_ventas_empleado(self):
        try:
            query = "CALL sp_get_resumen_ventas_empleado()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching employee sales summary: {e}")
            return []

    def get_vista_proveedores(self):
        try:
            query = "CALL sp_get_proveedores()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching supplier view: {e}")
            return []

    def search_proveedor(self, name):
        try:
            query = "CALL sp_search_proveedor(%s)"
            params = (f"%{name}%",)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error searching suppliers: {e}")
            return []

    def get_vista_promociones(self):
        try:
            query = "CALL sp_get_promociones()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching promotion view: {e}")
            return []

    def get_vista_turnos(self):
        try:
            query = "CALL sp_get_turnos()"
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching shift view: {e}")
            return []

    def get_shifts_list(self):
        query = "SELECT turno_id, nombre_turno FROM TURNO ORDER BY nombre_turno"
        return self.execute_query(query, fetch=True)

    def get_puestos_list(self):
        query = "SELECT puesto_id, nombre FROM PUESTO ORDER BY nombre"
        return self.execute_query(query, fetch=True)

    def get_user_accounts_view(self):
        query = """
            SELECT us.usuario_id, us.username, e.nombre, p.nombre
            FROM USUARIO_SISTEMA us
            JOIN EMPLEADO e ON us.empleado_id = e.empleado_id
            JOIN PUESTO p ON e.puesto_id = p.puesto_id
            ORDER BY e.nombre
        """
        try:
            return self.execute_query(query, fetch=True)
        except Error as e:
            print(f"Error fetching user accounts view: {e}")
            return []

    def get_promotion_details(self, promotion_id):
        try:
            query = """
                SELECT 
                    p.nombre AS nombre_producto,
                    p.precio AS precio_regular,
                    dp.precio_oferta
                FROM DETALLE_PROMOCION dp
                JOIN PRODUCTO p ON dp.producto_id = p.producto_id
                WHERE dp.promocion_id = %s
            """
            params = (promotion_id,)
            return self.execute_query(query, params, fetch=True)
        except Error as e:
            print(f"Error fetching promotion details: {e}")
            return []

    def get_total_products(self):
        try:
            query = "SELECT COUNT(*) FROM PRODUCTO"
            result = self.execute_query(query, fetch=True)
            return int(result[0][0]) if result and result[0][0] is not None else 0
        except Error as e:
            print(f"Error fetching total products: {e}")
            return 0

    def get_total_suppliers(self):
        try:
            query = "SELECT COUNT(*) FROM PROVEEDOR"
            result = self.execute_query(query, fetch=True)
            return int(result[0][0]) if result and result[0][0] is not None else 0
        except Error as e:
            print(f"Error fetching total suppliers: {e}")
            return 0

    def get_total_employees(self):
        try:
            query = "SELECT COUNT(*) FROM EMPLEADO"
            result = self.execute_query(query, fetch=True)
            return int(result[0][0]) if result and result[0][0] is not None else 0
        except Error as e:
            print(f"Error fetching total employees: {e}")
            return 0

    def get_sale_data_for_ticket(self, sale_id):
        try:
            query_header = """
                SELECT
                    v.fecha,
                    e.nombre AS empleado_nombre
                FROM VENTA v
                JOIN EMPLEADO e ON v.empleado_id = e.empleado_id
                WHERE v.venta_id = %s
            """
            header_data = self.execute_query(query_header, (sale_id,), fetch=True)
            if not header_data:
                return None

            fecha_hora, empleado_nombre = header_data[0]
            fecha_str = fecha_hora.strftime("%Y-%m-%d")
            hora_str = fecha_hora.strftime("%H:%M:%S")

            query_details = """
                SELECT
                    p.nombre,
                    o.cantidad,
                    o.precio_al_vender
                FROM ORDEN o
                JOIN PRODUCTO p ON o.producto_id = p.producto_id
                WHERE o.venta_id = %s
            """
            order_details = self.execute_query(query_details, (sale_id,), fetch=True)

            return {
                "venta_id": sale_id,
                "fecha": fecha_str,
                "hora": hora_str,
                "empleado_nombre": empleado_nombre,
                "orden_detalles": order_details
            }
        except Error as e:
            print(f"Error fetching sale data for ticket: {e}")
            return None

    def add_new_table(self, capacity, location):
        query = "INSERT INTO MESA (capacidad, ubicacion) VALUES (%s, %s)"
        params = (capacity, location)
        return self.execute_query(query, params)

    def add_new_product(self, name, brand_id, type_id, price, stock):
        query = "INSERT INTO PRODUCTO (nombre, marca_id, tipo_producto_id, precio, stock) VALUES (%s, %s, %s, %s, %s)"
        params = (name, brand_id, type_id, price, stock)
        return self.execute_query(query, params)

    def add_new_promotion(self, name, start_date, end_date):
        query = "INSERT INTO PROMOCION (nombre, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)"
        params = (name, start_date, end_date)
        return self.execute_query(query, params)

    def add_new_supplier(self, name, phone, email):
        query = "INSERT INTO PROVEEDOR (nombre, telefono, correo) VALUES (%s, %s, %s)"
        params = (name, phone, email)
        return self.execute_query(query, params)

    def add_new_product_type(self, name):
        query = "INSERT INTO TIPO_PRODUCTO (nombre) VALUES (%s)"
        params = (name,)
        return self.execute_query(query, params)

    def add_new_shift(self, name, start_time, end_time, employee_count):
        query = "INSERT INTO TURNO (nombre_turno, hora_inicio, hora_fin, cantidad_empleados) VALUES (%s, %s, %s, %s)"
        params = (name, start_time, end_time, employee_count)
        return self.execute_query(query, params)

    def add_new_employee(self, shift_id, position_id, name, salary):
        query = "INSERT INTO EMPLEADO (turno_id, puesto_id, nombre, salario) VALUES (%s, %s, %s, %s)"
        params = (shift_id, position_id, name, salary)
        return self.execute_query(query, params)

    def get_suppliers_list(self):
        query = "SELECT proveedor_id, nombre FROM PROVEEDOR ORDER BY nombre"
        return self.execute_query(query, fetch=True)

    def get_products_list(self):
        query = "SELECT producto_id, nombre FROM PRODUCTO ORDER BY nombre"
        return self.execute_query(query, fetch=True)

    def add_new_purchase_order(self, supplier_id, date, total, details):
        try:
            self.connection.start_transaction()

            order_query = "INSERT INTO ORDEN_COMPRA (proveedor_id, fecha_suministro, total_pago) VALUES (%s, %s, %s)"
            order_params = (supplier_id, date, total)
            order_id = self.execute_query(order_query, order_params, use_transaction=True)

            if not order_id:
                raise Exception("Failed to create purchase order")

            for (product_id, price, quantity) in details:
                detail_query = "INSERT INTO DETALLE_ORDEN_COMPRA (orden_compra_id, producto_id, precio_compra, cantidad_comprada) VALUES (%s, %s, %s, %s)"
                detail_params = (order_id, product_id, price, quantity)
                detail_id = self.execute_query(detail_query, detail_params, use_transaction=True)

                if not detail_id:
                    raise Exception("Failed to add purchase order detail")

                stock_query = "UPDATE PRODUCTO SET stock = stock + %s WHERE producto_id = %s"
                stock_params = (quantity, product_id)
                self.execute_query(stock_query, stock_params, use_transaction=True)

            self.connection.commit()
            return order_id
        except Exception as e:
            self.connection.rollback()
            print(f"Transaction failed: {e}")
            return None

    def add_new_promotion_with_details(self, name, start_date, end_date, details):
        try:
            self.connection.start_transaction()

            promo_query = "INSERT INTO PROMOCION (nombre, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)"
            promo_params = (name, start_date, end_date)
            promo_id = self.execute_query(promo_query, promo_params, use_transaction=True)

            if not promo_id:
                raise Exception("Failed to create promotion")

            for (product_id, offer_price) in details:
                detail_query = "INSERT INTO DETALLE_PROMOCION (promocion_id, producto_id, precio_oferta) VALUES (%s, %s, %s)"
                detail_params = (promo_id, product_id, offer_price)
                detail_id = self.execute_query(detail_query, detail_params, use_transaction=True)

                if not detail_id:
                    raise Exception("Failed to add promotion detail")

            self.connection.commit()
            return promo_id
        except Exception as e:
            self.connection.rollback()
            print(f"Transaction failed: {e}")
            return None

    def update_client(self, client_id, column_name, new_value):
        allowed_columns = {
            "Nombre": "nombre",
            "Teléfono": "telefono",
            "Correo": "correo",
            "Fecha Nacimiento": "fecha_nacimiento"
        }
        db_column = allowed_columns.get(column_name)

        if not db_column:
            print(f"Error: Non-editable column '{column_name}'")
            return False

        query = f"UPDATE CLIENTE SET {db_column} = %s WHERE cliente_id = %s"
        params = (new_value, client_id)
        self.execute_query(query, params)
        return True

    def update_supplier(self, supplier_id, column_name, new_value):
        allowed_columns = {
            "Nombre": "nombre",
            "Teléfono": "telefono",
            "Correo": "correo"
        }
        db_column = allowed_columns.get(column_name)

        if not db_column:
            print(f"Error: Non-editable column '{column_name}'")
            return False

        query = f"UPDATE PROVEEDOR SET {db_column} = %s WHERE proveedor_id = %s"
        params = (new_value, supplier_id)
        self.execute_query(query, params)
        return True

    def update_promotion(self, promotion_id, column_name, new_value):
        allowed_columns = {
            "Nombre": "nombre",
            "Fecha Inicio": "fecha_inicio",
            "Fecha Fin": "fecha_fin"
        }
        db_column = allowed_columns.get(column_name)

        if not db_column:
            print(f"Error: Non-editable column '{column_name}'")
            return False

        query = f"UPDATE PROMOCION SET {db_column} = %s WHERE promocion_id = %s"
        params = (new_value, promotion_id)
        self.execute_query(query, params)
        return True

    def update_shift(self, shift_id, column_name, new_value):
        allowed_columns = {
            "Nombre": "nombre_turno",
            "Hora Inicio": "hora_inicio",
            "Hora Fin": "hora_fin",
            "N. Empleados": "cantidad_empleados"
        }
        db_column = allowed_columns.get(column_name)

        if not db_column:
            print(f"Error: Non-editable column '{column_name}'")
            return False

        query = f"UPDATE TURNO SET {db_column} = %s WHERE turno_id = %s"
        params = (new_value, shift_id)
        self.execute_query(query, params)
        return True


DB_GLOBAL = BarDB()