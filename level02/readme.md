# Level 02

## Objectif

Analyser un fichier de capture réseau (`.pcap`) pour extraire les identifiants de connexion de l'utilisateur `flag02` et récupérer le token.

## La Faille

Ce niveau met en évidence les dangers liés à l'utilisation de **protocoles non chiffrés** sur un réseau.

Toutes les communications transitent en clair. N'importe qui ayant accès au trafic réseau peut lire ces informations. La subtilité ici est que la capture enregistre les frappes brutes, y compris les touches de contrôle (comme les retours arrière), ce qui demande une interprétation des caractères hexadécimaux pour reconstituer le mot de passe final.

## Résolution

L'objectif est d'extraire la capture réseau de la machine cible pour l'analyser et la décoder sur notre propre machine.

### 1. Rapatrier le fichier de capture (Machine hôte)
Dans le répertoire personnel de l'utilisateur `level02` se trouve un fichier de capture de paquets : `level02.pcap`. Nous allons le télécharger sur notre ordinateur hôte via `scp` :

```bash
    scp -P 4242 level02@<IP_VM>:level02.pcap .
```

2. Analyser le trafic avec Wireshark (Machine hôte)
    - Ouvrez le fichier level02.pcap avec l'outil d'analyse réseau Wireshark.
    - La liste des paquets réseau s'affiche.
    - Faites un clic droit sur l'un des paquets contenant de la donnée.
    - Sélectionnez Suivre (Follow) -> Flux TCP (TCP Stream).
    - La saisie brute de l'utilisateur s'affiche.

3. Reconstituer le mot de passe
Si l'on regarde les données brutes (en basculant l'affichage Wireshark en mode Hexadécimal), on constate que l'utilisateur a fait des erreurs de frappe et utilisé la touche Retour Arrière (code hexadécimal 0x7f).

Pour simuler cette frappe et révéler le vrai mot de passe, utilisez le script Python fourni dans le dossier resources qui nettoie automatiquement les caractères d'effacement :

Bash
./resources/decode_pcap.py "ft_wandr...NDRel.L0L"
Le script interprète les retours arrière et renvoie : ft_waNDReL0L
