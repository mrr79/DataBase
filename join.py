import os
import xml.etree.ElementTree as ET
import re

class Join:
    """
    Clase que representa una operación de unión en una base de datos XML.
    """

    def join_files(self, file1, file2):
        """
        Realiza la unión de dos archivos XML.

        :param file1: Nombre del primer archivo.
        :type file1: str
        :param file2: Nombre del segundo archivo.
        :type file2: str
        :return: Información sobre los archivos y las filas de datos.
        :rtype: tuple
        """
        folder1_path = os.path.join(self.folder1_path, file1)
        xml_file1 = os.path.join(folder1_path, file1 + ".xml")

        file1_tree = ET.parse(xml_file1)
        file1_root = file1_tree.getroot()
        file1_rows = file1_root.findall('.//' + file1)

        folder2_path = os.path.join(self.folder2_path, file2)
        xml_file2 = os.path.join(folder2_path, file2 + ".xml")

        file2_tree = ET.parse(xml_file2)
        file2_root = file2_tree.getroot()
        file2_rows = file2_root.findall('.//' + file2)

        return folder1_path, folder2_path, file1_rows, file2_rows

    def perform_join(self, filtered_folder, filtered_rows):
        """
        Realiza la operación de unión en la base de datos.

        :param filtered_folder: Carpeta filtrada.
        :type filtered_folder: str
        :param filtered_rows: Filas filtradas.
        :type filtered_rows: list
        :return: Filas unidas.
        :rtype: list
        """
        attributes = input("ON ")
        attribute1, attribute2 = attributes.split('=')
        file1, attr1 = attribute1.split('.')
        file2, attr2 = attribute2.split('.')

        self.folder1_path = ""
        self.folder2_path = ""
        self.xml_file1=""
        self.xml_file2=""
        self.file1_tree = ""
        self.file1_root = ""
        self.file1_rows = ""

        self.file2_tree = ""
        self.file2_root = ""
        self.file2_rows = ""

        folder1_path, folder2_path, file1_rows, file2_rows = self.join_files(file1, file2)

        

        if filtered_folder==file1:
            #print("ESTE ARRIBA")
            join_rows = []
            for row1 in filtered_rows:
                for row2 in file2_rows:
                    if self.rows_match(row1, row2, attr1, attr2):
                        join_rows.append(row1)
                        break
            return join_rows
        
        elif filtered_folder==file2:
            #print("ESTE ABAjo")
            join_rows = []
            for row1 in filtered_rows:
                for row2 in file1_rows:
                    if self.rows_match(row2, row1, attr1, attr2):
                        join_rows.append(row1)
                        break
            return join_rows
        
        
        else:
            print("NO SE PUEDE HACER JOIN")

    def rows_match(self, row1, row2, attr1, attr2):
        """
        Compara dos filas de datos para determinar si coinciden en los atributos dados.

        :param row1: Primera fila de datos.
        :type row1: Element
        :param row2: Segunda fila de datos.
        :type row2: Element
        :param attr1: Atributo de la primera fila.
        :type attr1: str
        :param attr2: Atributo de la segunda fila.
        :type attr2: str
        :return: True si las filas coinciden en los atributos dados, False en caso contrario.
        :rtype: bool
        """
        value1 = row1.findtext(attr1)
        value2 = row2.findtext(attr2)
        return value1 == value2

