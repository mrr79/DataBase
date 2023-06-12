import os
import xml.etree.ElementTree as ET
import re
import shutil

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

            attributes_str = ','.join(attributes)
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
            self.update_xml(file_name, xml_file, attributes_str)
            return file_name, attributes_str, xml_file, attributes_str

        else:
            # If no match is found, return None
            return None

    @staticmethod
    def update_xml(file_name, ruta_xml_original, attributes_str, ruta_local=None):
        print("                             estoy en UPDATE DENTRO  ")
        ruta_local = '/home/mrr/Desktop/DataBase/local'
        ruta_auxiliar = os.path.join(ruta_local, file_name)
        if not os.path.exists(ruta_auxiliar):
            os.makedirs(ruta_auxiliar)

        ruta_xml_modificado = os.path.join(ruta_auxiliar, 'productos.xml')
        shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

        tree = ET.parse(ruta_xml_modificado)
        root = tree.getroot()

        nuevo_ = ET.Element(file_name)

        attributes = attributes_str.split(',')  # Dividir los valores de atributos por coma

        for attribute_name in attributes:
            atributo = ET.SubElement(nuevo_, attribute_name)
            atributo.text = 'Nuevo producto en MARIANITAA'

        # Agregar el elemento 'nuevo_' al elemento raíz del árbol XML
        root.append(nuevo_)

        # Guardar los cambios en el archivo XML modificado
        tree.write(ruta_xml_modificado)

        respuesta = input("¿Deseas guardar el archivo modificado en el archivo original? (Y/N): ")

        if respuesta.upper() == "Y":
            # Copiar el archivo modificado a la ubicación del archivo original
            shutil.copyfile(ruta_xml_modificado, ruta_xml_original)
            print("El archivo modificado se ha guardado tanto en la ubicación original como en la carpeta 'Local'.")
        else:
            print("El archivo modificado se ha guardado únicamente en la carpeta 'Local'.")



