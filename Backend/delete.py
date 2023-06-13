import os
import xml.etree.ElementTree as ET
import re
import shutil
import ast
import time

import serial


class Delete:
    """
    Clase que permite borrar filas de un archivo XML.
    """

    def __init__(self, folder_path):
        """
        Inicializa la clase `Delete`.

        :param folder_path: Ruta de la carpeta que contiene el archivo XML.
        :type folder_path: str
        """
        self.folder_path = folder_path

    def execute_query(self, file_name, string_, columns=None, contador=0):
        """
        Ejecuta una consulta para borrar filas en el archivo XML.

        :param file_name: Nombre del archivo XML.
        :type file_name: str
        :param columns: Lista de nombres de columnas a considerar, por defecto None.
        :type columns: list, optional
        :param contador: Contador para llevar la cuenta de las filas borradas, por defecto 0.
        :type contador: int, optional
        """
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)
        xml_file = os.path.join(folder_path, file_name)

        ruta_xml_original=folder_path+"/"+file_name

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Obtener los elementos de la tabla
        rows = root.findall('.//' + folder_name)

        words = string_.split()
        parts = string_.split("WHERE")
        condiciones = parts[1].strip()

        # Verificar si hay filas en el archivo XML
        if len(rows) == 0:
            print("No hay filas en el archivo XML.")
            return

        # Obtener los nombres de los atributos
        if columns is None:
            columns = [child.tag for child in rows[0]]

        #ruta_local = '/home/mrr/Desktop/DataBase/local'
        ruta_local = 'C:/Users/henry/PycharmProjects/DataBase/Backend/local'

        ruta_auxiliar = os.path.join(ruta_local, folder_name)
        if not os.path.exists(ruta_auxiliar):
            os.makedirs(ruta_auxiliar)

        ruta_xml_modificado = os.path.join(ruta_auxiliar, file_name)
        shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

        # Imprimir las filas seleccionadas
        if len(words) > 3:
            answer = 'Y'
        else:
            answer = 'N'
        if answer.lower() == 'y':
            where_conditions = condiciones
            conditions = self.parse_conditions(where_conditions)
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        # borarr las filas seleccionadas
        for row in filtered_rows:
            root.remove(row)
            contador = contador+1

        if contador == 1:
            print("DELETE hecho en 1 instancia")
        elif contador > 1:
            arduino = serial.Serial('COM4', 9600)  # Reemplaza 'COM3' con tu puerto serie y 9600 con la velocidad de baudios correcta
            time.sleep(2)
            arduino.write(b'3')
            arduino.close()
            print("DELETE hecho en varias instancias")

        tree.write(ruta_xml_modificado)
        #               AQUI YA SE BORRO, ENTONCES AQUI VA LA SENAL PARA EL ARDUINO.
        

    def parse_conditions(self, where_conditions):
        """
        Analiza las condiciones de la cláusula WHERE.

        :param where_conditions: Condiciones especificadas en la cláusula WHERE.
        :type where_conditions: str
        :return: Condiciones analizadas.
        :rtype: list
        """
        conditions = []
        condition_groups = re.split(r'\bOR\b', where_conditions)  # Separar las condiciones por "OR"
        for group in condition_groups:
            conditions_in_group = [condition.strip() for condition in re.split(r'\bAND\b', group)]  # Separar las condiciones por "AND"
            conditions.append(conditions_in_group)
        return conditions

    def filter_rows(self, rows, conditions):
        """
        Filtra las filas según las condiciones especificadas.

        :param rows: Filas a filtrar.
        :type rows: list
        :param conditions: Condiciones de filtrado.
        :type conditions: list
        :return: Filas filtradas.
        :rtype: list
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