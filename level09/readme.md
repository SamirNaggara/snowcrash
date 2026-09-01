# Level 09

## 🎯 Objectif

Faire de la rétro-ingénierie sur un algorithme de chiffrement maison afin de déchiffrer un fichier protégé et obtenir le mot de passe de l'utilisateur `flag09`.

## 🐛 La Faille

À la racine se trouvent un exécutable SUID `level09` et un fichier `token` contenant une suite de caractères non imprimables.

En testant l'exécutable avec une chaîne simple (`./level09 aaaa`), il retourne `abcd`. On en déduit la logique de l'algorithme (une simple addition basée sur l'index de position du caractère dans la chaîne) :
`Caractère_Chiffré = Caractère_Clair + Index`

Le fichier `token` contient donc le mot de passe de `flag09` chiffré avec cette méthode. L'erreur ici est d'ordre cryptographique : l'utilisation d'un algorithme "maison" trivial, symétrique et totalement réversible.

python decrypt.py /home/user/level09/token

## 🚀 Résolution

L'attaque nécessite l'utilisation conjointe d'un script de déchiffrement Python (`decrypt.py`) chargé d'inverser l'opération mathématique (`Caractère_Clair = Caractère_Chiffré - Index`), et d'un script d'exploitation Bash (`exploit.sh`).

### Préréquis : Transfert du script de déchiffrement

Depuis le dossier `resources` de votre machine hôte, commencez par envoyer le script Python dans le répertoire temporaire de la VM :

scp -P 4242 decrypt.py level09@<IP>:/tmp/decrypt.py
puis
ssh level09@192.168.1.153 -p 4242 'bash' < exploit.sh
