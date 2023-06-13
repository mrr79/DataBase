import serial
from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect
import re
from Backend import Server
from Backend.Server import agregar_usuario_xml, verificar_credenciales, create_folder, merge_xml_files, read_xml_files, \
    create_local_xml_files, perform_database_action, crear_carpeta
from flask import Flask, request
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)
xml_folder = 'C:\\Users\\henry\\Documents\\Flask\\Frontend\\XML_local'  # Reemplaza con la ruta de tu carpeta existente

# Ruta para mostrar el formulario de selección de login o register
@app.route('/', methods=['GET'])
def index():
    return render_template('login_or_register.html')

# Ruta para mostrar el formulario de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Aquí puedes realizar la lógica de registro, como validar los datos y guardar el usuario en la base de datos

        success_message = '¡Registro exitoso! Email: {}, Usuario: {}'.format(email, username)
        agregar_usuario_xml(username, email, password)
        return render_template('register.html', success_message=success_message)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar las credenciales
        if verificar_credenciales(username, password):
            return redirect('/dashboard')  # Redirigir a la página de destino si las credenciales son válidas

        error_message = 'Credenciales incorrectas'

    return render_template('login.html', error_message=error_message)

# Ruta para el dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    create_local_xml_files()
    preloaded_folders = read_xml_files()
    # Variables para controlar el contenido dinámico
    content = None
    folders = ['Carpeta 1', 'Carpeta 2', 'Carpeta 3']

    if request.method == 'POST':
        button = request.form['button']

        if button == 'crear_carpeta':
            # Lógica para crear una nueva carpeta
            content = '¡Carpeta creada exitosamente!'
        elif button == 'ejecutar_script':
            # Lógica para ejecutar el script
            content = 'Script ejecutado correctamente'
        elif button == 'hacer_commit':
            # Lógica para hacer commit de los cambios
            content = 'Cambios guardados'

    return render_template('dashboard.html', folders=folders, content=content, preloaded_folders=preloaded_folders)

@app.route("/create_folder", methods=["POST"])
def create_folder_route():
    folder_data = request.get_json()
    folder_name = folder_data["name"]
    folder_attributes = folder_data["attributes"]

    result = crear_carpeta(folder_name, folder_attributes)
    return result


@app.route("/commit", methods=["POST"])
def commit():
    merge_xml_files()
    return render_template("commit_success.html")

# Ruta para recibir el código del script y verificar si contiene "SELECT"
@app.route('/execute_script', methods=['POST'])
def execute_script():
    code = request.form['code']

    output_message = ""

    output_message = perform_database_action(code)

    return output_message

# Configura el puerto serial con la ubicación correcta y la velocidad apropiada


if __name__ == '__main__':
    app.run(debug=True)