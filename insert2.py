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

            values_input = input("Ingrese los valores en el formato '(Producto 1, 10.99), (Producto 2, 15.99), ...': ")
            #values_input = values_input.replace('(', '').replace(')', '')  # Eliminar paréntesis
            #values_list = [tuple(value.strip().split(',')) for value in values_input.split(',')]
            #values_list= "["+values_input+"]"
            values_list = list(values_input)
            print("SUPUESTA PERRA LISTA DE FKN TUPLAS")
            print (values_list)
            #self.insert_xml(file_name, xml_file, attributes_str,values_list)
            return file_name, attributes_str, xml_file, attributes_str

        else:
            # If no match is found, return None
            return None

    @staticmethod
    def insert_xml(file_name, ruta_xml_original, attributes_str,value, ruta_local=None):
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

        print("SSSSSSSSSSSSSUPUESTA PERRA LISTA DE FKN TUPLAS ABAJJO")
        print(value)

        for val in value:
            nuevo_ = ET.Element('nuevo')

            for i, attribute_name in enumerate(attributes):
                atributo = ET.SubElement(nuevo_, attribute_name)
                atributo.text = str(val[i])

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