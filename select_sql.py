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
       # Obtener los nombres de los atributos
        if columns is None:
            columns_input = input("Ingrese los nombres de los atributos separados por comas (* para seleccionar todos): ")
            if columns_input.strip() == "*":
                columns = [child.tag for child in rows[0]]
            else:
                columns = [column.strip() for column in columns_input.split(',')] if columns_input else [child.tag for child in rows[0]]

        # Imprimir las filas seleccionadas
        answer = input("¿Desea agregar una cláusula WHERE? (Y/N): ")
        if answer.lower() == 'y':
            where_conditions = input("Ingrese las condiciones WHERE separadas por comas (columna=valor): ")
            conditions = [condition.strip() for condition in where_conditions.split(' AND ')] if where_conditions else []
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        # Imprimir las filas seleccionadas
        for row in filtered_rows:
            values = [row.find(attribute).text for attribute in columns]
            print(values)

    def filter_rows(self, rows, conditions):
        filtered_rows = []
        for row in rows:
            match = True
            for condition in conditions:
                column, value = condition.split('=')
                if row.find(column).text != value:
                    match = False
                    break
            if match:
                filtered_rows.append(row)
        return filtered_rows