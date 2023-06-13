import os
import xml.etree.ElementTree as ET
import re
from Backend.join import Join
class Select:
    """
    Clase que ejecuta consultas SELECT en archivos XML, seleccionar columnas, aplicar condiciones WHERE y realizar JOINs con otros archivos XML.
    """
    def __init__(self, folder_path):
        """
        Inicializa una instancia de la clase Select.

        :param folder_path: Ruta de la carpeta donde se encuentran los archivos XML.
        :type folder_path: str
        """
        self.folder_path = folder_path

    def execute_query(self, file_name, string_, columns=None):
        """
        Ejecuta una consulta SELECT en un archivo XML.

        :param file_name: Nombre del archivo XML.
        :type file_name: str
        :param columns: Lista de nombres de columnas a seleccionar, por defecto None (selecciona todas las columnas).
        :type columns: list, optional
        """
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)
        xml_file = os.path.join(folder_path, file_name)
        values_string = ""  # Variable para almacenar los valores

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
            select_part = string_.split("SELECT")[1]  # Obtener la parte después de "SELECT"
            where_part = select_part.split("WHERE")[0]  # Obtener la parte antes de "WHERE"
            selected_columns = where_part.strip()
            columns_input = selected_columns
            if columns_input.strip() == "*":
                columns = [child.tag for child in rows[0]]
            else:
                columns = [column.strip() for column in columns_input.split(',')] if columns_input else [child.tag for child in rows[0]]
                #print("----------------------------------------------")
                #print(columns_input)
        if "WHERE" in string_:
            answer = 'Y'
        else:
            answer = 'N'
        # Imprimir las filas seleccionadas
        if answer.lower() == 'y':
            where_index = string_.find("WHERE") + len("WHERE")  # Índice de inicio de la parte deseada
            join_index = string_.find("JOIN")  # Índice de fin de la parte deseada

            if join_index != -1:
                # Si se encuentra JOIN, extraer la parte entre WHERE y JOIN
                selected_part = string_[where_index:join_index].strip()
            else:
                # Si no se encuentra JOIN, extraer la parte desde WHERE hasta el final
                selected_part = string_[where_index:].strip()

            where_conditions = selected_part
            conditions = self.parse_conditions(where_conditions)
            filtered_rows = self.filter_rows(rows, conditions)
        else:
            filtered_rows = rows

        if "JOIN" in string_:
            answer_join = 'Y'
        else:
            answer_join = 'N'
        if answer_join.lower() == 'y':

            # Obtener la parte entre JOIN y ON
            join_index = string_.index("JOIN") + len("JOIN")  # Índice de inicio de la palabra siguiente
            next_word = string_[join_index:].strip().split()[0]
            join_file = next_word
            join_folder_name = join_file
            join_folder_path = os.path.join(self.folder_path, join_folder_name)
            join_xml_file = os.path.join(join_folder_path, join_file + ".xml")

            join_tree = ET.parse(join_xml_file)
            join_root = join_tree.getroot()

            join_rows = join_root.findall('.//' + join_folder_name)

            join_objeto = Join()

            on_index = string_.index("ON") + len("ON")  # Índice de inicio de la parte deseada
            on_clause = string_[on_index:].strip()

            join_filtered_rows = join_objeto.perform_join(folder_name,filtered_rows, on_clause)

            for row in join_filtered_rows:
                #imprimo las que cumplieron con lo del JOIN
                values = [row.find(attribute).text for attribute in columns]
                values_string += ",".join(values) + "\n"  # Agregar valores a la cadena
                print(values)
        else:
            for row in filtered_rows:
                values = [row.find(attribute).text for attribute in columns]
                values_string += ",".join(values) + "\n"  # Agregar valores a la cadena
                print(values)
        return values_string

    def parse_conditions(self, where_conditions):
        """
        Analiza las condiciones WHERE de la consulta y las separa en grupos.

        :param where_conditions: Condiciones WHERE de la consulta.
        :type where_conditions: str
        :return: Lista de condiciones separadas en grupos.
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