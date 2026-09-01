# Level 05

## 🎯 Objectif

Exploiter une tâche planifiée (Cron) mal sécurisée afin d'usurper l'identité de l'utilisateur `flag05` et récupérer le précieux token (flag).

## 🐛 La Faille

En constatant l'alerte de nouveau message à la connexion, un simple `cat /var/mail/level05` trahit l'existence d'une tâche Cron système s'exécutant toutes les deux minutes avec les privilèges de la cible :
`*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05`

Un second `cat /usr/sbin/openarenaserver` montre que ce script va exécuter aveuglément (via `bash -x`) puis supprimer absolument tout fichier déposé dans le dossier `/opt/openarenaserver/*`.

L'erreur critique ici est que ce répertoire est accessible en écriture pour notre utilisateur actuel, ce qui permet d'y injecter n'importe quel script qui sera exécuté nativement avec les privilèges de `flag05`. C'est une vulnérabilité majeure appelée **Arbitrary Code Execution** (Exécution de code arbitraire).

echo "/bin/getflag > /tmp/token_level05.txt" > /opt/openarenaserver/exploit.sh

## 🚀 Résolution

L'attaque consiste à déposer un script malveillant dans le dossier surveillé pour forcer la tâche Cron à exécuter `getflag` en arrière-plan, puis à récupérer le résultat redirigé dans un fichier temporaire dans `/tmp`.

### Lancement de l'exploit

Depuis le dossier `resources` de votre machine hôte, lancez le script d'exploitation :

ssh level05@<IP> -p 4242 'bash' < exploit.sh
