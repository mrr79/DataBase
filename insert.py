import os
import xml.etree.ElementTree as ET

class Insert:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def execute_query(self, file_name):
        print("Estoy en insert AAAAAAAAAAAAAAAAA")
       
        xml_file = os.path.join(self.folder_path, file_name+ ".xml")

        file_tree = ET.parse(xml_file)
        file_root = file_tree.getroot()
        file_rows = file_root.findall('.//' + file_name)

        print("File insert rows:", file_rows)
