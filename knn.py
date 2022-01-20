import numpy as np
import random

def nearestNeighbor(cities,i):
# Choix d'une première ville

  j = cities[i]
  road = [i]

  # Formation du chemin avec nearest neighbour
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