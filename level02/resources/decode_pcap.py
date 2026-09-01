#!/usr/bin/env python3
import sys

def parse_keystrokes(raw_data):
    password = []
    for char in raw_data:
        # Wireshark affiche les retours arrière sous forme de points '.' dans son aperçu ASCII.
        # On intercepte donc le '.', le '\x7f' (DEL) et le '\x08' (Backspace).
        if char in ('.', '\x7f', '\x08'):
            if password:
                password.pop() # Efface la dernière lettre ajoutée
        else:
            password.append(char) # Ajoute la lettre valide
            
    return "".join(password)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(parse_keystrokes(sys.argv[1]))
    else:
        default_payload = "ft_wandr...NDRel.L0L"
        print(f"[*] Aucun argument fourni. Test avec la chaîne Wireshark copiée :")
        print(f"[-] Saisie copiée : {default_payload}")
        print(f"[+] Résultat      : {parse_keystrokes(default_payload)}")