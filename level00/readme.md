# Level 00

## Objectif

Trouver le mot de passe de l'utilisateur `flag00` pour se connecter à son compte et récupérer le token (flag).

## La Faille

Ce niveau repose sur deux erreurs classiques d'administration système :

1. **Fichier sensible oublié (Information Disclosure) :** Un fichier (`/usr/sbin/john`) appartenant à l'utilisateur `flag00` a été laissé sur le système avec des droits de lecture ouverts à tous.
2. **Chiffrement obsolète :** Le mot de passe contenu dans ce fichier n'est pas haché de manière sécurisée, mais simplement obfusqué avec un très vieux chiffrement de César (décalage de 11 lettres, alias ROT11).

## Résolution

Voici les étapes à suivre entre la machine cible et la machine hôte.

### 1. Trouver le fichier caché
Sur la VM cible, on effectue une recherche sur tout le système (`/`) pour trouver les fichiers appartenant à l'utilisateur `flag00`. On redirige les erreurs (`2>/dev/null`) pour ne pas polluer l'affichage avec les dossiers auxquels on n'a pas accès :

# ssh level00@<IP> -p 4242  
-> password level00

```bash
    find / -user flag00 2>/dev/null
    cat /usr/sbin/john
```


3. Déchiffrer le mot de passe
De retour sur notre machine hôte, on utilise le script Python fourni dans le dossier resources pour appliquer la rotation inverse (ROT11) et retrouver le mot de passe en clair :


```bash
    ./rot11.py "cdiiddwpgswtgt"
```

On a le mot de passe, donc...
```bash
ssh flag00@10.0.2.16 -p 4242
```