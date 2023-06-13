import time

from Backend.verification import Verification
from Backend.where import Select
from Backend.insert import Insert
from Backend.delete import Delete
from Backend.update import Update
from Backend.create import Create
import os
import xml.etree.ElementTree as ET
import shutil
import random
import string
import re
import serial
from collections import Counter
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

from Backend.Huffman import encode_string, huffman_code_tree, make_tree
xml_folder = "C:/Users/henry/PycharmProjects/DataBase/Backend/local"  # Reemplaza con la ruta de tu carpeta existente


def perform_database_action(action_string):
    values_stringm = ""  # Variable para almacenar los valores

    #folder = '/home/mrr/Desktop/DataBase'
    values_string = ""  # Variable para almacenar los valores

    folder = 'C:/Users/henry/PycharmProjects/DataBase/Backend/disco'
    # Ruta de la carpeta principal
    verification = Verification(folder)
    query = Select(folder)
    delete_query = Delete(folder)
    update_query = Update(folder)
    create_query = Create()
    words = action_string.split()
    action = words[0]

    if action == 'FROM':
        file_name = words[1] + ".xml"
        if verification.verify_file(file_name):
            values_stringm = query.execute_query(file_name, action_string)
    elif action == 'INSERT':
        # Obtener la parte de la tabla y columnas
        start_index = action_string.index("(")  # Índice de inicio del paréntesis
        end_index = action_string.index(")")  # Índice de fin del paréntesis
        table_columns = action_string[action_string.index(" ", 7) + 1:start_index].strip() + " " + action_string[
                                                                                                   start_index:end_index + 1].strip()
        print(table_columns)

        parts = action_string.split("VALUES")
        datos = parts[1].strip()

        print(datos)

        file_insert= 'C:/Users/henry/PycharmProjects/DataBase/Backend'
        insert_query = Insert(table_columns)
        insert_query.execute_query(table_columns, datos)
    elif action == 'DELETE':
        file_name = words[2] + ".xml"
        if verification.verify_file(file_name):
            delete_query.execute_query(file_name, action_string)
    elif action == 'UPDATE':
        file_name = words[1] + ".xml"
        if verification.verify_file(file_name):
            update_query.execute_query(file_name, action_string)
    elif action == 'CREATE':
        file_name = input("CREATE TABLE ")
        #create_query.create(file_name)
        print("Carpeta y archivo XML creados exitosamente.")
    else:
        print("Opción inválida")
    return values_stringm

def crear_carpeta(nombre, atributos):
    Create.create_folder_with_xml(nombre, atributos)
    return "Archivo XML creado exitosamente"

def agregar_usuario_xml(usuario, correo, contrasena):
    # Cargar el archivo XML existente
    tree = ET.parse("C:/Users/henry/PycharmProjects/DataBase/Backend/usuarios.xml")
    root = tree.getroot()

    # Crear el nuevo elemento de usuario
    nuevo_usuario = ET.Element('usuario')
    nuevo_usuario.set('nombre', usuario)

    # Crear los subelementos de correo y contraseña
    correo_element = ET.SubElement(nuevo_usuario, 'correo')
    correo_element.text = correo

    # Comprimir la contraseña utilizando Huffman
    if "." in contrasena:
        contrasena = morse_to_text(contrasena)
    print(contrasena)
    freq = dict(Counter(contrasena))
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    encoded_contrasena = encode_string(contrasena, encoding)

    contrasena_element = ET.SubElement(nuevo_usuario, 'contrasena')
    contrasena_element.text = encoded_contrasena

    # Agregar el nuevo elemento de usuario al root
    root.append(nuevo_usuario)

    # Guardar los cambios en el archivo XML
    tree.write("C:/Users/henry/PycharmProjects/DataBase/Backend/usuarios.xml")

