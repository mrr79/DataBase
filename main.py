from verification import Verification

from where import Select
from insert import Insert
from delete import Delete
from  update import Update
from create import Create

if __name__ == "__main__":
    folder = '/home/mrr/Desktop/DataBase'  # Ruta de la carpeta principal
    verification = Verification(folder)
    query = Select(folder)
    delete_query = Delete(folder)
    update_query = Update(folder)
    create_query = Create()
    

    # Solicitar al usuario el nombre del archivo XML


    opcion = int(input("¿Qué acción deseas realizar? (0: CREATE, 1: SELECT/JOIN, 2: INSERT, 3: DELETE, 4: UPDATE): "))

    if opcion == 1:
        file_name = input("FROM (sin la extensión .xml): ") + ".xml"
        if verification.verify_file(file_name):
            query.execute_query(file_name)
    elif opcion == 2:
        file_insert= input("INSERT INTO: ")
        insert_query = Insert(file_insert)
        insert_query.execute_query(file_insert)
    elif opcion == 3:
        file_name = input(" DELETE FROM (sin la extensión .xml): ") + ".xml"
        if verification.verify_file(file_name):
            delete_query.execute_query(file_name)
    elif opcion == 4:
        file_name = input(" UPDATE ") + ".xml"
        if verification.verify_file(file_name):
            update_query.execute_query(file_name)
    elif opcion == 0:
        # Ejemplo de uso
        file_name = input("CREATE TABLE ")
        create_query.create(file_name)
        print("Carpeta y archivo XML creados exitosamente.")
    else:
        print("Opción inválida")
        
