import os
import xml.etree.ElementTree as ET
import re

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
        rows = root.findall('.//' + folder_name)

        # Verificar si hay filas en el archivo XML
        if len(rows) == 0:
            print("No hay filas en el archivo XML.")
            return

        # Obtener los nombres de los atributos
        if columns is None:
            columns_input = input("Ingrese los nombres de los atributos separados por comas (* para seleccionar todos): ")
            if columns_input.strip() == "*":
                columns = [child.tag for child in rows[0]]
            else:
                columns = [column.strip() for column in columns_input.split(',')] if columns_input else [child.tag for child in rows[0]]

        # Imprimir las filas seleccionadas
        answer = input("¿agregar WHERE? (Y/N): ")
        if answer.lower() == 'y':
            where_conditions = input("Ingrese las condiciones WHERE separadas por comas (columna=valor): ")
            conditions = self.parse_conditions(where_conditions)
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        # Imprimir las filas seleccionadas
        """for row in filtered_rows:
            values = [row.find(attribute).text for attribute in columns]
            print(values)"""
        

        answer_join = input("¿hacer JOIN (Y/N)? ")
        if answer_join.lower() == 'y':
            print("Mariana has el join")
            # Realizar el JOIN aquí
            print("JOIN realizado")
            print("Filas seleccionadas:")
            for row in filtered_rows:
                
                values = [row.find(attribute).text for attribute in columns]
                print(values)
        else:
            print("Filas seleccionadas:")
            for row in filtered_rows:
                values = [row.find(attribute).text for attribute in columns]
                print(values)

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