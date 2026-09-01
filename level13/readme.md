# Level 13

## Objectif

Contourner une vérification d'identité (User ID) codée en dur dans un binaire, en manipulant son exécution en direct à l'aide du débogueur GDB.

## La Faille

À la racine se trouve l'exécutable `level13`. Lorsqu'on le lance normalement, il échoue et affiche :
`UID 2013 started us but we we expect 4242`

Le programme utilise la fonction système `getuid()` pour vérifier l'identifiant de la personne qui le lance. Sous Linux, l'utilisateur `level13` a l'UID `2013`. Comme il n'est pas possible de changer son UID sans privilèges administrateur (root), il est impossible d'exécuter le programme de manière légitime pour satisfaire la condition.

La "faille" exploitée ici est la capacité de manipuler le flux d'exécution et la mémoire d'un programme à la volée grâce à un débogueur, afin de falsifier les valeurs retournées par le système.

## Résolution

La stratégie consiste à lancer le programme sous le contrôle de GDB (GNU Debugger), d'intercepter l'appel à la fonction `getuid()`, et de forcer la fonction à renvoyer `4242` au lieu de l'UID réel.

### Manipulation avec GDB

1. Lancez le binaire avec le débogueur :

```bash
	gdb ./level13
```

Posez un point d'arrêt (breakpoint) pour mettre le programme en pause exactement au moment où il fera appel à la fonction getuid :

Extrait de code

```bash
	(gdb) b getuid
	(gdb) run
	(gdb) return (int)4242
	(gdb) continue
```
