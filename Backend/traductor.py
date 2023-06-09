
def morse_to_text(codigo_morse):
    """
    Convierte un código Morse en texto.

    :param codigo_morse: Código Morse a traducir.
    :type codigo_morse: str
    :return: Texto traducido.
    :rtype: str
    """
    codigo_morse = codigo_morse.strip()
    morse_a_texto = {
        '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e',
        '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j',
        '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o',
        '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
        '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y',
        '--..': 'z'
    }

    letras_morse = codigo_morse.split(' ') 

    texto_traducido = ''
    for letra in letras_morse:
        if letra in morse_a_texto:
            texto_traducido += morse_a_texto[letra]
        else:
            texto_traducido += '?'  # si no se reconoce la letra pone un ?

    return texto_traducido


#codigo_morse = '-- .- .-. .. .- -. .-'
#texto_traducido = morse_to_text(codigo_morse)
#print(texto_traducido)