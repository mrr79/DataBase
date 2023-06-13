import os
import xml.etree.ElementTree as ET
import re
import shutil
import ast

class Update:
    """
    Clase que representa una operación de actualizacion/modificacion en una base de datos XML.
    """
    def __init__(self, folder_path):
        """
        Inicializa una instancia de la clase Update.

        :param folder_path: Ruta de la carpeta donde se encuentran los archivos XML.
        :type folder_path: str
        """
        self.folder_path = folder_path

    def execute_query(self, file_name, string_, columns=None):
        """
        Ejecuta una consulta de actualización en un archivo XML.

        :param file_name: Nombre del archivo XML.
        :type file_name: str
        :param columns: Columnas a actualizar.
        :type columns: list[str] or None
        """
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)
        xml_file = os.path.join(folder_path, file_name)

        ruta_xml_original=folder_path+"/"+file_name

        words = string_.split()

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Obtener los elementos de la tabla
        rows = root.findall('.//' + folder_name)

        parts = string_.split("WHERE")
        condiciones = parts[1].strip()

        # Verificar si hay filas en el archivo XML
        if len(rows) == 0:
            print("No hay filas en el archivo XML.")
            return

        # Obtener los nombres de los atributos
        if columns is None:
            where_input = words[3]
            attribute_value_pairs = [pair.strip() for pair in where_input.split(',')]
            columns_input = [pair.split('=')[0].strip() for pair in attribute_value_pairs]
            text_input = [pair.split('=')[1].strip() for pair in attribute_value_pairs]
            if columns_input == ["*"]:
                columns = [child.tag for child in rows[0]]
            else:
                columns = [column.strip() for column in columns_input] if columns_input else [child.tag for child in rows[0]]

        #ruta_local = '/home/mrr/Desktop/DataBase/local'
        ruta_local = 'C:/Users/henry/PycharmProjects/DataBase/Backend/local'
        ruta_auxiliar = os.path.join(ruta_local, folder_name)
        if not os.path.exists(ruta_auxiliar):
            os.makedirs(ruta_auxiliar)

        ruta_xml_modificado = os.path.join(ruta_auxiliar, file_name)
        shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

        if len(words) > 4:
            answer = 'Y'
        else:
            answer = 'N'

        if answer.lower() == 'y':
            where_conditions = condiciones
            conditions = self.parse_conditions(where_conditions)
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        # Imprimir las filas seleccionadas
        for row in filtered_rows:
            values = [row.find(attribute) for attribute in columns]
            for value, text in zip(values, text_input):
                value.text = text
            #print([value.text for value in values])

        tree.write(ruta_xml_modificado)
        print("UPDATE exitoso")


    def parse_conditions(self, where_conditions):
        """
        Parsea las condiciones de la cláusula WHERE.

        :param where_conditions: Condiciones de la cláusula WHERE.
        :type where_conditions: str
        :return: Condiciones parseadas.
        :rtype: list[list[str]]
        """
        conditions = []
        condition_groups = re.split(r'\bOR\b', where_conditions)  # Separar las condiciones por "OR"
        for group in condition_groups:
            conditions_in_group = [condition.strip() for condition in re.split(r'\bAND\b', group)]  # Separar las condiciones por "AND"
            conditions.append(conditions_in_group)
        return conditions

    def filter_rows(self, rows, conditions):
        """
        Filtra las filas de acuerdo a las condiciones especificadas.

        :param rows: Filas a filtrar.
        :type rows: list[xml.etree.ElementTree.Element]
        :param conditions: Condiciones de filtrado.
        :type conditions: list[list[str]]
        :return: Filas filtradas.
        :rtype: list[xml.etree.ElementTree.Element]
        """
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