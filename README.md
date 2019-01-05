# GS15 - Rapport de projet

## Introduction

Dans le cadre de GS15, nous devions  coder plusieurs fonctions se liant à la cryptologie.
 Nous devions donc faire :
 - La fonction de chiffrement IDEA
 - Le protocole diffie helman
 - La fonction de hash sha-3
 - Une fonction de signature électronique 


## La fonction IDEA
Tout d'abord, nous avons développé les trois méthode de chiffrement demandé : ECB, CBC, PCBC. Nous avons fait en sorte que ses fonctions soient le plus le réutilisable possible. Il est possible de passer des différentes fonctions de chiffrement, choisir le nom du fichier d'entrée et de sortie, la taille des bloc, la clé qui sera utilisée et, si besoin, le vecteur initial.

Le chiffrement IDEA ne nous a pas posé de problème particulier.
Par contre, nous avons passé plusieurs jours à essayé d'inverser le processus de chiffrement. Hors, pour IDEA, nous inversons la clé pour déchiffrer en utilisant le même processus. Nous l'avons découvert en regardant les standards et plus particulièrement le site suivant : http://www.quadibloc.com/crypto/co040302.htm

En vérifiant différent code trouvé sur internet, nous avons confirmé que nous devons inverser la clé pour déchiffrer. Nous nous sommes inspiré d'un code existant pour l'intégrer dans notre projet.

Dans le cadre du projet, si la clé donné est plus grand que 16 octets, nous ne prenons que les 16 premiers octets. 

## Le protocole Diffie Hellman
Nous avons utilisé le principe des groupes de Schnorr pour générer les nombres premier. Nous savons que d’après les standards, les nombres premier à utilisé sont déterminé. Pour autant, pour l'exercice académique, nous avons mis le plus d'aléatoire possible dans les différentes fonctions.
De plus, pour l'exercice, nous avons mis la clé privée avec la clé publique lors de l'écriture de la clé dans un fichier, ce qui ne doit pas du tout être fais dans une implémentation autre qu'académique.

Dans notre cas d'étude, nous ne pouvons que "être" Alice, et nous pouvons demander une clé de communication à Bob, avec notre clé.
C'est cette clé que nous utilisons pour chiffrer les fichiers.

## Sha-3

## La signature électronique
Pour la fonction électronique, nous avons décidé d'implémenter DSA (*Digital Signature Algorithm*). C'est un algorithme open source du temps où RSA était breveté.

Nous l'avons développé par ce que nous pouvions utiliser les mêmes fonctions développées pour Diffie hellman et de réfléchir sur un autre algorithme que RSA.

Dans un premier temps, nous avons découpé la génération d'un groupe de Schnorr en deux fonctions. La première générée q et p, et la seconde trouvée le générateur g dans Z_q et Z_p. Cependant, lors de la signature, nous ne trouvons pas de générateur dans Z_q et Z_p en même temps. En regroupant les deux fonctions, nous avons pu résoudre ce problème. Le souci vient sûrement d'un mauvais passage d'argument entre les deux fonctions.


# How To

La structure du projet:

- src : Le dossier où se trouve tous les fichiers source
- keys : Le dossier où tous les clés seront enregistré
- sig : Le dossier ou toutes les signatures DSA seront enregistré

## Les fichiers sources
Nous pouvons trouver 7 fichiers python. Chaque fichier peut être appelé pour tester les fonctions associées au fichier, excepté le fichier crypto_utils.py:

- ***crypto_utils*** : un fichier contenant des fonctions support tel que les méthodes de chiffrement par bloc ou le test de miller-rabin.
- ***diffie_hellman*** : fichier définissant les fonctions associées au protocole diffie hellman. En l'appelant, il simule les communications entre Alice et Bob en utilisant un protocole diffie hellman.
- ***DSA*** : un fichier définissant les fonctions associées à la méthode de signature DSA. En l'appelant, il simule la demande de signature d'un message avec la clé d'Alice, et la vérification de celui-ci.
- ***IDEA*** : un fichier définissant les fonctions associées à la méthode de chiffrement IDEA. En l'appelant, nous testons le chiffrement et le déchiffrement d'un bloc de donnée.
- ***read_file*** : un ficher testant les méthodes de chiffrement et déchiffrement par bloc sur un fichier
- ***GS15*** : le fichier permettant d'utiliser un menu pour interagir avec toutes les fonctions citées au-dessus.
- ***sha3*** :
