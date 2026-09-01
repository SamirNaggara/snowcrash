# Level 03

## Objectif

Exploiter un binaire vulnérable afin d'usurper l'identité de l'utilisateur `flag03` et récupérer le précieux token (flag).

## La Faille

En inspectant la racine du répertoire personnel (`ls -la`), on découvre un exécutable nommé `level03` possédant des permissions spécifiques :
`-rwsr-sr-x 1 flag03 level03 8627 Mar 5 2016 level03`

Le `s` à la place du traditionnel `x` indique la présence du **bit SUID** (Set-User-ID). Ce mécanisme permet à n'importe quel utilisateur qui lance ce programme de l'exécuter avec les privilèges de son propriétaire, ici `flag03`.

Lorsqu'on l'exécute, il affiche simplement `Exploit me`. Une analyse du comportement avec `ltrace ./level03` révèle l'utilisation de la fonction C `system()`, avec un appel du type :
`system("/usr/bin/env echo Exploit me");`

```bash
    ltrace ./level03
```

L'erreur critique ici est l'utilisation de `/usr/bin/env echo` (ou d'un chemin relatif). Le programme demande au système de chercher l'exécutable `echo` en parcourant dans l'ordre les dossiers listés dans la variable d'environnement `$PATH`. C'est une vulnérabilité majeure appelée **PATH Hijacking** (Détournement de PATH).

## Résolution

L'attaque consiste à créer un faux programme `echo` contenant notre commande malveillante, et à modifier notre variable `$PATH` pour que le système exécute notre faux programme au lieu du vrai.

Voici les étapes à suivre directement sur le terminal de la machine cible.

### 1. Créer le faux exécutable `echo`
Nous allons créer un script bash nommé `echo` dans le dossier temporaire `/tmp` (qui est accessible en écriture). Au lieu d'afficher du texte, ce script exécutera la commande `getflag` :

```bash
    echo "/bin/getflag" > /tmp/echo
    chmod +x /tmp/echo
```

2. Détourner la variable d'environnement PATH
Par défaut, le système cherche les commandes dans /usr/local/bin, /usr/bin, /bin, etc. Nous allons modifier temporairement la variable $PATH de notre session pour placer le dossier /tmp en tout premier :

```bash
    export PATH=/tmp:$PATH
```

3. Déclencher la faille
Il ne reste plus qu'à lancer le programme vulnérable :

```bash
    ./level03
```
Le flag s'affiche directement