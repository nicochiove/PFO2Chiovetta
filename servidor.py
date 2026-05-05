from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from sqlite3 import Connection

app = Flask(__name__)
DB_NAME = "Usuarios.db"


def get_db() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Tabla Usuarios
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()



# Métodos básicos de Autenticación

def get_basic_auth_credentials():
    """
    Lee el header Authorization: Basic ...
    y devuelve (usuario, contraseña) o (None, None)
    """
    auth = request.authorization
    if not auth:
        return None, None
    return auth.username, auth.password


def require_basic_auth():
    """
    Verifica credenciales usando Basic Auth contra la base de datos.
    Devuelve el registro de usuario o una respuesta 401.
    """
    username, password = get_basic_auth_credentials()
    if not username or not password:
        return None, unauthorized_response()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None, unauthorized_response()

    if not check_password_hash(row["password"], password):
        return None, unauthorized_response()

    return row, None


def unauthorized_response():
    resp = make_response(jsonify({"error": "Credenciales inválidas o faltantes"}), 401)
    resp.headers["WWW-Authenticate"] = 'Basic realm="Login requerido"'
    return resp


# Endpoints 

@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
    if not data or "usuario" not in data or "contraseña" not in data:
        return jsonify({"error": "Faltan campos 'usuario' y/o 'contraseña'"}), 400

    usuario = data["usuario"]
    password_plano = data["contraseña"]

    password_hash = generate_password_hash(password_plano)

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
            (usuario, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "usuario" not in data or "contraseña" not in data:
        return jsonify({"error": "Faltan campos 'usuario' y/o 'contraseña'"}), 400

    usuario = data["usuario"]
    password_plano = data["contraseña"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    if not check_password_hash(row["password"], password_plano):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    #Return Mensaje de éxito
    return jsonify(
        {
            "mensaje": "Login exitoso. Usa autenticación básica (usuario/contraseña) para acceder a /tareas."
        }
    ), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario_row, error_resp = require_basic_auth()
    if error_resp:
        return error_resp
    if usuario_row is None:
        return unauthorized_response()
    
    usuario = usuario_row["usuario"]

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Tareas</title>
    </head>
    <body>
        <h1>Bienvenido, {usuario}</h1>
        <p>Este es el sistema de gestión de tareas.</p>
    </body>
    </html>
    """
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}

# Ejecución
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    