import os
import xml.etree.ElementTree as ET
import re

class Join:

    """def imprimir_valores(self, filtered_rows):
        #print("                        ESTO ESTA EN JOIN")
        for row in filtered_rows:
            #print(row)"""

    def join_files(self, file1, file2):
        
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

        #print(xml_file1)
        #print(xml_file2)
        '''print("Esta es la carpeta que tenía el select:", filtered_folder) #imprime propietarios
        print("Estos son los que están filtrados que tenía el select:", filtered_rows)
        print("#######################################################################################################")
        print("fle 2 rows:", file2_rows)
        print("fle 1 rows:", file1_rows)
        print("#######################################################################################################")'''

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
        value1 = row1.findtext(attr1)
        value2 = row2.findtext(attr2)
        return value1 == value2

