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
import warnings
warnings.filterwarnings('ignore')

out_path = r"***"
fig, axes = plt.subplots(figsize=(10, 8))#, sharey=True)

_file = r"***"

Table = pd.read_excel(_file, sheet_name='Sheet1',header=None)
Table_Selected = np.array(Table.iloc[:, [15, 16, 19]])
Table_Selected = Table_Selected[~np.isnan(Table_Selected).any(axis=1)]

X = Table_Selected[:,1]
y = Table_Selected[:,2]#* -1
z = Table_Selected[:,0]    
        
r, p = stats.pearsonr(X, y) 

abs_sum = sum(abs(X - y))
abs_num = len(X)
mae = (abs_sum / abs_num)

axes.set_ylabel('Decrease of LST', fontsize=20, family="Times New Roman")
axes.set_xlabel('Increase of NDVI', fontsize=20, family="Times New Roman")
sc = axes.scatter(X, y, c=z, cmap='jet', s = 200) 
#axes[nrow,ncol].set(xlim=(0, 0.24), ylim=(0, 9)) 

axes.spines['left'].set_linewidth(3)
axes.spines['right'].set_linewidth(3)
axes.spines['top'].set_linewidth(3)
axes.spines['bottom'].set_linewidth(3)
axes.tick_params(axis='both', length = 5, width = 2, labelsize = 5)  
    
axes.set_yticks(np.linspace(0, -3.0, 7)[:-1])
axes.set_yticklabels([0.0, -0.6, -1.2, -1.8, -2.4, -3.0], fontsize = 20, family="Times New Roman")   
axes.set_xticks(np.linspace(0, 0.3, 8)[:-1])
axes.set_xticklabels([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], fontsize = 20, family="Times New Roman")
axes.set_title("Deurbanization", fontsize=30, family="Times New Roman")


axes.plot(axes.get_xlim()[::-1], axes.get_ylim(), ls="--", c=".1",linewidth = 3) 
axes.text(0.0, -2.5, "R$^2$ = {0}, p<0.01\nMAE={1}".format(round(r*r, 2), round(mae, 2)), fontsize=25, family="Times New Roman")                              
sc.set_facecolor("none")

cb = fig.colorbar(sc, ax=axes)
cb.set_label('Inrease of Vegetation Percentage',family="Times New Roman",size = 20) 
for l in cb.ax.yaxis.get_ticklabels():
    l.set_family("Times New Roman")
cb.ax.tick_params(axis='both', length = 5, width = 2, labelsize=20)
Plot_path = os.path.join(out_path, "Treefraction.jpg")
fig.tight_layout() 
plt.show()        
fig.savefig(Plot_path,dpi=600,quality=100)  
        
            