# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:20:55 2019

@author: HaoranLiu
"""
import numpy as np
import os

#SG filter
import scipy.signal
#LASSO算法
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV ,LassoLarsCV ,LassoLarsIC # LassoLarsCV基于最小角回归交叉验证实现alpha的选取

#关闭warnings
import warnings
warnings.filterwarnings('ignore')

from Parameter import Results_path  
from pyLASSO import Find_Index,Xarray_Calcultaion,LASSO_Calculation
from pyMask import Temp_Mask, NDVI_Mask


def LASSO_Chart(X,model):   
    X_interp = np.linspace(min(X),max(X),(X[-1] - X[0])).astype(int)
    Y_interp = model.predict(Xarray_Calcultaion(X_interp))
    Y_interp = scipy.signal.savgol_filter(Y_interp,5,3)  
    plt.plot(X_interp, Y_interp)    
    
def Plot (Point_Data,CCD_Obj,Number,Type):
    fig = plt.figure()#figsize=(50, 10))
    fig.add_subplot()#ylim=(0, 5000)) 
    
     
    Start_dates = CCD_Obj.get("start_dates") 
    End_dates = CCD_Obj.get("end_dates") 
    
    Julian_Days = Point_Data[:,0] 
    Values = Point_Data[:,1]
    
    for i in range(len(Start_dates)):
       
        Start = Find_Index(Start_dates[i],Julian_Days) 
        End = Find_Index(End_dates[i],Julian_Days)         

        model = LASSO_Calculation(Start,End,Julian_Days,Values)                  
        LASSO_Chart(Julian_Days[Start:End],model)
        plt.scatter(Julian_Days, Values, c = "g", alpha ="0.1")
        
        plot_path = Results_path.get("plot_Path")
        plot_file = os.path.join(plot_path,"{0}_{1}.jpg".format(Type,Number))
        plt.savefig(plot_file,dpi=300,quality=100)

    return {"Julian_Days":Julian_Days,
            "Values":Values,        
            }
    

def LASSO_Plot_NDVI(obj_results,i):
    CCD_Obj = obj_results.get("CCD_Obj") 
    NDVI_Data = obj_results.get("NDVI_Data") 
    Point_Data = NDVI_Mask(NDVI_Data)  
    Plot(Point_Data,CCD_Obj,i,"NDVI")
      
def LASSO_Plot_Temp(obj_results,i):        
    CCD_Obj = obj_results.get("CCD_Obj") 
    Temp_Data = obj_results.get("ST_Data")     
    Point_Data = Temp_Mask(Temp_Data)  
    Plot(Point_Data,CCD_Obj,i,"Temp")




    


