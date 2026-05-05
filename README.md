# PFO2Chiovetta

## Requerimientos
- Flask
- Werkzeug

### Instalación
* pip install Flask
* pip install werkzeug (Instalando Flask puede no ser necesario este paso)

## Instrucciones
1. Ejecutar en una terminal el archivo **servidor** (py servidor.py).
2. Ejecutar el **cliente** en otra terminal (py cliente.py).
3. Para agregar un **nuevo Usuario**, inmediatamente luego de ejecutar el cliente, ingresar 1; luego ingresar usuario y contraseña.
4. Para utilizar el **login**, inmediatamente luego de ejecutar el cliente, ingresar 2; luego ingresar usuario y contraseña previamente agregados. 

## Capturas
![Inicio Servidor](/capturas/servidor_inicio.png)
![Registro Exitoso](/capturas/registro_ok.png)
![Login Exitoso](/capturas/login_ok.png)
![Login con Error](/capturas/login_error.png)
![Tareas Exitoso](/capturas/tareas_ok.png)

## Preguntas Conceptuales
#### ¿Por qué hashear contraseñas?
Es una práctica de seguridad estándar, ya que si la base se filtra, o alguien accede sin permiso, la información sensible no se encuentra directamente disponible. Además, reduce la capacidad de los ataques de fuerza bruta, ya que cada intento de ataque debe incluir un proceso de hash intermedio, que vuelve el proceso menos eficaz.
#### Ventajas de usar SQLite en este proyecto.
Las ventajas de SQLite son:
* La velocidad y facilidad de implementación; no se requiere instalar ni configurar servidores por separado, simplemente se genera el archivo .db.
* Permite que uno se pueda enfocar mejor en el desarrollo de los endpoints y el código de la API, al no tener complejidad del lado de la base de datos.
* El archivo puede compartirse o facilmente o subirse a un repositrio sin problemas.
* Es una librería estandar y muy utilizada de python.
