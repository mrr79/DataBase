//
// Created by mrr on 20/05/23.
//

#include "Huffman.h"


std::string decodeMorse(const std::string& morseCode, const HuffmanNode* root) {
    std::string result;
    const HuffmanNode* current = root;

    for (char c : morseCode) {
        if (c == '.') {
            current = current->left;
        } else if (c == '-') {
            current = current->right;
        } else if (c == ' ') {
            result += current->data;
            current = root;
        }
    }

    result += current->data;

    return result;
}

HuffmanNode* buildHuffmanTree(const std::string& morseCodeFile) {
    std::ifstream file(morseCodeFile);

    if (!file.is_open()) {
        std::cout << "No se pudo abrir el archivo " << morseCodeFile << std::endl;
        return nullptr;
    }

    std::map<char, std::string> morseCodeMap;

    std::string line;
    while (std::getline(file, line)) {
        char letter;
        std::string code;
        std::stringstream ss(line);
        ss >> letter >> code;
        morseCodeMap[letter] = code;
    }

    file.close();

    // Construir el árbol de Huffman a partir del mapa de codificación Morse
    HuffmanNode* root = new HuffmanNode('\0');

    for (const auto& pair : morseCodeMap) {
        char letter = pair.first;
        const std::string& code = pair.second;

        HuffmanNode* current = root;
        for (char c : code) {
            if (c == '.') {
                if (current->left == nullptr) {
                    current->left = new HuffmanNode('\0');
                }
                current = current->left;
            } else if (c == '-') {
                if (current->right == nullptr) {
                    current->right = new HuffmanNode('\0');
                }
                current = current->right;
            }
        }

        current->data = letter;
    }

    return root;
}