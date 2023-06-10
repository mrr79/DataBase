from verification import Verification

from where import Select

if __name__ == "__main__":
    folder = '/home/mrr/Desktop/DataBase'  # Ruta de la carpeta principal
    verification = Verification(folder)
    query = Select(folder)

    # Solicitar al usuario el nombre del archivo XML
    file_name = input("FROM (sin la extensión .xml): ") + ".xml"

    # Verificar la existencia del archivo y ejecutar la consulta
    if verification.verify_file(file_name):
        query.execute_query(file_name)
        