import os
import shutil
import xml.etree.ElementTree as ET

# Ruta al archivo XML original
ruta_xml_original = '/home/mrr/Desktop/DataBase/productos/productos.xml'

# Ruta a la carpeta "Local"
ruta_local = '/home/mrr/Desktop/DataBase/local'

# Ruta a la carpeta "productos" dentro de "Local"
ruta_productos = os.path.join(ruta_local, 'productos')

# Verificar si la carpeta "productos" existe en la carpeta "Local", si no, crearla
if not os.path.exists(ruta_productos):
    os.makedirs(ruta_productos)

# Ruta al archivo XML modificado dentro de la carpeta "productos" en "Local"
ruta_xml_modificado = os.path.join(ruta_productos, 'productos.xml')

# Copiar el archivo XML original a la carpeta "productos" en "Local"
shutil.copyfile(ruta_xml_original, ruta_xml_modificado)

# Abrir el archivo XML modificado
tree = ET.parse(ruta_xml_modificado)
root = tree.getroot()

# Crear el nuevo elemento 'productos'
nuevo_producto = ET.Element('productos')

# Crear el elemento 'nombre' y establecer su texto
nombre = ET.SubElement(nuevo_producto, 'nombre')
nombre.text = 'Nuevo producto en MARIANITAA'

# Crear el elemento 'precio' y establecer su texto
precio = ET.SubElement(nuevo_producto, 'precio')
precio.text = '420'

# Agregar el nuevo producto al elemento raíz
root.append(nuevo_producto)

# Guardar los cambios en el archivo XML modificado
tree.write(ruta_xml_modificado)

# Preguntar al usuario si desea guardar el archivo modificado en el archivo original
respuesta = input("¿Deseas guardar el archivo modificado en el archivo original? (Y/N): ")

if respuesta.upper() == "Y":
    # Copiar el archivo modificado a la ubicación del archivo original
    shutil.copyfile(ruta_xml_modificado, ruta_xml_original)
    print("El archivo modificado se ha guardado tanto en la ubicación original como en la carpeta 'Local'.")
else:
    print("El archivo modificado se ha guardado únicamente en la carpeta 'Local'.")
