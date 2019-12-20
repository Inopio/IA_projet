------------------------ README ------------------------

Points forts du joueur :

Le joueur suis la stratégie de prendre les coins (en priorité) ainsi que les cotés.
Il est donc capable de savoir quand et où il peut poser pour obtenir un coin.
Il fait également attention à poser une pièce qui restera stable, c'est à dire que l'adversaire
ne pourra pas lui voler.

Résumé : 
Pour construire l'heuristique nous avons créé d'autres méthodes d'évaluation permettant 
de regarder la mobilité, les coins, les cotés, la parité, la stabilité, et la victoire ou la défaite.

Chacunes de ces évaluations ne vaut evidemment pas le même poids.
Ces poids ont été déterminés au fur et à mesure des entraînement.
On a choisi de retourner différentes évaluations en fonction de l'état du board. 
S'il y a moins de 50 pièces, on privilégie la prise des coins.
Entre 50 et 90 pièces on privilégie toujours les coins mais cette fois on rajoute la stabilité et le fait
de pouvoir bloquer l'adversaire.
A plus de 90, on privilégie le fait de gagner, c'est à dire posséder plus de pions que l'adversaire, les coins et la stabilité.

Pour calculer les différentes valeurs, nos fonctions utilisent un attribu de la classe qui est tab_weight, nous avons encodé à la main le poids
des cases. Nous nous sommes basés sur d'autres poids de jeux 8x8, et forcément adapté après reflexion à un board de 10x10.

