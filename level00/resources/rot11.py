#!/usr/bin/env python3
import sys

def rot11(text):
    result = ""
    for char in text:
        if char.islower():
            # Décale de 11 positions dans l'alphabet minuscule
            result += chr((ord(char) - ord('a') + 11) % 26 + ord('a'))
        elif char.isupper():
            # Décale de 11 positions dans l'alphabet majuscule
            result += chr((ord(char) - ord('A') + 11) % 26 + ord('A'))
        else:
            # Ne modifie pas les caractères spéciaux (chiffres, ponctuation...)
            result += char
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(rot11(sys.argv[1]))
    else:
        print("Usage: python3 rot11.py <texte_a_dechiffrer>")