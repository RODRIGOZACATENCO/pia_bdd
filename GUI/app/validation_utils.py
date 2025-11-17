import re
from PySide6.QtWidgets import QMessageBox

def is_not_empty(value):
    return bool(value)

def is_valid_date(date_string):
    # Regex for YYYY-MM-DD format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
        return False
    # Additional date validity check would be ideal but complex without specific library
    return True

def is_positive_number(value):
    try:
        return float(value) > 0
    except ValueError:
        return False

def show_warning(parent, title, message):
    QMessageBox.warning(parent, title, message)