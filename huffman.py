from collections import Counter
class NodeTree(object):
    """
    Clase que representa un nodo en el árbol de código Huffman.
    """

    def __init__(self, left=None, right=None):
        """
        Inicializa un nodo del árbol de código Huffman.

        :param left: Nodo izquierdo.
        :type left: NodeTree, optional
        :param right: Nodo derecho.
        :type right: NodeTree, optional
        """
        self.left = left
        self.right = right

    def children(self):
        """
        Devuelve los nodos hijos.

        :return: Tupla con los nodos izquierdo y derecho.
        :rtype: tuple
        """
        return self.left, self.right

    def __str__(self):
        """
        Representación en cadena del nodo.

        :return: Cadena que representa el nodo.
        :rtype: str
        """
        return self.left, self.right


def huffman_code_tree(node, binString=''):
    '''
    Función para encontrar el código Huffman.
    '''
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))
    return d


def make_tree(nodes):
    """
    Crea el árbol de código Huffman a partir de los nodos.

    :param nodes: Lista de tuplas (carácter, frecuencia).
    :type nodes: list
    :return: Nodo raíz del árbol de código Huffman.
    :rtype: NodeTree
    """
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]

def encode_string(string, encoding):
    """
    Codifica una cadena utilizando el código Huffman.

    :param string: Cadena a codificar.
    :type string: str
    :param encoding: Diccionario de codificación.
    :type encoding: dict
    :return: Cadena codificada.
    :rtype: str
    """
    encoded_string = ""
    for char in string:
        encoded_string += encoding[char]
    return encoded_string

if __name__ == '__main__':
    string = 'HolaaamellamoHenry'
    freq = dict(Counter(string))
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    for i in encoding:
        print(f'{i} : {encoding[i]}')
    encoded_string = encode_string(string, encoding)
    print("Palabra codificada:", encoded_string)