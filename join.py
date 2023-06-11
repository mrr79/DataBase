import os

class Join:
    def perform_join(rows1, rows2, attribute):
        join_rows = []
        for row1 in rows1:
            for row2 in rows2:
                if rows_match(row1, row2, attribute):
                    join_rows.append(row1)
                    break
        return join_rows
#este es un comentario de prueba
    def rows_match(row1, row2, attribute):
        value1 = row1.find(attribute).text
        value2 = row2.find(attribute).text
        return value1 == value2

    # Obtener el archivo y las filas para realizar el JOIN
    def get_join_rows(folder_path, join_file, join_folder_name, filtered_rows):
        join_folder_path = os.path.join(folder_path, join_folder_name)
        join_xml_file = os.path.join(join_folder_path, join_file + ".xml")

        join_tree = ET.parse(join_xml_file)
        join_root = join_tree.getroot()

        join_rows = join_root.findall('.//' + join_folder_name)

        return filtered_rows
