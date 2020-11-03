# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:49:08 2019

@author: HaoranLiu
"""
import os
import numpy as np

from Parameter import CSV_path  
from pyMask import Mask
from pyLASSO import LASSO_Temp,LASSO_NDVI
from pyCCD import CCD_Points

def Detection_Algorithm(m,n,i):
     Path = CSV_path.get("Path")
     
     path_SR = os.path.join(Path,"csv_SR_{0}_{1}".format(m,n))#文件夹目录
     path_ST = os.path.join(Path,"csv_ST")#文件夹目录              
     
     file = "Point_{0}.csv".format(i)            
     file_SR = os.path.join(path_SR,file)
     file_ST = os.path.join(path_ST,file)
    
     SR_Data = np.loadtxt(open(file_SR,"rb"),delimiter=",",skiprows=0)
     ST_Data = np.loadtxt(open(file_ST,"rb"),delimiter=",",skiprows=0)
     
     """
     Mask function:
         1. QA Cloud Mask 
         2. set Start Date 2000-1-1
         3. clear up all abnormal values
     """
     SR_Data = Mask(SR_Data)
     
     """
     Calculate NDVI values 
     NDVI = (nir -red)/(nir + red)
     """
     NDVI_Data = np.vstack((SR_Data[:,0],(SR_Data[:,4] - SR_Data[:,1])/(SR_Data[:,4] + SR_Data[:,1])))
     NDVI_Data = NDVI_Data.T
     
     """
     CCD algorithm
     """
     CCD_Obj  = CCD_Points(SR_Data)                  
     NDVI_obj = LASSO_NDVI(CCD_Obj,NDVI_Data) 
     Temp_obj = LASSO_Temp(CCD_Obj,ST_Data) 
     
     return {"CCD_Obj":CCD_Obj,
             "NDVI_Data":NDVI_Data,
             "ST_Data":ST_Data,
             
             "BreakDate":CCD_Obj.get("break_dates"),
             
             "NDVI_Value" : NDVI_obj.get("NDVI_Value"),
             "NDVI_Coefficient" : NDVI_obj.get("NDVI_Coefficient"),
             "NDVI_Intercept" : NDVI_obj.get("NDVI_Intercept"),
             "NDVI_Mean" : NDVI_obj.get("NDVI_Mean"),
                            
             "Temp_Value" : Temp_obj.get("Temp_Value"),
             "Temp_Coefficient" : Temp_obj.get("Temp_Coefficient"),
             "Temp_Intercept" : Temp_obj.get("Temp_Intercept"), 
             "Temp_Mean" : Temp_obj.get("Temp_Mean"),  
            }
