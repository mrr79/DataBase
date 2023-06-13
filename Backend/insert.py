import os
import xml.etree.ElementTree as ET
import re
import shutil
import ast


class Insert:
    """
    Clase que representa una operación de inserción en una base de datos XML.
    """

    def __init__(self, folder_path):
        """
        Inicializa la clase de inserción.

        :param folder_path: Ruta de la carpeta de la base de datos.
        :type folder_path: str
        """
        self.folder_path = 'folder_path'

    def execute_query(self, input_insert, string_):
        """
        Ejecuta una consulta de inserción en la base de datos.

        :param input_insert: Consulta de inserción en formato "INSERT INTO table_name (attribute1, attribute2, ...) VALUES (value1, value2, ...);"
        :type input_insert: str
        :return: Información sobre la inserción realizada.
        :rtype: tuple
        """

        # Define the regular expression pattern to extract the file name and attributes
        pattern = r'(\w+)\s*\((.+)\)'

        # Find matches with the pattern in the input_insert string
        print("AAAAAA")
        matches = re.match(pattern, input_insert)

        if matches:
            print('ssssssssssssss')
            # Extract the file name and attributes
            file_name = matches.group(1)
            attributes = matches.group(2).split(',')
            attributes = [attr.strip() for attr in attributes]

            attributes_str = ','.join(attributes)
          

            # Construct the file path
            folder_name = re.sub(r'\W+', '', file_name)
            xml_file = os.path.join("C:/Users/henry/PycharmProjects/DataBase/Backend/disco", file_name, file_name + ".xml")
            print(xml_file)
            file_tree = ET.parse(xml_file)
            file_root = file_tree.getroot()
            file_rows = file_root.findall('.//' + file_name)

            #print("INSERT INTO ", file_rows)

            values_input = string_
            values_input = values_input.strip(';')
            values_list = [tuple(value.strip().strip('()').split(',')) for value in values_input.split('),(')]
            #print("Lista de tuplas:")
            #print(values_list)

            self.insert_xml(file_name, xml_file, attributes_str, values_list)
            return file_name, attributes_str, xml_file, attributes_str

        else:
            print('DDDDDDDDDD')

            # If no match is found, return None
            return None

    @staticmethod
    def insert_xml(file_name, ruta_xml_original, attributes_str, values_list, ruta_local=None):
        """
        Inserta valores en un archivo XML.

        :param file_name: Nombre del archivo.
        :type file_name: str
        :param ruta_xml_original: Ruta del archivo XML original.
        :type ruta_xml_original: str
        :param attributes_str: Cadena de atributos separados por comas.
        :type attributes_str: str
        :param values_list: Lista de tuplas con los valores a insertar.
        :type values_list: list
        :param ruta_local: Ruta de la carpeta local.
        :type ruta_local: str, optional
        """
        print("                             estoy en UPDATE DENTRO  ")
        #ruta_local = '/home/mrr/Desktop/DataBase/local'
        ruta_local = 'C:/Users/henry/PycharmProjects/DataBase/Backend/local'
        ruta_auxiliar = os.path.join(ruta_local, file_name)
        if not os.path.exists(ruta_auxiliar):
            os.makedirs(ruta_auxiliar)

        ruta_xml_modificado = os.path.join(ruta_auxiliar, file_name+".xml")
        shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

        tree = ET.parse(ruta_xml_modificado)
        root = tree.getroot()

        for value in values_list:
            nuevo_ = ET.Element(file_name)

            for i, attribute_name in enumerate(attributes_str.split(',')):
                atributo = ET.SubElement(nuevo_, attribute_name)
                atributo.text = str(value[i])

            root.append(nuevo_)
            print("se hizo")
            print(ruta_xml_modificado)

        # Guardar los cambios en el archivo XML modificado
        tree.write(ruta_xml_modificado)

        print("INSERT realizado correctamente")