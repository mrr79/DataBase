import os
import xml.etree.ElementTree as ET

class Select:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def execute_query(self, file_name, columns=None):
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)
        xml_file = os.path.join(folder_path, file_name)

        print("FOLDER NAME:", folder_name)
        print("FOLDER PATH:", folder_path)
        print("FILE NAME:", file_name)

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Obtener los elementos de la tabla
        #rows = root.findall('.//alumnos')
        rows = root.findall('.//' + folder_name)
        # Verificar si hay filas en el archivo XML
        if len(rows) == 0:
            print("No hay filas en el archivo XML.")
            return

        # Obtener los nombres de los atributos
        if columns is None:
            columns_input = input("Ingrese los nombres de los atributos separados por comas (deje en blanco para seleccionar todos): ")
            columns = [column.strip() for column in columns_input.split(',')] if columns_input else [child.tag for child in rows[0]]

        # Imprimir las filas seleccionadas
        for row in rows:
            values = [row.find(attribute).text for attribute in columns]
            print(values)
