# 3

outil en CLI
expliquer brièvement le projet
environnement, cadre de travail permettant de développer des bouts de code (modules) spécialisés ayant pour but d’extraire des données sensibles (tokens, username/password, fichiers transférés, etc.) du trafic réseau intercepté

à la base : analyse de réseau, mais finalement le projet a changé de trajectoire
expliquer pq nom

# 4

expérimentations : voir les données sensibles échangées sur réseau perso

TI : machine compromise -> analyse du trafic pour progresser et récolter données intéressantes
[+] wirefish passif sur le réseau
[-] environnement nécessaire pour fonctionner : pyinstaller envisagé mais pas top
[-] droits admin

mitm :
[+] pertinent car fait gagner du temps (outil qui peut être lancé en fond)
[+] outil installé sur machine attaquante : pas de pb d’env

# 5

avant toute chose, on a fait un état de l’art des outils les plus connus effectuant de la capture et de l’analyse de trafic réseau, on va donc rapidement
vous parler de 3 logiciels connus (sauf peut-être le dernier) :

Wireshark : interface graphique simple, mais qui peut devenir complexe en utilisant fonctionnalités poussées, nombreuses fonctionnalités poussées comme le traitement de VoIP
possibilité de le scripter en Lua, mais plutôt dans l’objectif de faire des tests/POC avant d’intégrer la fonctionnalité dans le projet, en C++

tcpdump : en CLI, disponible nativement sur bcp de distributions Linux, fonctionnalités - poussées que Wireshark
permet notamment d’afficher ou d’enregistrer à l’écran le trafic réseau et des interfaces spécifiées en appliquant des filtres

NetworkMiner : moins connu, outil d’analyse forensique réseau, utilisé pour capturer le réseau ou extraire des données diverses, comme des fichiers transférés sur
différents protocoles comme HTTP, FTP, SMB, SMTP => se rapproche + de ce qu’on veut faire
-> nous a donné idée du module

on s’est rendu compte qu’il n’y avait pas vraiment d’outil qui reprend strictement l’idée de notre projet (concept de modules), donc création de qqc = valeur ajoutée

# 7

outil en CLI. 1er paramètre = nom de l’action, détermine les autres paramètres attendus et donne la main à l’action correspondante
après avoir fait des vérif sur les paramètres

- show-interfaces : affiche l’ensemble des interfaces réseau disponibles, avec des détails comme l’adresse MAC ou l’adresse IPv4 associée

- print-packets : écouter une ou plusieurs interfaces et affiche des informations élémentaires sur les paquets en ligne de console (filtrage possible)
-> inutile à part pour faire genre jui un hacker, vérif si outil fonctionne bien

- sniff-data : analyser le trafic en temps réel et d’en extraire les données sensibles à l’aide des modules activés

# 8

1. écoute des interfaces spécifiées
2. pour chaque paquet, on le transmet à chaque module activé qui ne doit pas le modifier
3. traitement du paquet par les modules à l’aide (ou non) de fonctionnalités de bases fournies par notre outil
  a. packet_analyse : extraire données ou interpréter payload des paquets, lorsque Scapy ne fournit pas les fonctionnalités
  b. misc : divers
  c. AbstractBaseModule : classe mère de tous les modules
4. attente du prochain paquet 

# 9

qu’est ce qu’un module ? comment un module est-il représenté dans le code ?

dire que c’est simplement une classe nommée module, qui implémente les champs abstraits de AbstractBaseModule, pour l’instant il s’agit seulement de la méthode
on_receive_packet()

pour charger un module, on se base sur son nom qui est un chemin d’import python (dossiers séparés par un point), importe dynamiquement,
instancie et c’est parti !

expliquer que AbstractBaseModule embarque des méthodes qui permettent de faire un retour à l’utilisateur : écriture de fichier, log dans la console

# 11

affiché code source car module le + court et permet d’expliquer comment créer un module
et code très explicite, même si jamais fait de python

expliquer brièvement code source et expliquer que créer module = simple, et on veut que ce soit simple

On voit que cette classe hérite de AbstractBaseModule et implémente tous les champs abstraits requis, ici seulement la méthode on_receive_packet()
FTPPacketParser a été développé dans le cadre de notre outil, et on voit que ça permet de rendre le code tout de suite plus compréhensible et
tourné vers le “quoi faire” plutôt que le “comment faire” : en tout cas pour des tâches simples

# 12

module + complexe que précédent car : 3 points du diapo

# 13

ceci est un exemple de cas où le client télécharge un fichier file.txt depuis le serveur en utilisant le mode passif

il a fallu implémenter cette logique pour pouvoir correctement intercepter les fichiers transférés dans un sens comme dans l’autre

# 14

lorsqu’on reçoit un paquet, on vérifie s’il s’agit d’une requête ou réponse HTTP

en fonction du résultat, on va chercher des données intéressantes dans la requête ou réponse et on les affiche à l’écran
ces données sont donc des tokens d’authentification ou des cookies (en-têtes), ou bien le corps de requêtes post permettant
d’accéder aux données de formulaire

# 15

lorsqu’on reçoit un paquet, on vérifie s’il s’agit d’une requête ou réponse HTTP

