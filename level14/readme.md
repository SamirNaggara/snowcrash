# Level 14

## Objectif

S'attaquer directement au binaire central du système, `/bin/getflag`, en contournant ses protections anti-débogage pour usurper l'identité de l'utilisateur final et récupérer le dernier token.

## La Faille

L'objectif est de cibler `/bin/getflag` lui-même.

Le fonctionnement de `getflag` repose sur la vérification de l'UID (User ID) de la personne qui l'exécute, via la fonction système `getuid()`. Il contient tous les tokens du jeu en dur et affiche celui qui correspond à l'UID appelant. L'UID cible pour ce dernier niveau est celui de `flag14`, soit `3014`.

Pour empêcher l'usurpation via un débogueur (comme au niveau 13), le développeur a intégré une protection anti-débogage : au lancement, le programme appelle la fonction `ptrace`.
Sous Linux, un processus ne peut être tracé que par un seul débogueur à la fois. Si `ptrace` renvoie `-1`, le programme déduit qu'il est déjà sur écoute (par GDB), affiche `You should not reverse this`, et quitte.

La vulnérabilité réside dans le fait que, tout comme `getuid()`, la fonction de protection `ptrace()` peut elle-même être interceptée et modifiée en vol par GDB.

## Résolution

La stratégie consiste à réaliser une double interception dans GDB : désactiver le bouclier (`ptrace`), puis falsifier la carte d'identité (`getuid`).

### Manipulation avec GDB

Lancez le binaire cible dans le débogueur :

```bash
	gdb /bin/getflag
```

Posez des points d'arrêt (breakpoints) pour mettre le programme en pause afin de désactiver la protection anti-débogage, puis pour falsifier l'identité en renvoyant l'UID 3014 :

```bash
	(gdb) b ptrace
	(gdb) b getuid
	(gdb) run
	(gdb) return (int)0
	(gdb) continue
	(gdb) return (int)3014
	(gdb) continue
``
```
