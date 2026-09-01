# Level 06

## 🎯 Objectif

Exploiter une vulnérabilité dans une expression régulière PHP afin d'usurper l'identité de l'utilisateur `flag06` et récupérer le précieux token (flag).

## 🐛 La Faille

En inspectant la racine du répertoire personnel (`ls -la`), on découvre un exécutable nommé `level06` possédant des permissions spécifiques :
`-rwsr-x---+ 1 flag06 level06 7503 Aug 30 2015 level06`

Le `s` à la place du traditionnel `x` indique la présence du **bit SUID** (Set-User-ID). Pour contourner le fait que Linux bloque le SUID sur les scripts interprétés, ce binaire sert d'enveloppe pour exécuter le script `level06.php` avec les privilèges de `flag06`.

Un simple `cat level06.php` trahit l'utilisation de la fonction `preg_replace` avec le modificateur dangereux et obsolète **/e** : `$a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);`.

L'erreur critique ici est que ce modificateur évalue la chaîne de remplacement comme du code PHP exécutable. En combinant la syntaxe d'interpolation complexe de PHP (`${...}`) et l'opérateur d'exécution système (les backticks), on peut injecter des commandes. C'est une vulnérabilité majeure appelée **Code Injection** (Injection de code).

echo '[x ${`getflag`}]' > /tmp/payload06

## 🚀 Résolution

L'attaque consiste à créer un fichier contenant notre payload structuré pour correspondre à la Regex attendue, puis à passer ce fichier en argument au binaire SUID pour déclencher l'exécution de code sous l'identité de `flag06`.

### Lancement de l'exploit

Depuis le dossier `resources` de votre machine hôte, lancez le script d'exploitation :

ssh level06@<IP> -p 4242 'bash' < exploit.sh
