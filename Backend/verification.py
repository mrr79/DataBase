import os

class Verification:
    """
    Clase que representa una operación de verficacion para la autenticacion de la existencia del archivo XML.
    """
    def __init__(self, folder_path):
        """
        Inicializa una instancia de la clase Verification.

        :param folder_path: Ruta de la carpeta donde se encuentran los archivos XML.
        :type folder_path: str
        """
        self.folder_path = folder_path

    def verify_file(self, file_name):
        """
        Verifica la existencia de un archivo XML en una carpeta específica.

        :param file_name: Nombre del archivo XML.
        :type file_name: str
        :return: True si el archivo existe, False de lo contrario.
        :rtype: bool
        """

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

        return True
        
