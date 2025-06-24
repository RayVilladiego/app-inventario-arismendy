# login.py

USERS = {
    "admin":    {"password": "1234", "rol": "admin"},
    "compras":  {"password": "1234", "rol": "compras"},
    "almacen":  {"password": "1234", "rol": "almacen"},
    "auditor":  {"password": "1234", "rol": "auditor"},
}

def check_login(username, password):
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]["rol"]
    return None
