# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:58:57 2019

@author: Administrator
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
from scipy.stats import gaussian_kde
from scipy import optimize
import warnings
warnings.filterwarnings('ignore')

#直线方程函数
def f_1(x, A, B):
    return A*x + B

out_path = r"***\Urbanization"
fig, axes = plt.subplots(figsize=(8, 8))#, sharey=True)

_file = r"**"
Table = pd.read_excel(_file, sheet_name='Sheet1',header=None)
Table_Selected = np.array(Table.iloc[:, [0, 1]])
Table_Selected = Table_Selected[~np.isnan(Table_Selected).any(axis=1)]

X = Table_Selected[:,0] #* -1
y = Table_Selected[:,1]
#xy = np.vstack([X,y])
#z = gaussian_kde(xy)(xy)    
        
r, p = stats.pearsonr(X, y) 

abs_sum = sum(abs(X - y))
abs_num = len(X)
mae = (abs_sum / abs_num)

#直线拟合与绘制
A1, B1 = optimize.curve_fit(f_1, X, y)[0]
x1 = X
y1 = A1*X + B1

axes.set_title("Urbanization", fontsize=30, family="Times New Roman")
axes.set_ylabel('Increase of LST', fontsize=20, family="Times New Roman")
axes.set_xlabel('Decrease of NDVI', fontsize=20, family="Times New Roman")
axes.scatter(X, y, color='', marker='o', edgecolors='black', s = 50)
axes.plot(x1, y1, "red", label = 'regression line', lw = 2)    
axes.set(xlim = axes.get_xlim(), ylim = axes.get_ylim())   

axes.set_yticks(np.arange(0, 15, 3))  
axes.set_xticks(np.arange(0, (int(max(X)*20))/20/5), (int(max(X)*20) + 1)/20)  
#axes.plot(axes.get_xlim()[::-1], axes.get_ylim(),'red', label = '1:1 line', lw = 2)

axes.spines['left'].set_linewidth(3)
axes.spines['right'].set_linewidth(3)
axes.spines['top'].set_linewidth(3)
axes.spines['bottom'].set_linewidth(3)
axes.tick_params(axis='both', length = 5, width = 2, labelsize = 5)
import matplotlib
matplotlib.mathtext.SHRINK_FACTOR = 0.5
matplotlib.mathtext.GROW_FACTOR = 1 / 0.5

if B1 < 0:
    axes.text(int(min(X)*20)/20,  0.15, "R$\mathregular{^2}$" + " = {0}, p<0.01,\nMAE = {1}"\
    .format(round(r*r, 2), round(mae, 2)), fontsize=20, family="Times New Roman")                              
if B1 > 0:
    axes.text(int(min(X)*20)/20,  0.15, "R$\mathregular{^2}$" + " = {0}, p<0.01,\nMAE = {1}"\
    .format(round(r*r, 2), round(mae, 2)), fontsize=20, family="Times New Roman") 
for l in axes.yaxis.get_ticklabels():
    l.set_family("Times New Roman") 
    l.set_size(20)
for l in axes.xaxis.get_ticklabels():
    l.set_family("Times New Roman") 
    l.set_size(20)
#axes.legend(loc='upper left', frameon=False, prop={'size':20})    
    
Plot_path = os.path.join(out_path, "Urbanization.jpg")
plt.show()        
fig.savefig(Plot_path,dpi=300,quality=100)  
        
            