import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import set_credentials_file
import plotly.offline as py

import pandas as pd
import numpy as np
from ipywidgets import interactive, HBox, VBox

from sklearn.datasets import make_blobs

X, y = make_blobs(30,random_state=101)

py.init_notebook_mode()

f = go.FigureWidget([go.Scatter(y = X[y==0][:,1], x = X[y==0][:,0], mode = 'markers'),
                     go.Scatter(y = X[y==1][:,1], x = X[y==1][:,0], mode = 'markers'),
                     go.Scatter(y = X[y==2][:,1], x = X[y==2][:,0], mode = 'markers')])
scatter = f.data[0]
N = len(X)

# Create a table FigureWidget that updates on selection from points in the scatter plot of f
t = go.FigureWidget([go.Table(
    header=dict(values=['x','y','class'],
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=[X[:,0], X[:,1], y],
               fill = dict(color='#F5F8FF'),
               align = ['left'] * 5))])

def selection_fn(trace,points,selector):
    print(points.point_inds)
    t.data[0].cells.values = [X[points.point_inds,0], X[points.point_inds,1], y[points.point_inds]]

scatter.on_selection(selection_fn)

# Put everything together
VBox((HBox(),f,t))