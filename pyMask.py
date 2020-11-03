# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 19:48:59 2019

@author: HaoranLiu
"""
import numpy as np

def Mask(Data):
    index = []
    for i in range(len(Data)):
        if Data[i,0] <= 730486 or Data[i,1] == -9999 or Data[i,7] == 0 or Data[i,8] == 4:
            index.append(i)
    Data = np.delete(Data,index,axis = 0)    #记录的矢量点的日期和对应的值
    Data = Data[Data[:,0].argsort()]     #按照时间进行排序
    Data = Data[~np.isnan(Data).any(axis=1)]    #将所有含有nan项的row删除
    return Data

def Temp_Mask(Data):
    index = []
    for i in range(len(Data)):
        if Data[i,0] <= 730486 or Data[i,1] == -9999 or Data[i,1] < 2300 :
            index.append(i)
    Data = np.delete(Data,index,axis = 0)    #记录的矢量点的日期和对应的值
    Data = Data[Data[:,0].argsort()]     #按照时间进行排序
    Data = Data[~np.isnan(Data).any(axis=1)]    #将所有含有nan项的row删除
    Value = Data[:,1]

    for i in range(len(Value)):
        Data[i,1] = Value[i]

    return Data

def NDVI_Mask(Data):
    
    index = []
    for i in range(len(Data)):
        if Data[i,1] < 0 or Data[i,1] > 0.8:
            index.append(i)
    Data = np.delete(Data,index,axis = 0)    #记录的矢量点的日期和对应的值
    
    Data = Data[Data[:,0].argsort()]     #按照时间进行排序
    Data = Data[~np.isnan(Data).any(axis=1)]    #将所有含有nan项的row删除
    Value = Data[:,1]

    for i in range(len(Value)):
        Data[i,1] = Value[i]
        
    return Data
