# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:34:41 2019

@author: HaoranLiu
"""
 
import os
from pyLP import walkDirFile,get_Value,date_Conversion,QA_Conversion,get_Array

#关闭warnings
import warnings
warnings.filterwarnings('ignore')
    
def getSR_PointValues(Points_obj,rasterPath,xrls,yrls):
    
    ncol = 9
    obj = get_Array(Points_obj,rasterPath,ncol)
    xValues = obj.get("xValues")
    yValues = obj.get("yValues")
    Plot_Data = obj.get("Plot_Data")
    
    j = -1
    
    for home, dirs, files in os.walk(rasterPath):
        for single_dir in dirs:
            
            Julian_Day_Original = single_dir[15:23]           
            Julian_Day = date_Conversion(Julian_Day_Original)

            dir_path = os.path.join(home, single_dir)            
            fileList = walkDirFile(dir_path)
            
            if fileList[0:4] == "LC08":
                bandList = ["SRB2","SRB3","SRB4","SRB5","SRB6","SRB7","TB10","ELQA"]
            else:
                bandList = ["SRB1","SRB2","SRB3","SRB4","SRB5","SRB7","BTB6","ELQA"]
            
            j = j + 1
            
            #文件名列表，包含完整路径
            for file in fileList:
                if file[-8:-4] in bandList:   
                    
                    if os.path.exists(file):
                    #打开栅格数据  
                    Point_Value = get_Value(file,xValues,yValues,xrls,yrls)
                    
                    if Point_Value is not None:
                        for i in range(len(xValues)):
                            
                            Plot_Data[i,j,0] = Julian_Day
                            
                            Band_Number = bandList.index(file[-8:-4]) + 1
                            
                            if Band_Number == len(bandList):
                                if Point_Value[i] > 0:
                                    Point_Value[i] =QA_Conversion(Point_Value[i])
                                    
                            Plot_Data[i,j,Band_Number] = Point_Value[i]
    return Plot_Data

 
    