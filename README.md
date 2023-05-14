# Dumbo Moteur de template

## By *Carlos María del Pino* and *Lamlih Houssam*

Le moteur de template Dumbo repose sur une grammaire modifiée de Lark, adaptée à nos besoins spécifiques. Nous présenterons en détail cette grammaire, en expliquant les règles modifiées et les ajouts que nous avons apportés pour répondre aux exigences de notre projet.

1. ### Description des principales règles de la grammaire

    1. `start: programme`

            Cette règle définit le point d'entrée de notre grammaire, qui est le programme global du template.

    2. `programme: txt | txt programme | dumbo_bloc | dumbo_bloc programme`

            Cette règle permet de définir un programme comme une séquence de blocs de texte (txt) et de blocs Dumbo (dumbo_bloc). Un programme peut contenir plusieurs blocs de texte et de blocs Dumbo, qui peuvent être intercalés dans n'importe quel ordre.

    3. `txt: /[^{}]+/`

            Cette règle définit un bloc de texte, qui est une séquence de caractères ne contenant pas les caractères '{' et '}'.

    4. `expressions_list: expression ";" expressions_list | expression`

            Cette règle permet de définir une liste d'expressions. Une liste d'expressions peut contenir une ou plusieurs expressions séparées par des points-virgules.

    5. `expression: "print" string_expression | for_loop | assign_statement | integer_expression | boolean_expression | if_statement`

            Cette règle définit les différentes expressions pouvant apparaître dans un bloc Dumbo. Les expressions peuvent être des instructions d'affichage (print), des boucles (for_loop), des affectations (assign_statement), des expressions entières (integer_expression), des expressions booléennes (boolean_expression), ou des instructions conditionnelles (if_statement).

    6. `assign_statement: variable ":=" string | variable ":=" string_expression "." string_expression | variable ":=" integer_expression | variable ":=" string_list`

            Cette règle définit les instructions d'affectation, qui permettent d'assigner une valeur à une variable. Une instruction d'affectation peut prendre différentes formes : assignation d'une chaîne de caractères (string), assignation d'une expression de chaîne de caractères (string_expression), assignation d'une expression entière (integer_expression), ou assignation d'une liste de chaînes de caractères (string_list).

    7. `for_loop: "for" variable "in" string_list "do" expressions_list "endfor" | "for" variable "in" variable "do" expressions_list "endfor"`

            Cette règle définit les boucles for dans notre moteur de template. Une boucle for itère sur les éléments d'une liste (string_list) ou d'une variable et exécute un bloc d'expressions (expressions_list) pour chaque élément.

    8. `if_statement: "if" boolean_expression "do" expressions_list "endif"`

            Cette règle définit les instructions conditionnelles if dans notre moteur de template

2. ### Analyse Sémantique

    L'analyse sémantique dans le moteur de template Dumbo repose sur la classe DumboTemplateEngine et utilise la bibliothèque Lark pour l'analyse syntaxique. L'objectif de l'analyse sémantique est d'interpréter les expressions et les instructions de la template, d'évaluer les valeurs des variables, de gérer les portées des variables et d'implémenter les boucles.

    L'analyse sémantique utilise deux dictionnaires pour stocker les variables : `global_variables` pour les variables globales et `local_variables` pour les variables locales. Lorsque les données sont chargées à partir du fichier de données, l'analyseur parcourt l'arbre syntaxique généré par Lark et traverse chaque noeud pour extraire les variables et leurs valeurs correspondantes. Les variables sont ensuite stockées dans le dictionnaire `global_variables`.

    Lors du rendu du template, l'analyseur effectue à nouveau un parcours de l'arbre syntaxique pour évaluer les expressions et exécuter les instructions. Les expressions entières et booléennes sont évaluées en utilisant des fonctions spécifiques, telles que `evaluate_integer_expression` et `evaluate_boolean_expression`. Ces fonctions récursives évaluent les sous-arbres correspondants en utilisant les opérations arithmétiques et logiques appropriées. Les nouvelles variables crées sonnt stockées dans le dictionnaire `local_variables`.

    L'analyseur prend également en charge les instructions conditionnelles if. Les expressions booléennes sont évaluées pour déterminer si le bloc d'expressions doit être exécuté ou non en fonction de la condition spécifiée.

    En cas d'erreur de syntaxe, telle qu'une expression invalide, une exception DumboTemplateEngineError est levée pour signaler l'erreur et afficher un message d'erreur approprié.

3. ### Problèmes rencontrés

    Pendant le développement du moteur de template, plusieurs problèmes ont été identifiés et résolus pour assurer le bon fonctionnement de l'application. Tout d'abord, la gestion des boucles a posé problème. Il était nécessaire de s'assurer que les variables d'itération soient correctement définies et mises à jour à chaque itération de la boucle. Pour résoudre ce problème, une structure de boucle while a été utilisée pour parcourir les éléments de la collection spécifiée, en veillant à mettre à jour les variables d'itération à chaque itération.

    Un autre problème rencontré était la gestion des portées des variables. Il était important de distinguer les variables globales des variables locales pour éviter les conflits de noms et garantir que les variables soient accessibles dans les bonnes portées. Pour résoudre ce problème, deux dictionnaires distincts ont été utilisés : `global_variables` pour les variables globales et `local_variables` pour les variables locales. Les variables sont stockées dans le dictionnaire approprié en fonction de leur portée, assurant ainsi une gestion correcte des portées des variables.

    Une autre difficulté était l'ambiguïté entre certaines règles de la grammaire. Puisqu'on a une grammaire LALR, il est indispensable d'éviter les collisions de réduction, cette ambiguïté pouvait entraîner des problèmes d'interprétation lorsqu'une variable était utilisée dans une expression. Pour résoudre ce problème, des vérifications ont été ajoutées et des règles ont été enlevées pour distinguer les contextes d'utilisation des variables, en s'assurant que les variables sont correctement évaluées en fonction du contexte spécifié.

    Grâce à ces solutions appliquées, les problèmes identifiés ont été résolus avec succès, permettant ainsi au moteur de template de fonctionner de manière fiable et de produire les sorties souhaitées en interprétant correctement les templates.

4. ### Répartition des tâches

    Au sein de notre groupe, nous avons adopté une approche collaborative et organisée pour mener à bien la création du moteur de template. Chaque membre du groupe a contribué de manière significative en se concentrant sur des domaines spécifiques du projet.

    Carlos s'est principalement concentré sur la conception de la grammaire du moteur de template. Il a effectué des recherches approfondies et a analysé les spécifications du moteur de template pour définir les règles de grammaire nécessaires. Il a également pris en charge la modification de la grammaire en fonction des besoins spécifiques du projet.

    Houssam s'est chargé de l'implémentation de l'analyse sémantique du moteur de template. Il a développé les fonctionnalités pour gérer les boucles, les portées des variables et l'interprétation des expressions

    Les membres du groupes ont travaillé en étroite collaboration sur les deux aspects clés du moteur de template, à savoir la conception de la grammaire et l'implémentation de l'analyse sémantique.

5. ### Conclusion

    En conclusion, le développement du moteur de template en utilisant Lark Python a été une expérience enrichissante mais également remplie de défis. La grammaire a été complétée et modifiée pour prendre en compte les besoins spécifiques du moteur de template, permettant ainsi de définir des règles claires pour l'interprétation des templates.
