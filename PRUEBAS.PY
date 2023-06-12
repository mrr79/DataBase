import os

def crear_carpeta_y_archivo(nombre, atributos):
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
nombre = input("Ingrese el nombre: ")
atributos = input("Ingrese los atributos separados por comas: ").split(",")

crear_carpeta_y_archivo(nombre, atributos)
print("Carpeta y archivo XML creados exitosamente.")
