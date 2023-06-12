import os
import xml.etree.ElementTree as ET
import re
import shutil
import ast

class Update:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def execute_query(self, file_name, columns=None):
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)
        xml_file = os.path.join(folder_path, file_name)

        ruta_xml_original=folder_path+"/"+file_name

        print("FOLDER NAME:", folder_name)
        print("FOLDER PATH:", folder_path)
        print("FILE NAME:", file_name)

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Obtener los elementos de la tabla
        rows = root.findall('.//' + folder_name)

        # Verificar si hay filas en el archivo XML
        if len(rows) == 0:
            print("No hay filas en el archivo XML.")
            return

        # Obtener los nombres de los atributos
        if columns is None:
            where_input = input("SET ")
            attribute_value_pairs = [pair.strip() for pair in where_input.split(',')]
            columns_input = [pair.split('=')[0].strip() for pair in attribute_value_pairs]
            text_input = [pair.split('=')[1].strip() for pair in attribute_value_pairs]
            if columns_input == ["*"]:
                columns = [child.tag for child in rows[0]]
            else:
                columns = [column.strip() for column in columns_input] if columns_input else [child.tag for child in rows[0]]

        ruta_local = '/home/mrr/Desktop/DataBase/local'
        ruta_auxiliar = os.path.join(ruta_local, folder_name)
        if not os.path.exists(ruta_auxiliar):
            os.makedirs(ruta_auxiliar)

        ruta_xml_modificado = os.path.join(ruta_auxiliar, file_name)
        shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

        answer = input("¿agregar WHERE? (Y/N): ")
        if answer.lower() == 'y':
            where_conditions = input("WHERE")
            conditions = self.parse_conditions(where_conditions)
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        # Imprimir las filas seleccionadas
        for row in filtered_rows:
            values = [row.find(attribute) for attribute in columns]
            for value, text in zip(values, text_input):
                value.text = text
            print([value.text for value in values])

        tree.write(ruta_xml_modificado)

        respuesta = input("¿Deseas guardar el archivo modificado en el archivo original? (Y/N): ")

        if respuesta.upper() == "Y":
            # Copiar el archivo modificado a la ubicación del archivo original
            shutil.copyfile(ruta_xml_modificado, ruta_xml_original)
            print("El archivo modificado se ha guardado tanto en la ubicación original como en la carpeta 'Local'.")
        else:
            print("El archivo modificado se ha guardado únicamente en la carpeta 'Local'.")


    def parse_conditions(self, where_conditions):
        conditions = []
        condition_groups = re.split(r'\bOR\b', where_conditions)  # Separar las condiciones por "OR"
        for group in condition_groups:
            conditions_in_group = [condition.strip() for condition in re.split(r'\bAND\b', group)]  # Separar las condiciones por "AND"
            conditions.append(conditions_in_group)
        return conditions

    def filter_rows(self, rows, conditions):
        filtered_rows = []
        for row in rows:
            match = False
            for condition_group in conditions:
                group_match = True
                for condition in condition_group:
                    if '=' in condition:
                        column, value = condition.split('=', 1)
                        operator = '='
                    elif '<' in condition:
                        column, value = condition.split('<', 1)
                        operator = '<'
                    elif '>' in condition:
                        column, value = condition.split('>', 1)
                        operator = '>'
                    else:
                        # Si no se especifica un operador, se asume igualdad
                        column, value = condition, None
                        operator = '='

                    cell_value = row.find(column).text
                    if operator == '=' and cell_value != value:
                        group_match = False
                        break
                    elif operator == '<' and not (cell_value is not None and float(cell_value) < float(value)):
                        group_match = False
                        break
                    elif operator == '>' and not (cell_value is not None and float(cell_value) > float(value)):
                        group_match = False
                        break

                if group_match:
                    match = True
                    break

            if match:
                filtered_rows.append(row)

        return filtered_rows