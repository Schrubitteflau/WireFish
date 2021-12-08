# WireFish : Cahier des charges

Ydays labo SSI, année 2021/2022
25/11/2021

## Groupe

Benjamin DELSOL & Antoine SANSON
M1 cybersécurité

## Nom du projet
WireFish

## Présentation
L'objectif va être de réaliser un programme qui va permettre d'intercepter le trafic passant par une interface précise de la machine. Il faudra ensuite décoder et analyser le trafic couche par couche en remontant le modèle OSI pour fournir le plus d'informations possibles. Ce programme sera en ligne de commandes et acceptera différents paramètres pour configurer son fonctionnement, comme l'interface à utiliser, le niveau de détail à afficher (payloads HTTP uniquement ? paquets et détails IP ? trames Ethernet ?), mais également des filtres éventuels à appliquer : IP, protocole applicatif, etc.
  
## Technologies utilisées
Le langae python ainsi que la bibliothèque **scapy** seront utilisés

## Différentes étapes à suivre
1. Dans un premier temps, revoir rapidement les concepts et la syntaxe du Python
2. En parallèle, réviser ses cours de réseau
4. Se familiariser avec la bibliothèque scapy pour comprendre l'étendue de ce qu'il est possible de faire, ainsi que ses limitations
5. Réaliser un prototype se contentant d'intercepter les trames Ethernet et d'afficher des informations élémentaires à leur propos : adresse MAC source et de destination
6. Remonter les couches du modèle OSI pour gérer la couche réseau (IPv4), la couche transport (TCP, UDP), puis la couche application en implémentant certains protocoles très communs comme HTTP ou FTP

## Fonctionnalités bonus
Une fois l'outil en ligne de commande fonctionnel, de nombreuses perspectives d'améliorations s'offrent à nous :
- Prendre en charge plus de protocoles applicatifs
- Permettre d'écouter le trafic d'un processus en particulier et non plus d'une interface, ce qui serait un premier pas vers un outil d'analyse de comportement sur le réseau
- Rendre l'outil interactif, c'est-à-dire faire en sorte qu'il accepte des entrées au clavier alors qu'il est déjà en fonctionnement, par exemple pour modifier à la volée la configuration appliquée
- Implémenter une interface graphique simple

## Difficultés
- Allier nos compétences en réseau et en développement. En effet, il faudra être prêt à se former efficacement dans ces deux domaines afin que le projet aboutisse.
- En termes d'organisation, il nous faudra bien nous répartir les tâches en termes de documentation et de développement, ce qui mène à la prochaine difficulté
- L'organisation du code devra être impeccable, afin que l'amélioration continue de l'outil par les implémentations successives de nouvelles couches et protocoles puisse se faire de manière fluide et efficace 
- Ne pas voir trop loin : il peut être facile de s'imaginer des fonctionnalités qui pourraient s'avérer très utiles, mais il faut rester simple au début et avancer étape par étape, pour empiler les briques fondamentales sans griller les étapes, tout en conservant un projet fonctionnel et présentable à chaque étape

## Difficultés techniques
- La bibliothèque scapy semble très complète et est utilisée par de nombreux outils, mais une courbe d'apprentissage sera ajoutée
- Bien appréhender les notions de réseau sera un prérequis qu'il ne faudra pas prendre à la légère 
