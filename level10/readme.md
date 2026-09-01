# Level 10

## 🎯 Objectif

Exploiter une vulnérabilité de type **TOCTOU** : Time-Of-Check to Time-Of-Use dans un binaire SUID pour lire un fichier protégé par des permissions strictes.

## 🐛 La Faille

L'exécutable `level10` est un binaire SUID appartenant à `flag10`. Il attend deux arguments : un fichier et une adresse IP hôte, et envoie le contenu du fichier sur le réseau via le port 6969.

En analysant le binaire avec `ltrace`, on observe un flux d'exécution vulnérable :

1. **Time-Of-Check** : Le programme appelle `access()` pour vérifier si l'utilisateur courant (`level10`) a le droit de lire le fichier fourni.
2. **Délai réseau** : Le programme effectue des opérations de socket (connexion au port 6969).
3. **Time-Of-Use** : Le programme appelle `open()` pour lire le fichier et l'envoyer sur le réseau.

La faille réside dans le fait que la validation des droits (`access`) est séparée de l'action (`open`). Comme le programme est SUID, `open()` utilise les privilèges de `flag10`, mais `access()` ne vérifie que les droits de `level10`.

## 🚀 Résolution

La stratégie est de forcer une "course" (Race Condition) en faisant varier le chemin du fichier entre le moment de la vérification et celui de l'ouverture.

### 1. Préparation du serveur de réception

Dans un terminal, on lance un serveur `netcat` pour capturer le contenu du fichier envoyé par le binaire :

# nc -lk 6969

### 2. L'attaque "Bait and Switch"

Dans deux autres terminaux, on lance simultanément deux boucles :

- Terminal A (Le commutateur de lien) :
  Cette boucle fait basculer sans cesse un lien symbolique /tmp/swap entre un fichier autorisé (dummy) et le fichier cible interdit (token).

# while true; do touch /tmp/dummy; ln -fs /tmp/dummy /tmp/swap; ln -fs /home/user/level10/token /tmp/swap; done

- Terminal B (L'exécuteur de binaire) :
  Cette boucle tente d'ouvrir /tmp/swap à toute vitesse.

- while true; do ./level10 /tmp/swap 127.0.0.1 > /dev/null 2>&1; done

Dès que la course est gagnée (lorsque access() vérifie /tmp/dummy et qu'immédiatement après, open() lit /tmp/swap pointant vers token), le contenu du fichier token apparaît dans le premier terminal.

ssh flag10@<IP> -p 4242

# Mot de passe : <TOKEN_RECUPERE>
