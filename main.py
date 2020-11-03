# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:36:48 2019

@author: HaoranLiu
"""
#计算运行时间
import time
from pyTraversal_Detection import CCDL
from Parameter import Point

if __name__ == "__main__":
     print("running start ...")
     t1 = time.time()
     CCDL(Point.get("Point_Number"))     
     print("use time: {0}".format(time.time() - t1))
     print("running end ...")
