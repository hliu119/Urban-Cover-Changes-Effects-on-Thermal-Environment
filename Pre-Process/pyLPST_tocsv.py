# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:31:04 2019

@author: HaoranLiu
"""
import os
from pyLP import get_Value,date_Conversion,QA_Conversion,get_Array

#关闭warnings
import warnings
warnings.filterwarnings('ignore')
      
def getST_PointValues(Points_obj,rasterPath):
    
    ncol = 2
    obj = get_Array(Points_obj,rasterPath,ncol)
    xValues = obj.get("xValues")
    yValues = obj.get("yValues")
    Plot_Data = obj.get("Plot_Data")
    
    j = -1
    
    for home, dirs, files in os.walk(rasterPath):
        for file in files:
            
            #文件名列表，包含完整路径
            filename1 = os.path.splitext(file)[1]  # 读取文件后缀名
            filename0 = os.path.splitext(file)[0]  #读取文件名  
            
            Suffix_name = filename1 == ".tif"
            Document_name = filename0[-6:] == "V01_ST"
            
            if Suffix_name and Document_name:
                QA_file = os.path.join(home, filename0[:-3] + "_PIXELQA"+".tif")
                ST_file = os.path.join(home,file)
                #判断文件是否存在
                if os.path.exists(QA_file) and os.path.exists(ST_file):
                    
                    j = j + 1
                    
                    Julian_Day_Original = filename0[15:23]                    
                    Julian_Day = date_Conversion(Julian_Day_Original)
                    
                    QA_value = get_Value(QA_file,xValues,yValues)                
                    Point_value = get_Value(ST_file,xValues,yValues)
                    
                    if QA_value is not None and Point_value is not None:
                        for i in range(len(xValues)):
                            
                            Plot_Data[i,j,0] = Julian_Day
                            if QA_value[i] > 0:   
                                
                                QA_value[i] = QA_Conversion(QA_value[i])   
                                
                                if QA_value[i] == 4:
                                    Plot_Data[i,j,1] = -9999     
                                    
                                else:
                                    Plot_Data[i,j,1] = Point_value[i]
    return Plot_Data

  



