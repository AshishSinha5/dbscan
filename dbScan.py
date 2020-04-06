# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 09:43:11 2020

@author: ashish
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

point = pd.read_csv("G:/dbscan/ca.csv",delimiter=":", header = None, names = ["long", "lat", "place"])

sample = point[:20000]

#determining Eps and MinPts

MinPts = 4

def dist(x1,x2,y1,y2): #returns euclidian distance
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

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

y = sample.sort_values(by = 'k-dist', ascending = False)['k-dist']

fig = go.Figure(
        data = [go.Scatter(y=y, text = list(y.index))]
        )

fig.show(renderer = "browser")

#by inspection
Eps = sample['k-dist'].iloc[5746]

