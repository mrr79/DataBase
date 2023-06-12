import os

class Verification:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def verify_file(self, file_name):
        folder_name = file_name.split('.')[0]
        folder_path = os.path.join(self.folder_path, folder_name)

        # Verificar si la carpeta existe
        if not os.path.isdir(folder_path):
            print(f"La carpeta {folder_name} no existe.")
            return False

        # Verificar si el archivo XML existe dentro de la carpeta
        xml_file = os.path.join(folder_path, file_name)
        if not os.path.isfile(xml_file):
            print(f"No se encontró el archivo {file_name} en la carpeta {folder_name}.")
            return False

        #print ("si esta la carpeta")
        return True
        
