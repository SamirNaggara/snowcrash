# SnowCrash

Un projet de sécurité offensive de l'école 42 : une machine volontairement vulnérable, quinze niveaux, et à chaque niveau une faille à trouver et à exploiter pour récupérer le mot de passe du niveau suivant. Du plus simple (fichier sensible oublié, chiffrement obsolète) au plus avancé (exploitation binaire, conditions de course, scripts SUID).

Ce dépôt rassemble, pour chaque niveau, une explication de la faille et la démarche de résolution.

## Ce qu'on y trouve

```text
level00/ à level14/
  readme.md    l'objectif, la faille, la résolution
  resources/   les scripts et fichiers utilisés (exploits, décodage, pcap...)
  flag         le token récupéré
```

## Notes

- La machine cible est un environnement de laboratoire de 42, hors ligne et sans lien avec un système réel. Les tokens n'ouvrent rien d'autre.
- Les techniques couvertes : divulgation d'information, chiffrements faibles (César, hashs obsolètes), analyse de trafic, scripts SUID mal écrits, conditions de course, exploitation mémoire.
- Publié comme trace d'apprentissage. Les écoles régénèrent leurs sujets, et l'intérêt est dans la méthode, pas dans les flags.
