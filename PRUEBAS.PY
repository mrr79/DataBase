import ast

datos = ast.literal_eval(input("Ingrese los valores en el formato '(Producto 1, 10.99), (Producto 2, 15.99), ...': "))
lista_de_tuplas = list(datos)
print(lista_de_tuplas)
