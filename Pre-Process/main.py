# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 15:41:49 2019

@author: HaoranLiu
"""
#计算运行时间
import time
import os

from Parameter import Raster_path,Shp_path,CSV_path 
from pyDocument import arr_to_csv
from pyLP import getPoint_Values
from pyLPSR_tocsv import getSR_PointValues
from pyLPST_tocsv import getST_PointValues

print("running start ...")
t1 = time.time()

PointPath =  Shp_path.get("PointPath")
Points_obj = getPoint_Values(PointPath)

ST_Path = Raster_path.get("ST_Path")
ST_Data = getST_PointValues(Points_obj,ST_Path)
file_ST = os.path.join(CSV_path.get("csv"),"csv_ST") 
arr_to_csv(file_ST,ST_Data)
                          
for i in range(-1,2):
    for j in range(-1,2):
        
        xrls = i
        yrls = j
        
        SR_Path = Raster_path.get("SR_Path")
        SR_Data = getSR_PointValues(Points_obj,SR_Path,xrls,yrls)
        file_SR = os.path.join(CSV_path.get("csv"),"csv_SR_{0}_{1}".format(i,j))             
        arr_to_csv(file_SR,SR_Data)


print("use time: {0}".format(time.time() - t1))
print("running end ...")  
