import os
import xml.etree.ElementTree as ET

class Create:
    """
    Clase que permite crear una carpeta con un archivo XML dentro.
    """

    @staticmethod
    def create_folder_with_xml(nombre, atributos):
        """
        Crea una carpeta con un archivo XML dentro.

        :param nombre: Nombre de la carpeta y del archivo XML.
        :type nombre: str
        :param atributos: Lista de atributos para el archivo XML.
        :type atributos: list[str]
        """
        # Ruta de la ubicación de guardado
        ruta_guardado = r"C:\Users\henry\PycharmProjects\DataBase\Backend\local"

        # Crear la carpeta con el nombre especificado en la ruta deseada
        ruta_completa = os.path.join(ruta_guardado, nombre)
        os.makedirs(ruta_completa, exist_ok=True)

        # Crear el contenido del archivo XML
        contenido = f"<{nombre}>\n"
        contenido += f"\t<{nombre}>\n"  # Agregar etiqueta adicional <estudiantes>
        for atributo in atributos:
            contenido += f"\t\t<{atributo}></{atributo}>\n"
        contenido += f"\t</{nombre}>\n"
        contenido += f"</{nombre}>"  # Cerrar etiqueta <estudiantes> adicional

        # Crear el archivo XML dentro de la carpeta
        archivo = open(os.path.join(ruta_completa, f"{nombre}.xml"), "w")
        archivo.write(contenido)
        archivo.close()