def verificar_credenciales(usuario, contrasena):
    arduino = serial.Serial('COM4', 9600)  # Reemplaza 'COM3' con tu puerto serie y 9600 con la velocidad de baudios correcta
    tree = ET.parse("C:/Users/henry/PycharmProjects/DataBase/Backend/usuarios.xml")
    root = tree.getroot()
    if "." in contrasena:
        contrasena = morse_to_text(contrasena)
    # Comprimir la contraseña utilizando Huffman
    freq = dict()
    for char in contrasena:
        freq[char] = freq.get(char, 0) + 1
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    encoded_password = encode_string(contrasena, encoding)

    for user in root.findall('usuario'):
        username = user.get('nombre')
        stored_password = user.find('contrasena').text

        if username == usuario and stored_password == encoded_password:
            time.sleep(2)
            arduino.write(b'1')
            arduino.close()
            return True
    time.sleep(2)
    arduino.write(b'2')
    arduino.close()
    return False


def create_folder(folder_name, folder_attributes):
    xml_root = ET.Element(folder_name)

    object_element = ET.SubElement(xml_root, folder_name[:-1])
    for attribute in folder_attributes:
        attribute_element = ET.SubElement(object_element, attribute)
        attribute_element.text = ''.join(random.choices(string.ascii_letters, k=5))

    xml_tree = ET.ElementTree(xml_root)
    xml_file_path = os.path.join(xml_folder, folder_name + ".xml")
    xml_tree.write(xml_file_path)

    return "Archivo XML creado exitosamente"

def merge_xml_files():
    # Obtener la lista de archivos XML en la carpeta de origen
    # Ruta de la carpeta XML_local
    local_folder = "C:/Users/henry/PycharmProjects/DataBase/Backend/local"
    # Ruta de la carpeta XML_disco
    disco_folder = "C:/Users/henry/PycharmProjects/DataBase/Backend/disco"
    shutil.rmtree(disco_folder)  # Elimina el directorio de destino y su contenido
    shutil.copytree(local_folder, disco_folder)
    return "Archivos XML fusionados exitosamente"

def read_xml_files():
    preloaded_folders = []

    for filename in os.listdir("C:/Users/henry/PycharmProjects/DataBase/Backend/disco"):
        if filename.endswith(".xml"):
            filepath = os.path.join("C:/Users/henry/PycharmProjects/DataBase/Backend/disco", filename)
            tree = ET.parse(filepath)
            root = tree.getroot()

            folder_name = root.tag
            folder_attributes = [child.tag for child in root[0]]

            folder = {
                "name": folder_name,
                "attributes": folder_attributes
            }

            preloaded_folders.append(folder)

    return preloaded_folders

def create_local_xml_files():
    # Ruta de la carpeta XML_local
    local_folder = "C:/Users/henry/PycharmProjects/DataBase/Backend/local"
    # Ruta de la carpeta XML_disco
    disco_folder = "C:/Users/henry/PycharmProjects/DataBase/Backend/disco"
    shutil.rmtree(local_folder)  # Elimina el directorio de destino y su contenido
    shutil.copytree(disco_folder, local_folder)
    return "Archivos XML copiados exitosamente"

def morse_to_text(codigo_morse):
    """
    Convierte un código Morse en texto.

    :param codigo_morse: Código Morse a traducir.
    :type codigo_morse: str
    :return: Texto traducido.
    :rtype: str
    """
    codigo_morse = codigo_morse.strip()
    morse_a_texto = {
        '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e',
        '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j',
        '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o',
        '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
        '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y',
        '--..': 'z'
    }

    letras_morse = codigo_morse.split(' ')

    texto_traducido = ''
    for letra in letras_morse:
        if letra in morse_a_texto:
            texto_traducido += morse_a_texto[letra]
        else:
            texto_traducido += '?'  # si no se reconoce la letra pone un ?

    return texto_traducido

# Call the function to execute the database action
#action_string = "INSERT INTO alumnos (nombre,nota) VALUES (juan,197),(mariana,22222),(henry,12444)"
#result = perform_database_action(action_string)
#print(result)
#agregar_usuario_xml("1", "henryda@gmail.com", "-- .- .-. .. .- -. .-")
