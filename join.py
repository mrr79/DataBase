class Join:
    def imprimir_valores(self, filtered_rows,):
        print("                        ESTO ESTA EN JOIN")
        for row in filtered_rows:
            print(row)

    def perform_join(self, rows1, rows2):
        join_rows = []
        for row1 in rows1:
            for row2 in rows2:
                if self.rows_match(row1, row2):
                    join_rows.append(row1)
                    break
        return join_rows

    def rows_match(self, row1, row2):
        # Aquí debes definir la lógica para determinar si las filas coinciden en ambas tablas.
        # Puedes comparar los valores de los atributos u otras condiciones que apliquen a tu caso particular.
        # Devuelve True si las filas coinciden, False en caso contrario.
        # Ejemplo básico: Compara el valor de un atributo en ambas filas
        attribute = "carnet"  # Reemplaza "columna" por el nombre del atributo que deseas comparar
        value1 = row1.find(attribute).text
        value2 = row2.find(attribute).text
        return value1 == value2