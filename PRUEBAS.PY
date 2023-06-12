import os

def create(input_str):
    # Dividir el input en nombre y atributos
    partes = input_str.split(" (")
    nombre = partes[0]
    atributos = partes[1][:-2].split(",")  # Remover el punto y coma final
    
    # Crear la carpeta con el nombre especificado
    os.makedirs(nombre, exist_ok=True)
    
    # Crear el contenido del archivo XML
    contenido = f"<{nombre}>\n"
    contenido += f"\t<{nombre}>\n"  # Agregar etiqueta adicional <estudiantes>
    for atributo in atributos:
        contenido += f"\t\t<{atributo}></{atributo}>\n"
    contenido += f"\t</{nombre}>\n"
    contenido += f"</{nombre}>"  # Cerrar etiqueta <estudiantes> adicional
    
    # Crear el archivo XML dentro de la carpeta
    archivo = open(f"{nombre}/{nombre}.xml", "w")
    archivo.write(contenido)
    archivo.close()

# Ejemplo de uso
input_str = input("CREATE TABLE ")
create(input_str)
print("Carpeta y archivo XML creados exitosamente.")
