# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:03:26 2019

@author: HaoranLiu
"""
import numpy as np

#LASSO算法
from sklearn.linear_model import LassoCV ,LassoLarsCV ,LassoLarsIC # LassoLarsCV基于最小角回归交叉验证实现alpha的选取
#关闭warnings
import warnings
warnings.filterwarnings('ignore')

from pyMask import Temp_Mask, NDVI_Mask


def Find_Index(Values,Julian_Days):
    location = 0
    if Values >= Julian_Days[-1]:
        location = len(Julian_Days) - 1
    else:
        for i in range(1,len(Julian_Days)): 
            if Values >= Julian_Days[i - 1] and Values < Julian_Days[i]:
                location = i - 1
                break
    return location

def Xarray_Calcultaion(X):
    T = 365.25
    n_samples, n_features = len(X), 7 # n_samples样本个数，n_features特征个数
    X_array = np.zeros((n_samples, n_features))
    for m in range(n_samples):
        for n in range(0, n_features - 2, 2):
            X_array[m,n] = np.cos((n + 2) * np.pi * X[m] / T)
            X_array[m,n + 1] = np.sin((n + 2) * np.pi * X[m] / T)
        X_array[m,n_features - 1] = X[m]
    return X_array

def LASSO_Calculation(BreakPoint_0,BreakPoint_1,Julian_Days,Values):
    Julian_Days_Interval = Julian_Days[BreakPoint_0:BreakPoint_1]
    Values_Interval = Values[BreakPoint_0:BreakPoint_1]
    X = Xarray_Calcultaion(Julian_Days_Interval)
    Y = Values_Interval.reshape(len(Values_Interval),1)    
    # ==============================使用样本数据训练系数矩阵============================
    model = LassoLarsIC() # LassoLarsCV自动调节alpha可以实现选择最佳的alpha
    model.fit(X, Y)   # 线性回归建模
    return model 

def LASSO(CCD_Obj,Data):
    Coefficient = np.ones((0))
    Intercept = np.ones((0)) 
    Mean = np.ones((0)) 
    Value = np.ones((0)) 
    
    Start_dates = CCD_Obj.get("start_dates") 
    End_dates = CCD_Obj.get("end_dates") 

    Julian_Days = Data[:,0] 
    Values = Data[:,1]   
    
    for i in range(len(Start_dates)):
       
        Start = Find_Index(Start_dates[i],Julian_Days) 
        End = Find_Index(End_dates[i],Julian_Days)         

        model = LASSO_Calculation(Start,End,Julian_Days,Values)   
        Coefficient = np.append(Coefficient, model.coef_[6])
        Intercept = np.append(Intercept, model.intercept_ )
        Mean = np.append(Mean, np.mean(Julian_Days))
        Value = np.append(Value, np.mean(Julian_Days) * model.coef_[6] + model.intercept_)
    
    return {"Value":Value,
            "Coefficient":Coefficient,
            "Intercept":Intercept,
            "Mean":Mean,            
            }
    
def LASSO_NDVI(CCD_Obj,NDVI_Data) : 
    
    Data = NDVI_Mask(NDVI_Data) 
    arr_obj = LASSO(CCD_Obj,Data)
    
    return {"NDVI_Value":arr_obj.get("Value"),
            "NDVI_Coefficient":arr_obj.get("Coefficient"),
            "NDVI_Intercept":arr_obj.get("Intercept"),
            "NDVI_Mean":arr_obj.get("Mean"),            
            }
    
    
def LASSO_Temp(CCD_Obj,Temp_Data):     

    Data = Temp_Mask(Temp_Data) 
    arr_obj = LASSO(CCD_Obj,Data)

    return {"Temp_Value":arr_obj.get("Value"),
            "Temp_Coefficient":arr_obj.get("Coefficient"),
            "Temp_Intercept":arr_obj.get("Intercept"),
            "Temp_Mean":arr_obj.get("Mean"),                       
            }
    