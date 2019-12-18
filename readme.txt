------------------------ README ------------------------

Points forts du joueur :

Le joueur suis la stratégie de prendre les coins (en priorité) ainsi que les cotés.
Il est donc capable de savoir quand et où il peut poser pour obtenir un coin.

Résumé : 
Pour construire l'heuristique nous avons créé d'autres méthodes d'évaluation permettant 
de regarder la mobilité, les coins, les cotés, et la parité.

Chacunes de ces évaluations ne vaut evidemment pas le même poids.
Ces poids ont été déterminés au fur et à mesure des entraînement.

Ces fonctions utilisent un attribu de la classe qui est tab_weight, nous avons encodé à la main le poids
des cases. Nous nous sommes basés sur d'autres poids de jeux 8x8, et forcément adapté après reflexion à un board de 10x10.

