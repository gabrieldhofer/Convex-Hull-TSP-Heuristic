"""
    Author: Gabriel Hofer
    Date: 01/27/2021
"""
import random as R
import time
import numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

def tour(lst,a,b):
  """ Returns distance of the tour """
  s=0
  for i in range(a,b):
    s+=cdist(lst[(i+len(lst))%len(lst)].reshape(1,-1),lst[(i+1)%len(lst)].reshape(1,-1,),'euclidean')
  return s

def show(output):
  """ Show Visual of Tour """
  plt.ioff()  # interactive mode off
  plt.pause(2)   # brief wait
  plt.ion()  # turn interactive mode on
  plt.clf()
  temp = np.vstack((output, output[0]))
  plt.plot(temp[:,0], temp[:,1], color='red') 
  plt.show()

def tsp_ch(n):
  """ Traveling Salesperson Problem - Convex Hull Heuristic """
  """ First, Call Convex Hull on all points """
  points = np.random.rand(n, 2)   
  hull = ConvexHull(points)
  P = hull.vertices
  z=np.zeros(n)
  for i in P: z[i]=1

  def dist(i,j):
  """ 
      dist returns the net length added to the tour when an interior point j 
      is added to the tour. Basically, we remove one line segment and add 
      two more (like rerouting) 
  """
    one=cdist(points[P[i]].reshape(1,-1), points[P[i+1]].reshape(1,-1), 'euclidean')
    two=cdist(points[P[i]].reshape(1,-1), points[j].reshape(1,-1)) + \
        cdist(points[P[i+1]].reshape(1,-1),points[j].reshape(1,-1))
    return two-one

  """ 
      Add points to the tour greedily - i.e. add an interior points which increases 
      the length of the tour by a minimal amount. this is how dist is applied		
  """
  while P.shape[0]<len(points):
    mn=1e8
    for i in range(len(P)-1):
      for j in range(len(z)):
        if not z[j] and dist(i,j)<mn:
          mn=dist(i,j)
          idxj=j
          idxi=i
    P=np.concatenate((P[:idxi+1],np.array([idxj]),P[idxi+1:]), axis=None)
    z[idxj]=1
  
  """ 
      Apply Dr. McGough's idea where two random indeces 
      are chosen and the subarray is reversed 
  """
  output = np.array([points[k] for k in P])
  bef=tour( output ,0,len(P)+1) # init tour dist of P
  i=0
  while True:
    a=R.randint(0,len(P)-1)
    b=R.randint(0,len(P)-1)
    if a>b: a,b=b,a
    output[a:b+1,:]=output[a:b+1,:][::-1]
    aft=tour(output,0,len(P)+1)
    i+=1
    if aft<bef: 
      print("before pert.: "+str(bef)+" after pert.: "+str(aft))
      bef=aft
      show(output)
      i=0
    else:
      output[a:b+1,:]=output[a:b+1,:][::-1] 
    if i>1e3*n: break
  return output

if __name__ == "__main__":
  tsp_ch(int(input()))
