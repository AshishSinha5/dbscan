# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 09:43:11 2020

@author: ashish
"""

import pandas as pd
import numpy as np
#import plotly.graph_objects as go
import json
import math

point = pd.read_csv("G:/dbscan/ca.csv",delimiter=":", header = None, names = ["long", "lat", "place"])

sample = point.sample(frac = 0.3, random_state = 1)

#determining Eps and MinPts

MinPts = 4

def dist(x1,x2,y1,y2): #returns euclidian distance
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

# Heuristic calculation of parameter Eps as discussed in section 4.2 of the original paper

def kdist(sample,MinPts): #returns kth nearest neighbour of the point
    sample['k-long'] = np.nan
    sample['k-lat'] = np.nan
    sample['k-dist'] = np.nan
    for i in range(len(sample)):
        df = sample[['long','lat']]
        df['dist'] = dist(df['long'].iloc[0], df['long'], df['lat'].iloc[0], df['lat'])
        sample['k-long'].iloc[i] = df.sort_values(by = 'dist').iloc[5]['long']
        sample['k-lat'].iloc[i] = df.sort_values(by = 'dist').iloc[5]['lat']
        sample['k-dist'].iloc[i] = df.sort_values(by = 'dist').iloc[5]['dist']
    return

#sample["k-dist"] = dist(sample['long'], sample['k-long'], sample['lat'], sample['k-lat'])

#kdist(sample, MinPts)

#y = sample.sort_values(by = 'k-dist', ascending = False)['k-dist']

#fig = go.Figure(
#        data = [go.Scatter(y=y, text = list(y.index))]
#        )

#fig.show(renderer = "browser")

#fig.write_image("G:/dbscan/k-dist.png")
#by inspection
#Eps = sample['k-dist'].iloc[5746]
Eps = 3173.0516856805216 #found on previous run of k-dist
sample['clId'] = np.nan

# Naive implementation of algorithms as discussed in Section 4.1 of the paper

def regionQuery(sample, pt, Eps): # gives the epsilon neighborhood of point pt
    seed = []
    for i in range(len(sample)):
        x1 = sample['long'].iloc[pt]
        y1 = sample['lat'].iloc[pt]
        x2 = sample['long'].iloc[i]
        y2 = sample['lat'].iloc[i]
        d = dist(x1,x2,y1,y2)
        if d<=Eps:
            seed.append(i)
    return seed

def dbscan(sample, Eps, MinPts): # main function for dbscan
    ClusterId = -1 # cluster Id for noise is -1
    for i in range(len(sample)):
        if math.isnan(sample['clId'].iloc[i]):
            if expandCluster(sample, i, ClusterId, Eps, MinPts):
                ClusterId+=1
    
                
                
                
def expandCluster(sample, i, ClId, Eps, MinPts): #function for expanding the clusters
    seeds = regionQuery(sample, i, Eps)
    if len(seeds) < MinPts:
        sample['clId'].iloc[i] = -1  #noise  = -1
        return False
    else:
        sample['clId'].iloc[seeds] = ClId
        seeds.remove(i)
        while len(seeds):
            currentP = seeds[0]
            result = regionQuery(sample, currentP, Eps)
            if len(result) >= MinPts:
                for i in range(len(result)):
                    if math.isnan(sample['clId'].iloc[i]) or sample['clId'].iloc[i] == -1:
                        if math.isnan(sample['clId'].iloc[i]):
                            seeds.append(i)
                        sample['clId'].iloc[i] = ClId
            seeds.remove(currentP)
        return True


dbscan(sample, Eps, MinPts)

    
# save the output file
output = {}
output['MinPts'] = MinPts
output['Eps'] = Eps
output['data'] = sample

with open('data.txt', 'w') as outfile:
    json.dump(output, outfile)
    
    
        
        
    

