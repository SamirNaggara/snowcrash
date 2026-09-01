#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def decrypt(filename):
    try:
        # Lecture du fichier binaire ("rb") pour gérer les caractères non imprimables
        with open(filename, 'rb') as f:
            content = f.read()
        
        # Suppression du saut de ligne final s'il a été ajouté par le système
        if content.endswith(b'\n'):
            content = content[:-1]

        decrypted = ""
        
        # Algorithme inverse : on boucle sur chaque caractère et son index
        for index, char in enumerate(content):
            # En Python 2, on utilise ord() pour obtenir la valeur numérique (ASCII)
            original_char_val = ord(char) - index
            
            # On reconvertit la valeur numérique en caractère
            decrypted += chr(original_char_val % 256)

        print(decrypted)

    except Exception as e:
        print("Erreur lors du déchiffrement :", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <fichier_token>")
    else:
        decrypt(sys.argv[1])