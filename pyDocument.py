# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 18:44:05 2019

@author: HaoranLiu
"""
import os
import pandas as pd
from Parameter import Results_path  
     
def arr_to_csv(Results_obj):
    for i in Results_obj:       
        Data = pd.DataFrame(Results_obj.get(i))
        csv_path = Results_path.get("csv_Path")
        csv_file = os.path.join(csv_path, "{0}.csv".format(i))
        Data.to_csv(csv_file, index=False, header=False)