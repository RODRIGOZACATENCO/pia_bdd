# BISONBAR - Bar Management System

BISONBAR is a desktop Point of Sale (POS) and administration system designed for bar operations, inventory management, sales tracking, and staff management.

## Functions

### Table and POS Management
- Real-time floor plan visualization and table status tracking.
- Client registration and assignment to active tables.
- Order intake with itemized pricing and ticket generation.
- Sale finalization with automatic table release.

### Inventory and Purchase Management
- Product catalog organized by brand and product type.
- Automatic stock reduction during customer orders.
- Purchase order processing with inventory restocking.
- Supplier registration and contact directory.

### Promotions and Pricing Engine
- Promotion creation with start and end date ranges.
- Dynamic item pricing evaluation based on current date promotions.

### Human Resources and Staff Administration
- Employee profiles linked to job positions and work shifts.
- Shift scheduling with start time, end time, and employee quota.
- Employee sales performance tracking.

### System Access and Security
- User authentication with credentials validation.
- Role-based interface customization for Administrators, Servers, Cashiers, and Cooks.

## Technical Features

### Desktop GUI Architecture
- Built with Python and PySide6 (Qt framework).
- Multi-window interface using QStackedWidget and QTabWidget.
- Modular layout split across sales, data input, queries, and administrative modules.
- Custom QSS stylesheets for UI styling.
- Asynchronous UI timer for live metrics and timestamp display.

### Database Backend
- Relational database schema hosted on MySQL.
- Data access layer encapsulated in Python (BarDB class).
- Explicit transaction management for multi-statement atomic database updates.

### Security and Cryptography
- Passwords hashed using PBKDF2 with HMAC-SHA256 and 100,000 iterations.
- Unique 32-byte cryptographically secure salt generated per user account.
- Constant-time hash comparison via hmac.compare_digest to prevent timing attacks.

### Database Audit Logging (Triggers)
- Automated event tracking triggers configured on PRODUCTO, EMPLEADO, CLIENTE, VENTA, ORDEN, and PROVEEDOR.
- Operation tracking (INSERT, UPDATE, DELETE) logged to LOG_CAMBIOS table with timestamp, database user, and detailed field diffs.

### Stored Procedures and Relational Views
- Stored procedures for catalog queries, sales aggregation, and best-selling product analysis.
- Database views encapsulating multi-table joins for product catalogs, staff lists, and employee revenue summaries.

### Role-Based Access Control (RBAC)
- Dynamic UI tab enabling and disabling based on employee position.
- Server/Cashier role: restricted to POS and table management.
- Cook role: restricted to product and query views.
- Administrator role: full access to HR, user account creation, system configuration, and audit logs.

## System Architecture

```
pia_bdd/
|-- CREACION_BASE_DATOS.sql
|-- PROCEDURES.sql
|-- TRIGGERS.sql
|-- VISTAS.sql
|-- DATOS_PRUEBA.sql
|-- FULL_SQL.sql
`-- GUI/
    |-- app/
    |   |-- MainApp.py
    |   |-- bar_db.py
    |   |-- auth_utils.py
    |   `-- validation_utils.py
    |-- resources/
    `-- windows/
        |-- administrative/
        |-- data_input/
        |-- queries/
        `-- sales/
```

## Setup and Execution

### Requirements
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- PySide6
- mysql-connector-python

### Database Setup
1. Execute `CREACION_BASE_DATOS.sql` to initialize database schema and tables.
2. Execute `PROCEDURES.sql` to register stored procedures.
3. Execute `TRIGGERS.sql` to configure audit log triggers.
4. Execute `VISTAS.sql` to create database views.
5. (Optional) Execute `DATOS_PRUEBA.sql` to populate initial test data.

### Running the Application
1. Configure MySQL connection parameters in `GUI/app/MainApp.py`.
2. Run the main entry point:
   ```bash
   python GUI/app/MainApp.py
   ```
