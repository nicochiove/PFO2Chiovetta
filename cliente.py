import requests
from getpass import getpass

BASE_URL = "http://127.0.0.1:5000"


def registrar():
    usuario = input("Usuario nuevo: ")
    password = getpass("Contraseña: ")
    resp = requests.post(
        f"{BASE_URL}/registro",
        json={"usuario": usuario, "contraseña": password},
    )
    print(resp.status_code, resp.json())


def login_y_ver_tareas():
    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    # Login
    resp_login = requests.post(
        f"{BASE_URL}/login",
        json={"usuario": usuario, "contraseña": password},
    )
    print("LOGIN:", resp_login.status_code, resp_login.json())

    if resp_login.status_code != 200:
        return

    # Acceso a /tareas con Basic Auth
    resp_tareas = requests.get(f"{BASE_URL}/tareas", auth=(usuario, password))
    print("TAREAS:", resp_tareas.status_code)
    print(resp_tareas.text)


if __name__ == "__main__":
    print("1) Registrar\n2) Login y ver tareas")
    op = input("Opción: ")
    if op == "1":
        registrar()
    else:
        login_y_ver_tareas()