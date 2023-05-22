//
// Created by mrr on 21/05/23.
//

#ifndef DATABASE_HUFFMAN_H
#define DATABASE_HUFFMAN_H



#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <string>

// Estructura de nodo para el árbol de Huffman
struct HuffmanNode {
    char data;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(char data) : data(data), left(nullptr), right(nullptr) {}
};

// Función para decodificar el código Morse utilizando el árbol de Huffman
std::string decodeMorse(const std::string& morseCode, const HuffmanNode* root);

// Función para construir el árbol de Huffman utilizando el archivo de codificación Morse
HuffmanNode* buildHuffmanTree(const std::string& morseCodeFile);



#endif //DATABASE_HUFFMAN_H
