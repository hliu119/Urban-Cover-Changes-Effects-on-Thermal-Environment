# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:22:03 2019

@author: HaoranLiu
"""

#读取矢量
from osgeo import ogr
import  sys
#读取栅格
from osgeo import gdal 
import  os
import numpy as np
#转换时间
from datetime import datetime
#转换QA波段
import math

def get_Array(Points_obj,rasterPath,ncol):
    xValues = Points_obj.get("x")
    yValues = Points_obj.get("y")
    """
    获取矢量点对应的栅格值
    """  
    gdal.AllRegister() #获取注册类
    Plot_Data = np.zeros(shape=(len(xValues),\
                                len([lists for lists in os.listdir(rasterPath)\
                                     if os.path.isdir(os.path.join(rasterPath, lists))]) + 2, ncol)) #每个点形成一张图,对应存储不同的波段值3
    return {"xValues": xValues, 
            "yValues": yValues,
            "Plot_Data":Plot_Data
            }
    
def walkDirFile(srcPath, ext=".tif"):
    """
    遍历文件夹
    :param srcPath:
    :param ext:
    :return:
    """
    if not os.path.exists(srcPath):
        print("not find path:{0}".format(srcPath))
        return None
    if os.path.isfile(srcPath):
        return None

    if os.path.isdir(srcPath):
        fileList = []
        for root, dirs, files in os.walk(srcPath):
            for name in files:
                filePath = os.path.join(root, name)
                if ext:
                    if ext == os.path.splitext(name)[1]:
                        fileList.append(filePath)
                else:
                    fileList.append(filePath)
        fileList.sort()
        return fileList
    else:
        return None
    
    
def getPoint_Values(pointPath):
    """
    获取矢量点经纬度
    """
    #设置driver
    driver = ogr.GetDriverByName('ESRI Shapefile')
    #打开矢量
    ds = driver.Open(pointPath, 0)
    if ds is None:
        print('Could not open points of the shpfile')
        sys.exit(1)
    #获取图层
    layer = ds.GetLayer()
    
    #获取要素及要素地理位置
    xValues = []
    yValues = []
    feature = layer.GetNextFeature()
    while feature:
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()
        xValues.append(x)
        yValues.append(y)  
        feature = layer.GetNextFeature()
    return {"x": xValues, 
            "y": yValues
            }
    
def date_Conversion(Julian_Day_Original):
    Date_value = datetime.strptime(Julian_Day_Original, '%Y%m%d').date()
    Julian_Day = Date_value.toordinal()
    return Julian_Day
    
def get_Value(rasterfile,xValues,yValues,xrls=0, yrls=0):
    
    ds = gdal.Open(rasterfile)
    
    if ds is None:
        print('Could not open {0}'.format(rasterfile))
        Data_value = None
        
    else:
        #提取单波段对应的像元值
        band = ds.GetRasterBand(1)

        """
        #获取行列、波段
        rows = ds.RasterYSize
        cols = ds.RasterXSize
        bands = ds.RasterCoun
        """
        #获取放射变换信息
        transform = ds.GetGeoTransform()
        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]
      
        #提取各个点对应的像元值
        """
        i 代表每一个像元点
        j 代表每个具体的日期代表的数据
        """        
        xOffset = np.zeros(len(xValues))
        yOffset = np.zeros(len(xValues))              
        for i in range(len(xValues)):
            x = xValues[i]
            y = yValues[i]
            #获取点位所在栅格的位置
            xOffset[i] = int((x-xOrigin)/pixelWidth)
            yOffset[i] = int((y-yOrigin)/pixelHeight)            
        
        Data_value = np.zeros(len(xOffset))
        for i in range(len(Data_value)):
            data = band.ReadAsArray(xOffset[i] + xrls, yOffset[i] + yrls, 1, 1)
            if data :
                Data_value[i] = data[0,0]
                
    return Data_value

def QA_Conversion(Value):
    return int(math.log2(Value % 64) - 1)
    