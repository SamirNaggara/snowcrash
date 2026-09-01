# Level 01

## Objectif

Trouver le mot de passe de l'utilisateur `flag01` pour se connecter à son compte et récupérer le token (flag).

## La Faille

Ce niveau exploite une vulnérabilité liée à une ancienne gestion des mots de passe sous Unix/Linux : la **fuite d'informations via `/etc/passwd`**.

Historiquement, les mots de passe hachés (chiffrés) étaient stockés directement dans le fichier `/etc/passwd`. Le problème majeur est que ce fichier doit obligatoirement être lisible par tous les utilisateurs du système (droits de lecture globaux) pour que des programmes légitimes puissent mapper les UID aux noms d'utilisateurs. 
Aujourd'hui, les systèmes modernes déportent ces hachages dans le fichier `/etc/shadow` (lisible uniquement par `root`). Cependant, sur ce système mal configuré, le hash de l'utilisateur `flag01` est exposé en clair dans le fichier public.

## Résolution

Voici les étapes à suivre pour extraire ce hachage et le casser sur votre propre machine.

### 1. Extraire le hachage (VM cible)
Sur la machine cible, on lit le fichier des utilisateurs et on isole la ligne correspondant à notre cible :

```bash
grep "flag01" /etc/passwd
```
Le système renvoie la ligne de l'utilisateur. Le hachage se trouve en deuxième position, juste après le premier deux-points (:).

2. Craquer le mot de passe (Machine hôte)
On va utiliser John the Ripper, un outil célèbre de cassage de mots de passe.

On enregistre le hachage récupéré dans un fichier texte, puis on le hash

```Bash
    echo 42hDRfypTqqnw > hash.txt
    john hash.txt --show
```

