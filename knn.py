import numpy as np
import random

# Tableau des distances entre villes
cities = [[np.inf, 208, 324, 548, 252, 12, 228, 212, 212], [207, np.inf, 532, 756, 398, 194, 28, 94, 359], [323, 530, np.inf, 258, 574, 334, 551, 534, 535], [546, 754, 251, np.inf, 798, 557, 774, 758, 758], [250, 399, 575, 799, np.inf, 237, 419, 403, 46], [12, 194, 339, 563, 238, np.inf, 214, 198, 199], [228, 28, 553, 777, 419, 214, np.inf, 76, 380], [210, 93, 535, 758, 401, 196, 76, np.inf, 361], [210, 359, 535, 759, 46, 197, 379, 363, np.inf]]
cities = np.array(cities)
def nearestNeighbor(cities,i):
# Choix d'une première ville

  j = cities[i]
  road = [i]

  # Formation du chemin en KNN
  while 1:
      if len(road) == len(cities):
          break
      else:
          # Distance minimale
          new_city = np.argmin(j)
          if not(new_city in road):
              road.append(new_city)
              j = cities[new_city]
          else:
              j[new_city] = np.inf

  # Ajout du dernier noeud pour terminer le tour
  road.append(i)
  road = np.array(road) + 1
  return road

print(nearestNeighbor(cities,0))