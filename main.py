from verification import Verification

from where import Select
from insert import Insert

if __name__ == "__main__":
    folder = '/home/mrr/Desktop/DataBase'  # Ruta de la carpeta principal
    verification = Verification(folder)
    query = Select(folder)
    

    # Solicitar al usuario el nombre del archivo XML


    opcion = int(input("¿Qué acción deseas realizar? (1: SELECT/JOIN, 2: INSERT): "))

    if opcion == 1:
        file_name = input("FROM (sin la extensión .xml): ") + ".xml"
        if verification.verify_file(file_name):
            query.execute_query(file_name)
    elif opcion == 2:
        file_insert= input("INSERT INTO: ")
        insert_query = Insert(file_insert)
        insert_query.execute_query(file_insert)
              
    else:
        print("Opción inválida")
        
