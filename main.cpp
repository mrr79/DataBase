#include <iostream>
#include "Huffman.h"

int main() {
    // Construir el árbol de Huffman
    HuffmanNode* root = buildHuffmanTree("/home/mrr/Desktop/app/morse_code.txt");

    // Texto a decodificar
    std::string morseCode = "-- .- .-. .. .- -. .-";
    std::cout << "Texto decodificado: " << morseCode << std::endl;
    // Decodificar el texto utilizando el árbol de Huffman
    std::string decodedText = decodeMorse(morseCode, root);

    // Imprimir el resultado decodificado
    std::cout << "Texto decodificado: " << decodedText << std::endl;

    // Liberar la memoria del árbol de Huffman
    // ...

    return 0;
}