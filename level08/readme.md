# Level 08

## 🎯 Objectif

Exploiter une validation de nom de fichier naïve dans un binaire SUID afin de lire un fichier protégé appartenant à `flag08` et récupérer le précieux token (flag).

## 🐛 La Faille

En inspectant la racine du répertoire personnel (`ls -la`), on découvre deux éléments clés :

- Un exécutable nommé `level08` possédant le **bit SUID** (`-rwsr-s---+ 1 flag08 level08`).
- Un fichier `token` contenant le secret mais uniquement lisible par `flag08` (`-rw------- 1 flag08 flag08`).

Lorsqu'on tente de lire le fichier via le binaire (`./level08 token`), le programme renvoie explicitement `You may not access 'token'`. Cela indique que le binaire implémente une fonction de sécurité restrictive (type `strstr`) vérifiant uniquement si le nom de l'argument contient textuellement la chaîne "token".

L'erreur critique ici est de baser la sécurité d'accès sur une simple vérification textuelle du chemin fourni plutôt que sur l'identité ou le descripteur réel du fichier ciblé. C'est une vulnérabilité majeure permettant un contournement par **Symbolic Link** (Lien symbolique).

ln -s /home/user/level08/token /tmp/bypass

## 🚀 Résolution

L'attaque consiste à créer un lien symbolique (un pointeur) dans un répertoire accessible en écriture (`/tmp/`), en lui donnant un nom arbitraire ne contenant pas le mot interdit. En passant ce lien au binaire SUID, la vérification textuelle réussit, et le programme ouvre le fichier pointé avec les privilèges de `flag08`.

### Lancement de l'exploit

Depuis le dossier `resources` de votre machine hôte, lancez le script d'exploitation :

ssh level08@<IP> -p 4242 'bash' < exploit.sh
