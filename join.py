class Join:
    def perform_join(self, rows1, rows2):
        join_rows = []
        attribute = input("Ingrese el nombre del atributo que desea comparar: ")
        for row1 in rows1:
            for row2 in rows2:
                if self.rows_match(row1, row2, attribute):
                    join_rows.append(row1)
                    break
        return join_rows

    def rows_match(self, row1, row2, attribute):
        value1 = row1.find(attribute).text
        value2 = row2.find(attribute).text
        return value1 == value2
