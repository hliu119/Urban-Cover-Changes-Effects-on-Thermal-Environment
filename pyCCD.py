# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:31:04 2019

@author: HaoranLiu
"""
import ccd
import numpy as np
#关闭warnings
import warnings
warnings.filterwarnings('ignore')

def Values(days,intercept,coef):
    value = intercept + coef[0] * days +\
    coef[1]*np.cos(days*1*2*np.pi/365.25) + coef[2]*np.sin(days*1*2*np.pi/365.25) +\
    coef[3]*np.cos(days*2*2*np.pi/365.25) + coef[4]*np.sin(days*2*2*np.pi/365.25) +\
    coef[5]*np.cos(days*3*2*np.pi/365.25) + coef[6]*np.sin(days*3*2*np.pi/365.25)    
    return value

def CCD_Points(Data):

    params = {'QA_BITPACKED': False,
                  'QA_FILL': 255,
                  'QA_CLEAR': 0,
                  'QA_WATER': 1,
                  'QA_SHADOW': 2,
                  'QA_SNOW': 3,
                  'QA_CLOUD': 4}
    
    dates, blues, greens, reds, nirs, swir1s, swir2s, thermals, qas = Data.T
    
    results = ccd.detect(dates, blues, greens, reds, nirs, swir1s, swir2s, thermals, qas, params=params)

    start_dates = []
    end_dates = []
    break_dates = []
    
    for num, result in enumerate(results['change_models']):
        
        time_length = result['end_day'] - result['start_day']

        if time_length > 365:
        #if result['change_probability'] == 1 and time_length > 730:
        #if result['change_probability'] == 1 :
            
            start_dates.append(result['start_day'])
            end_dates.append(result['end_day'])
            break_dates.append(result['break_day'])           
   
    return {"start_dates": start_dates,
            "end_dates": end_dates,
            "break_dates": break_dates,     
            }