en fonction du résultat, on va chercher des données intéressantes dans la requête ou réponse et on les affiche à l’écran
ces données sont donc des tokens d’authentification ou des cookies (en-têtes), ou bien le corps de requêtes post permettant
d’accéder aux données de formulaire

voici une partie du code de ce module, juste à des fins d’illustration, mais il est franchement simple à comprendre et donc pas besoin
de passer du temps à l’expliquer

# 16

on se s’intéresse qu’au corps des réponses HTTP, et on utilise l’en-tête Content-Type pour obtenir le type du fichier transmis
si le content-type ne fait pas partie des types à ignorer, alors le fichier est copié. par exemple, on ne s’intéresse pas aux fichiers
.css ou aux fichiers de police de caractère

nous avons un problème lorsque la taille du fichier est trop importante pour que celui-ci soit transmis dans un seul paquet (ce qui
représente malheureusement la majorité des fichiers), mais il s’agit là du dernier module en date, qui n’a pas eu le temps d’être peaufiné
de plus, le lien entre la réponse et la requête n’est pas effectué, ce qui fait qu’on récupère des fichiers sans connaître la requête d’origine,
et donc le nom du fichier par exemple

# 17

python :
- langage interprété : pas besoin de compiler des trucs qui dépendent de la machine et portabilité
- syntaxe claire et concise : bon ratio de qtt de code / fonctionnalité, donc permet de programmer trucs complexes en peu de lignes
- écosystème : énormément de bibliothèques existent, pour presque tout. Avec les bonnes bibliothèques, on peut créer des outils spécifiques en peu de code et de temps.
- cyber : c’est pour toutes ces raisons que ce langage est apprécié dans le domaine de la cybersécurité

scapy :
- traitement de paquet en python : programme et bibliothèque peut être utilisé comme programme avec shell interactif de scapy, ou importé comme module Python
qui permet d’effectuer du traitement et de la création de paquet en Python
- syntaxe simple : en 1 ligne de code, on peut écouter une interface réseau, ou bien créer un paquet personnalisé en paramétrant chaque couche du modèle TCP/IP
- flexibilité : fournit des fonctions de manipulation de paquet, et bien d’autres, sans se préoccuper de ce qu’on en fait. Par exemple, on peut créer des paquets donc le payload est invalide et les émettre sur le réseau
- à jour : de nouvelles versions sortent régulièrement et des améliorations sont donc apportées en continu

# 19

Perte, ou non-capture de paquets : qd beaucoup de trafic d’un coup, sur un délai court, certains paquets ne sont pas capturés par Scapy
problèmes d’optimisation avec certaines configuration d’après forums. Ici, l’impact est que le module ftp.transfer_files ne fonctionne pas correctement
si des fichiers relativement volumineux sont transférés, (à partir de 1Mo environ)
utilisation de la libpcap = configuration dans Scapy => résout partiellement le pb mais des soucis subsistent

Méthodologie : par rapport à l’architecture du projet, il n’est pas facile, au sein d’un module, d’écrire la logique du protocole applicatif ciblé, étant
donné qu’à l’origine ça a vraiment été pensé pour permettre l’analyse des paquets uns à uns. Du coup on arrive rapidement à du code pas très lisible
et sujet à des bugs si les fonctionnalités dans Wirefish ne sont pas suffisantes. Le module ftp.transfer_files est un bon exemple.

Limites d’un module : quand s’arrête un module ? on peut être tenté de repartir d’un module existant et de l’améliorer pour se baser sur le code déjà
existant, alors qu’un module devrait être spécialisé. Au final, ça rejoint un peu le problème de méthodologie pusiqu’on se retrouve à programmer
un module à rallonge qui apprend à comprendre le protocole applicatif ciblé, et il devient en quelque sorte un « client muet »

# 20

stocker logs : rediriger logs vers un fichier à part, mais pourrait être fait avec le terminal qui exécute le programme

fichier de configuration : rendre les différents modules paramétrables à l’aide d’un fichier de configuration au format texte facile à lire et à éditer, donc format YAML intéressant
Une utilité pourrait être, par exemple, d’indiquer la taille maximum des fichiers à enregistrer localement, ou bien de spécifier quelles extensions ignorer : par exemple pour ftp.transfer_files
on pourrait dire de ne sauvegarder que les .zip

optimisation : mettre en place un système qui ne rend pas l’exécution des modules bloquants : utilisation de threads ?
permettre aussi aux modules d’indiquer quand ils doivent être appelés, sous quelles conditions, car là chaque paquet est transmis à chaque module et c’est vrm pas efficace
cela éviterait de faire des vérifications dans le code des modules

lecture de fichiers de capture réseau : cette fonctionnalité semble très intéressante, puisque notre outil pourrait faire tous les traitements et utiliser les modules sur des captures réseau
déjà enregistrées. plus de problème de performance ou de perte de paquet. En cas de crash, pas de perte potentielle de données sensibles car elles se trouvent tjrs dans la capture.
En plus, wirefish pourrait être utilisé dans d’autres domaines, comme potentiellement des CTFs.
Si jamais on devait continuer le développement de wirefish, cette fonctionnalité serait la première ajoutée.

# 22

Le choix de ces technos c’est aussi fait pour maximiser nôtre valeur à l’embauche : car avoir une expérience en Python et en capture et manipulation de paquets avec Scapy pourraient peser dans la balance si on souhaite continuer à faire de la technique

