# Level 04

## Objectif

Exploiter un script CGI vulnérable afin d'usurper l'identité de l'utilisateur `flag04` et récupérer le précieux token (flag).

## La Faille

En inspectant la racine du répertoire personnel (`ls -la`), on découvre un script Perl nommé `level04.pl` possédant des permissions spécifiques :
`-rwsr-sr-x 1 flag04 level04 152 Mar 5 2016 level04.pl`

Le `s` à la place du traditionnel `x` indique la présence du **bit SUID** (Set-User-ID). Cependant, par mesure de sécurité, le noyau Linux moderne ignore par défaut le bit SUID sur les scripts interprétés (Perl, Bash, Python...) lorsqu'ils sont lancés directement depuis le terminal.

En analysant le code via **`cat level04.pl`**, on découvre comment le script traite le paramètre `x` :
```perl
    #!/usr/bin/python
    # (Le code utilise CGI et récupère le paramètre 'x')
    print `echo $y 2>&1`;
```
L'erreur critique est l'utilisation des backticks (`) pour exécuter une commande système contenant la variable $y (qui prend la valeur de x) sans aucun nettoyage ni validation.

Puisque ce script est configuré comme un CGI accessible via un serveur web local sur le port 4747, et que ce serveur web s'exécute avec les privilèges de flag04, nous faisons face à une **Injection de Commande** (Command Injection) exploitable à distance (localement).

## Résolution
L'attaque consiste à envoyer une requête HTTP au serveur web local en injectant une sous-commande dans le paramètre d'URL x. Au lieu d'afficher simplement du texte, le serveur va évaluer et exécuter notre commande avec ses propres privilèges.

Voici l'unique étape à exécuter directement dans le terminal de la machine cible :

```Bash
curl 'localhost:4747/?x=$(getflag)'
```

Le flag apparait directement