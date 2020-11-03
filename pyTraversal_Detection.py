# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:28:42 2019

@author: HaoranLiu
"""
from datetime import datetime
import numpy as np

from pyLASSO_Detection import Detection_Algorithm
from pyDocument import arr_to_csv
from pyPlot import LASSO_Plot_NDVI,LASSO_Plot_Temp

def CCDL(Point_length):
     """
     Read Arrays to Save Different Parameters 
     """
     
     NDVI_Coefficient = []
     NDVI_Intercept = []   
     NDVI_Mean = [] 
     NDVI_Value = []  

     Temp_Coefficient = []
     Temp_Intercept = []    
     Temp_Mean = []  
     Temp_Value = [] 
     
     Delta = []  
     MaxCoeff = []
     
     BreakDate = []
     
     Multi_Location = []
     Single_Location = []
     
     """
     Travese every Point
     """
     for i in range(0,Point_length):
  
         """
         function:
             Single_flag are used to flag whether CCD can detect break point(s) in buffer area
              
             If yes, ignore single trend 
             
             If no, compare all single trend 
             
         """
         Single_flag = 0   
         
         """
         Initialize the Delta and Maxcoeff value to record 
         """
         Single_record_x = 0
         Single_record_y = 0
         
         Multi_record_x = 0
         Multi_record_y = 0
         
         Delta_ID = 0
         Delta_NDVI = 0
         Delta_Temp = 0
         
         MaxCoeff_ID = 0         
         MaxCoeff_NDVI = 0
         MaxCoeff_Temp = 0
         
         """
         Travese Buffer Area
         """
         for m in range(-1,2):
             for n in range(-1,2):
                 
                 obj = Detection_Algorithm(m,n,i)   
                               
                 NDVI_SinglePoint = obj.get("NDVI_Value")                                
                 Temp_SinglePoint = obj.get("Temp_Value")  
                 BreakDate_SinglePoint = obj.get("BreakDate")
                 
                 NDVI_SingleCoef = obj.get("NDVI_Coefficient") 
                 Temp_SingleCoef = obj.get("Temp_Coefficient")  
                                               
                 """
                 function:
                     
                     If CCD Algorithm can dectect the breakpoint, travese the buffer area;
                     
                     compare 3*3 Buffer Points values, select the Highest Delta Value.
                     
                 """
                 length = len(NDVI_SinglePoint)                            
                 if  length > 1:  
                     for p in range(0, length):
                         for q in range(p + 1, length):
                             if NDVI_SinglePoint[p] < NDVI_SinglePoint[q]:
                                 if Temp_SinglePoint[p] > Temp_SinglePoint[q]:
                                     if (NDVI_SinglePoint[q] - NDVI_SinglePoint[p]) > Delta_NDVI:
                                         #if NDVI_SinglePoint[q] - NDVI_SinglePoint[p] < 0.4 :
                                             #if Temp_SinglePoint[p] - Temp_SinglePoint[q] < 100 :
                                         
                                                 Single_flag = 1 #Make sure "elif" will not be executed
                                                 
                                                 Multi_record_x = m
                                                 Multi_record_y = n
                                                 
                                                 Delta_ID = i
                                                 Delta_NDVI =  NDVI_SinglePoint[q] - NDVI_SinglePoint[p] 
                                                 Delta_Temp = (Temp_SinglePoint[q] - Temp_SinglePoint[p]) * 0.1 
                                                 
                                                 Date_SinglePoint = BreakDate_SinglePoint[p]
                                                 
                 elif length == 1 and Single_flag == 0:
                      """
                      function:
                         
                          single trend is different from the muitiple trends 
                         
                          compare the coefficient rather than value
                         
                      """
                      if NDVI_SingleCoef[0] > MaxCoeff_NDVI:
                          if Temp_SingleCoef[0] < MaxCoeff_Temp:
                              
                                 Single_record_x = m
                                 Single_record_y = n
                                 
                                 MaxCoeff_ID = i 
                                 MaxCoeff_NDVI =  NDVI_SingleCoef[0] 
                                 MaxCoeff_Temp =  Temp_SingleCoef[0]
         """
         Record position of the highest value point in 3*3 Buffer Area
         
         """                              
         
         if Single_flag == 1 and Delta_NDVI != 0 and Delta_Temp != 0:             
             Delta.append([Delta_ID,Delta_NDVI,Delta_Temp])  
             Multi_Location.append([Delta_ID,Multi_record_x, Multi_record_y])
             BreakDate.append([Delta_ID,datetime.fromordinal(int(Date_SinglePoint)).date()])
             obj_results = Detection_Algorithm(Multi_record_x,Multi_record_y,i) 
             
         elif Single_flag == 0 and MaxCoeff_NDVI != 0 and MaxCoeff_Temp != 0:             
             MaxCoeff.append([MaxCoeff_ID,MaxCoeff_NDVI,MaxCoeff_Temp])
             Single_Location.append([MaxCoeff_ID,Single_record_x, Single_record_y])
             obj_results = Detection_Algorithm(Single_record_x,Single_record_y,i) 
             
         else:
             continue
         NDVI_Coefficient.append(np.insert(obj_results.get("NDVI_Coefficient"),0,i))
         NDVI_Intercept.append(np.insert(obj_results.get("NDVI_Intercept"),0,i)) 
         NDVI_Mean.append(np.insert(obj_results.get("NDVI_Mean"),0,i))
         NDVI_Value.append(np.insert(obj_results.get("NDVI_Value"),0,i))
         
         Temp_Coefficient.append(np.insert(obj_results.get("Temp_Coefficient"),0,i))
         Temp_Intercept.append(np.insert(obj_results.get("Temp_Intercept"),0,i))
         Temp_Mean.append(np.insert(obj_results.get("Temp_Mean"),0,i))
         Temp_Value.append(np.insert(obj_results.get("Temp_Value"),0,i))               
             
         LASSO_Plot_NDVI(obj_results,i)
         LASSO_Plot_Temp(obj_results,i) 

     arr_obj =  {
             "Delta"     : Delta,
             "MaxCoeff"  : MaxCoeff,
             "Multi_Location"  : Multi_Location,     
             "Single_Location" : Single_Location,
             "BreakDate" : BreakDate,
             
             "NDVI_Coefficient" : NDVI_Coefficient,
             "NDVI_Intercept"   : NDVI_Intercept,
             "NDVI_Mean"        : NDVI_Mean,             
             "NDVI_Value"       : NDVI_Value,
             
             "Temp_Coefficient" : Temp_Coefficient,
             "Temp_Intercept"   : Temp_Intercept,
             "Temp_Mean"        : Temp_Mean,             
             "Temp_Value"       : Temp_Value,
            }               
     arr_to_csv(arr_obj)   
