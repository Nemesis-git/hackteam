# How to use Hashcat :

Hashcat est sûrement le logiciel de craquage de mot de passe hors connexion le plus rapide de nos jours.

Il se peut que Hashcat ne veuille pas se lancer pour des raisons de hardware, pour cela on peut rajouter l’option --force.

## .potfile :

Il faut déjà savoir que Hashcat enregistre tous les hash crackés dans un fichier nommé .potfile. Ainsi, si le logiciel est lancé sur des hashes, il va déjà vérifier s’ils n’ont pas déjà été crackés. Il est situé ici : ~/.hashcat/hashcat.potfile
On peut supprimer son utilisation avec l’option --potfile-disable.
On peut aussi afficher les mdp déjà crackés avec l’option --show :
hashcat md5.hash --show
Et afficher ceux qui restent avec l’option --left :
hashcat md5.hash --left

## Options :

Hashcat propose deux options importantes qui sont les suivantes :
-m nombre permet de spécifier le type de hashes.
Par exemple 0 correspond au MD5, 100 pour SHA1 ou 1000 pour NTLM.
Si on connait pas le type du hash on peut utiliser la commande hashid.

-a nombre permet de spécifier le type d’attaques.
Par exemple 0 signifie par dictionnaire, 1 par combinaison et 2 par bruteforce.

## Attaque par dictionnaire :

Permet de cracker des mdp à partir d’une liste de mdp en clair.
En utilisant l’option -a 0 :
hashcat -a 0 -m 0 md5.hash password.lst --force

## Attaque par combinaison :

Permet de cracker des mdps à partir de la combinaison de deux dictionnaires (cela peut être les mêmes).
En utilisant l’option -a 1 :
hashcat -a 1 -m 0  md5.hash password.lst password2.lst --force
Attaque par dictionnaire avec règles :

Permet de réaliser des opérations sur les mots de passe du dictionnaire, afin d’augmenter les possibilités.
On va alors rajouter l’option -r rules (avec rules le path vers le fichier rules):
Voici des exemples fréquents de règles :
: (ne fais rien → important !)
r (permet de reverse le mdp)
u (permet de le mettre en upper case)
Tn (effectue une case sur le caractère n)
$c (append le caractère c)
^c (prepend le caractère c)

Voir plus de rules ici.

## Attaque par Bruteforce :

Permet de cracker les mdps en testant toutes les combinaisons.
En utilisant l’option -a 3 :
hashcat -a 3 -m 0 --increment md5.hash ?a?a?a?a?a?a?a --force 

Les ? symbolisent les combinaisons à utiliser.
?d pour les chiffres
?l pour les lower case
?u pour les upper case
?s pour les caractères spéciaux
?a pour tous les caractères

Et l’option --increment permet de spécifier qu’on va déjà tester ceux de taille 1, puis de taille 2, etc …



