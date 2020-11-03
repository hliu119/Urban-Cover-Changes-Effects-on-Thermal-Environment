# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 17:07:33 2019

@author: Deng
"""

import os
import numpy as np

def mkdir(path): 
    isExists=os.path.exists(path)
    
    if not isExists:
        os.makedirs(path) 

    else:
        print (path+' path exists')
        
def arr_to_csv(file,Data):
    mkdir(file)            
    for k in range(len(Data)):     
        csv_SR = os.path.join(file,"Point_{0}.csv".format(k))        
        np.savetxt(csv_SR, Data[k], delimiter = ',')        
