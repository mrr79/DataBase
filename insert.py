import os
import xml.etree.ElementTree as ET
import re

class Insert:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def execute_query(self, input_insert):
        print("Estoy en insert AAAAAAAAAAAAAAAAA")

        # Define the regular expression pattern to extract the file name and attributes
        pattern = r'(\w+)\s*\((.+)\)'

        # Find matches with the pattern in the input_insert string
        matches = re.match(pattern, input_insert)

        if matches:
            # Extract the file name and attributes
            file_name = matches.group(1)
            attributes = matches.group(2).split(',')
            attributes = [attr.strip() for attr in attributes]

            attributes_str = ', '.join(attributes)
            print(file_name)
            print(attributes)
            print("attributes string:", attributes_str)

            # Construct the file path
            folder_name = re.sub(r'\W+', '', file_name)
            xml_file = os.path.join(file_name, file_name + ".xml")

            file_tree = ET.parse(xml_file)
            file_root = file_tree.getroot()
            file_rows = file_root.findall('.//' + file_name)

            print("File insert rows:", file_rows)

            return file_name, attributes_str

        else:
            # If no match is found, return None
            return None

