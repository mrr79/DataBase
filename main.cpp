#include <iostream>
#include "Huffman.h"

/*
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
}*/

#include <iostream>
#include "tinyxml2.h"

using namespace tinyxml2;

bool evaluarConsulta(int edad, int carnet) {
    // Implementa la lógica adecuada para evaluar las condiciones
    return (edad > 20 || carnet > 2345);
}

int main() {
    XMLDocument doc;
    if (doc.LoadFile("/home/mrr/Desktop/DataBase/estudiantes.xml ") == XML_SUCCESS) {
        XMLElement* root = doc.FirstChildElement("estudiantes");
        if (root) {
            const char* query = "edad > 20 OR carnet > 2345";
            XMLElement* estudiante = root->FirstChildElement("estudiante");
            while (estudiante) {
                const char* nombre = estudiante->FirstChildElement("nombre")->GetText();
                const char* apellido = estudiante->FirstChildElement("apellido")->GetText();
                int edad = std::stoi(estudiante->FirstChildElement("edad")->GetText());
                int carnet = std::stoi(estudiante->FirstChildElement("carnet")->GetText());

                // Ejecutar la consulta
                if (evaluarConsulta(edad, carnet)) {
                    std::cout << "Nombre: " << nombre << ", Apellido: " << apellido << std::endl;
                }

                estudiante = estudiante->NextSiblingElement("estudiante");
            }
        }
    } else{
        std::cout << "No se abrio" << std::endl;
    }

    return 0;
}
