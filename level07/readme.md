# Level 07

## 🎯 Objectif

Exploiter une mauvaise gestion des variables d'environnement dans un binaire SUID afin d'usurper l'identité de l'utilisateur `flag07` et récupérer le précieux token (flag).

## 🐛 La Faille

En inspectant la racine du répertoire personnel (`ls -la`), on découvre un exécutable nommé `level07` possédant des permissions spécifiques :
`-rwsr-sr-x 1 flag07 level07 8805 Mar 5 2016 level07`

Le `s` à la place du traditionnel `x` indique la présence du **bit SUID** (Set-User-ID).

Un `ltrace ./level07` révèle que le programme récupère le contenu de la variable d'environnement `LOGNAME` via la fonction `getenv("LOGNAME")`, puis construit dynamiquement une commande système passée à la fonction `system()` sous la forme `/bin/echo <LOGNAME>`.

L'erreur critique ici est que la variable d'environnement est entièrement contrôlable par l'utilisateur local. L'absence de sanitisation permet de manipuler le flux d'exécution du shell invoqué par `system()`. C'est une vulnérabilité majeure appelée **Environment Command Injection** (Injection de commande via environnement).

export LOGNAME="; getflag"

## 🚀 Résolution

L'attaque consiste à modifier la variable `LOGNAME` en y injectant un délimiteur de commande (le point-virgule `;`) suivi de la commande `getflag`. Lors de l'exécution du binaire SUID, le shell exécutera d'abord `/bin/echo` (à vide), puis enchaînera immédiatement sur `getflag` avec les privilèges de `flag07`.

### Lancement de l'exploit

Depuis le dossier `resources` de votre machine hôte, lancez le script d'exploitation :

ssh level07@<IP> -p 4242 'bash' < exploit.sh
