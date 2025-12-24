"""
2019/12/12
<info>
{
	"rule_name": "CH_Rule_COP_V",
	"version":"V3.2.1",
	"rule_type": "chiller",
	"rule_describle": "COP degradation",
	"sensors": [
	{"standName": "Leaving_Chilled_Water","ruleName": "Leaving_Chilled_Water","dynamic":"chiller"},
	{"standName": "Leaving_Condenser_Water","ruleName": "Leaving_Condenser_Water","dynamic":"chiller"},
	{"standName": "Percent_Line_Current","ruleName": "Percent_Line_Current","dynamic":"chiller"}
	],
	"rule_parameters":{
            "parameters":[
            {
                    "name":"evap_approach",
                    "value":0,
                    "description":"Default evaporator approach(℃)"
            },
            {
                    "name":"cond_approach",
                    "value":0,
                    "description":"Default condenser approach(℃)"
            }
            ]
    }
}
</info>
"""


"""FDD
/*{
    "rule_name":"CH_Rule_COP_V",
    "rule_type":"chiller",
    "rule_description":"COP degradation",
    "rule_category":"Inefficient Running Equipment",
    "rule_suggestion":"1.Please check CHST and ERT sensors; 2.Please check CDLT and CRT sensors; 3.Please check DischargeT and CRT sensors; 4.Plan to clean the high approach temperature heat exchangers; 5.Plan to clean the high approach temperature heat exchangers; 6.Plan to maintain the compressor; 7.Plan to maintain the motor; 8.Check heat insulation of the system; 9.Plan of maintenance.",
    "trend_display":"",
    "sensors":[
        {
            "ref_name":"ch1DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch1EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch2EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch3EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch4EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch5EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch6EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch7EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8DPM_pow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Evap_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Evap_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Entering_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Leaving_Chilled_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Cond_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Cond_Sat_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Leaving_Condenser_Water",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Economizer_Pressure",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Economizer_Gas_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Comp_Discharge_Temp",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Chilled_Water_Flow",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Percent_Line_Current",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8Actual_VFD_Speed_Per",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8GV1_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
        {
            "ref_name":"ch8EXV_Position",
            "data_type":"analog",
            "mandatory":"false"
        },
    ],
    "parameters":[
        {
          "name":"CH_TP",
          "value":[],
          "description":"Chiller types"
        },
        {
          "name":"evap_approach",
          "value":0,
          "description":"Default evaporator approach"
        },
        {
          "name":"cond_approach",
          "value":0,
          "description":"Default condenser approach"
        },
    ],
    "delays":[
        {
            "name":"",
            "value":0,
            "description":""
        }
    ]
}
*/
"""


from CoolProp.CoolProp import PropsSI
import datetime
import numpy as np
import pandas as pd
from scipy import interpolate
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import time
import warnings
import joblib
warnings.filterwarnings("ignore")

def chiller_type(NumberOfChiller,CH_TP):
    refrigerant = ['R134a']*NumberOfChiller
    try:
        for i in range(NumberOfChiller):
            if 'DV' in CH_TP: refrigerant[i] = 'R1233zd'
    except: pass
#        print('Error in chiller type information')
    return refrigerant

def taskPool(commonTime, batch_size=10080):

    nums = int((commonTime[1]-commonTime[0])/60+1)
    ts = np.arange(1,nums,batch_size)
    tasks = []
    for i in range(len(ts)-1):
        tasks.append( [int(ts[i]),int(ts[i+1]-1) ] )

    if (len(ts) > 0):
        tasks.append([ int(ts[-1]),nums])
    temp = []
    for i in tasks:
        temp.append(list((np.array(i)-1)*60+commonTime[0]))
    res = {'times':temp,
           'indexs':tasks}
    return res

def Props(a1,a2,a3,a4,a5,a6):
    try:
        if isinstance(a3,pd.Series):
            a3 = np.array(a3)
        if isinstance(a5,pd.Series):
            a5 = np.array(a5)
        r = PropsSI(a1,a2,a3,a4,a5,a6)
        r[np.isinf(r)] = np.nan
        return r
    except:
        return np.nan
    
def Regressor(X, Y, positive):
    
    lr = LinearRegression(positive = positive)
    quadratic = PolynomialFeatures(degree = 2)
    X = quadratic.fit_transform(X)
    lr.fit(X, Y)
    
    return lr
    
def Stable_Data(data,ref,stbt=5):
    
    if 'Power' in data.columns:
        data.Power[data.Power==0] = np.nan
    data['stable'] = data.PLC>0
    data.stable.iloc[:stbt]=0
    data.stable.iloc[-stbt:]=0

    for para in [['SST','SP'],
                 ['SDT','DP']]:
        # 筛选出SST/SDT为NAN的值，通过SP/DP计算来替换
        # data[para[0]][data[para[0]]!=data[para[0]]] = data[para[1]][data[para[0]]!=data[para[0]]].apply(lambda x: Props('T',
        #                                                                                                                 'P',x*1000+101325,
        #                                                                                                                 'Q',0,
        #                                                                                                                 ref)) - 273.15
        if data[para[0]].isnull().max():
            data[para[0]][data[para[0]]!=data[para[0]]] = Props('T',
                                                                'P',data[para[1]][data[para[0]]!=data[para[0]]]*1000+101325,
                                                                'Q',0,
                                                                ref) - 273.15   
    for para in ['PLC']:
        para_dif = data[para].rolling(stbt).max()/data[para].rolling(stbt).min()
        data.stable.loc[(para_dif>=1.1)|(para_dif==1)|(data[para]<30)|(data[para]>100)] = 0
    for para in ['SST','SDT','ECW','LCW','ECDW','LCDW','CDT']:
        try:
            para_dif = data[para].rolling(stbt).max()-data[para].rolling(stbt).min()
            data.stable.loc[(para_dif>=1)|(para_dif==0)|(data[para]<-15)|(data[para]>120)] = 0
        except:
            pass
        
    data = data[(data['stable'] == 1)&(data['stable'].shift(1) == 0)]
        
    return data

def Cal_COP(data, SST, SDT, COP, eta_isen = False, eta_comp='eta_comp', ref='R134a'):
    
    data['SP'] = Props('P','T',data[SST]+273.15,'Q',0,ref)
    data['DP'] = Props('P','T',data[SDT]+273.15,'Q',1,ref)
    data['h_cdo'] = Props('H','P',data['DP'],'Q',0,ref)
    data['h_suc'] = Props('H','P',data['SP'],'Q',1,ref)
    data['s_suc'] = Props('S','P',data['SP'],'Q',1,ref)
    data['h_dis_i'] = Props('H','P',data.DP,'S',data.s_suc,ref)
    if eta_isen:
        data['h_dis'] = Props('H','P',data.DP,'T',data.CDT+273.15,ref)
        data['eta_comp'] = (data.h_dis_i - data.h_suc) / (data.h_dis - data.h_suc)
        data['eta_comp'][data['eta_comp']>0.85] = 0.85
    # else:
    data['h_dis'] = data.h_suc + (data.h_dis_i - data.h_suc) / data[eta_comp]
    data[COP] = (data.h_suc - data.h_cdo) / (data.h_dis - data. h_suc)

    return data

def Cal_HX(data, evap_approach, cond_approach):
    
    data['COOLDT'] = data.ECW - data.LCW
    data['SST'][(data.SST>data.LCW)
                |(data.LCW-data.SST>20)] = data.LCW - 0.1
    data['SDT'][data.SDT<data.LCDW] = data.LCDW + 0.1
    
    return data

def genfolder(fd):
    dirs = ''
    for i in fd:
        dirs += i
        try:
            os.mkdir(dirs)
        except: pass
    return dirs

def Standardization(data, col_y, col_x, col_new, chiller, plot=False, positive = False):
    if col_y in data.columns:
        quadratic = PolynomialFeatures(degree = 2)
        train = data[(data[col_y]==data[col_y])&(data[col_y]<100)]
        for para in col_x.keys():
            train = train[train[para]==train[para]]
        # if ('GV' in train.columns) & ('comp' not in col_y):
        #     train = train[train.GV>60]
        if len(train)>0:
            try:
                dirs = genfolder(['model','/'+chiller])
                lr = joblib.load(dirs+'/%s.joblib'%col_y)
                train['exp'] = lr.predict(quadratic.fit_transform(train[col_x.keys()]))
            except:
                train['exp'] = 1
            
            residuals = []
            for i in range(100):
                train['exp'] = train['exp']/train['exp'].max()
                exp = train['exp'].shift(1)/train[col_y].shift(1)*train[col_y]
                lr = Regressor(train[col_x.keys()].iloc[1:],
                               exp.iloc[1:],
                               positive)
                train['exp'] = lr.predict(quadratic.fit_transform(train[col_x.keys()]))
                residual = ((train['exp']/exp-1)**2).sum()/len(train)
                residuals.append(residual)
                if len(residuals)>2:
                    if ((residuals[-2] - residual)<1E-8)|(residual<1E-3):
                        break
            
            joblib.dump(lr,dirs+'/%s.joblib'%col_y)    
            train[col_new] = train[col_y]/train['exp']*lr.predict(quadratic.fit_transform(np.array(list(col_x.values())).reshape(1,-1)))
            data = data.join(train[[col_new]],how='outer')
            
            if plot:
                plt.figure(figsize=(5,4))
                plt.subplot(211)
                plt.title(col_y.split('_')[0]+' values')
                sns.scatterplot(x=data.index,y=data[col_y],s=5)
                plt.ylim(0,)
                plt.subplot(212)
                plt.title(col_new.split('_')[0]+ ' standardized to standard working condition')
                sns.scatterplot(x=data.index,y=data[col_new],s=5)
                plt.ylim(0,)
                plt.tight_layout()
                plt.savefig('charts/'+chiller +' standardized '+col_new+'.jpg')
                plt.clf
                # plt.scatter(range(len(residuals)),residuals)
                # plt.yscale('log')
                # plt.show()
    
    return data
    
def rule_cop(json):
    
    last_trend_time1 = json['last_trend_time1']
    last_trend_time2 = json['last_trend_time2']
    NumberOfChiller = int(len(json['sensors'])/17)
    CH_TP = json['parameters'][0]['value']
    evap_approach = json['parameters'][1]['value']
    cond_approach = json['parameters'][2]['value']
    ref = chiller_type(NumberOfChiller,CH_TP)
    columns = ['Power','SP','SST','ECW','LCW',
               'DP','SDT','ECDW','LCDW',
               'EP','ET',
               'CDT',
               'CWFlow',
               'PLC','VFD','GV','EXV']
    result = []
    for j in range(NumberOfChiller):
        data = pd.DataFrame(columns = columns)
        for i,para in enumerate(columns):
            try:
                data[para] = json['sensors'][j*17+i]['values']
            except:
                pass
        if data.empty: continue
        data = Stable_Data(data,ref[j])
        if len(data)>0:
            data = Cal_HX(data, evap_approach, cond_approach)
            data = Cal_COP(data, 'SST', 'SDT', 'COP', eta_isen = True)
            data = Cal_COP(data, 'LCW', 'SDT', 'COP_ievap')
            data = Cal_COP(data, 'SST', 'LCDW', 'COP_icond')
            data['eta_evap'] = data['COP'] / data['COP_ievap']
            data['eta_cond'] = data['COP'] / data['COP_icond']
            data['Time'] = data.index+last_trend_time1
            data['COP_w'] = data.CWFlow * data.COOLDT * 4.2 / 15.85 / data.Power
            data['eta_motor'] = data['COP_w'] / data['COP']
            data = data[['Time','LCW','LCDW','ECW','ECDW','SST','SDT','CDT','COP','COP_w','eta_comp','eta_evap','eta_cond','eta_motor','PLC','VFD','GV','EXV']]
            data.rename(columns = {'LCW':'CHST',
                                   'ECW':'CHRT',
                                   'LCDW':'CDLT',
                                   'ECDW':'CDET',
                                   'SST':'T_evap',
                                   'SDT':'T_cond',
                                   'CDT':'T_DC',
                                   'PLC':'PLR'},
                        inplace = True)
            data.dropna(axis=1,how='all',inplace=True)
            data = data.round(3)
            data = data.round({'CHST':1,'CHRT':1,'CDLT':1,'CDET':1,'T_evap':1,'T_cond':1,'T_DC':1})
        result.append(data)
            
    return result

def get_COP(CRT,ERT):
    crt = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
    ert = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
    cop = [[5.949, 4.969, 4.228, 3.646, 3.174, 2.783, 2.451, 2.165, 1.914, 1.69, 1.489, 1.305],
           [7.426, 6.036, 5.036, 4.279, 3.684, 3.202, 2.801, 2.461, 2.167, 1.908, 1.677, 1.469],
           [9.645, 7.533, 6.117, 5.097, 4.325, 3.717, 3.224, 2.813, 2.464, 2.162, 1.895, 1.657],
           [13.35, 9.784, 7.634, 6.191, 5.152, 4.364, 3.743, 3.239, 2.818, 2.46, 2.149, 1.874],
           [20.769, 13.542, 9.915, 7.727, 6.258, 5.199, 4.395, 3.762, 3.246, 2.815, 2.447, 2.127],
           [43.048, 21.069, 13.724, 10.037, 7.811, 6.316, 5.238, 4.419, 3.772, 3.244, 2.802, 2.424],
           [43.048, 43.669, 21.353, 13.893, 10.148, 7.886, 6.365, 5.267, 4.432, 3.771,3.232,	2.778],
           [43.048, 43.669, 44.261, 21.619, 14.049, 10.246, 7.949, 6.403, 5.285, 4.434, 3.759, 3.206],
           [43.048, 43.669, 44.261, 44.819, 21.865, 14.189, 10.331, 7.998, 6.427, 5.29, 4.422, 3.732]]
    f = interpolate.interp2d(crt, ert, cop, kind = 'cubic')
    COP = float(f(CRT, ERT))
    return COP

def group_COP(COP,KEYs,stbn=5):
    groups = []
    for keys,group in COP.groupby(KEYs):
        s = 1
        if len(KEYs)>1:
            for i in keys: s *= i
        else: s = keys
        if (s != 0) & (len(group) >= stbn): groups.append(group)
    groups.sort(key= lambda x:len(x), reverse = True)
    return groups

def COP_RP(db,plantName,i,r=1):
    Chiller_list = db['Device'].find_one({'_id': plantName})['Chillers']
    CH_DB = [CH['_id'] for CH in Chiller_list]
    DEG_ben = [0.9,0.9,0.9,0.85,0.85,0.85,0.9]
    try: DEG_ben = db['Device'].find_one({'_id':plantName})['DEG_ben']
    except: pass
    for CH in CH_DB:
        if not 'chiller' in CH: CH_DB.remove(CH)
    CH_DB = sorted(CH_DB)
    CH_DB.sort(key = len)
    data = pd.DataFrame(list(db['COP'].find({'BusinessKey':CH_DB[i]},{'_id':0})))
    if r:
        if len(data)>0:
            alarm_content = rule_RP(data,CH_DB,DEG_ben,i,r)
        # print(alarm_content)
        chiller = CH_DB[i]
        db['Report'].remove({'AlgFrom': 'CH_Rule_COP_V','BusinessKey':chiller}, multi=True)


        for AC in alarm_content:
            last_end = db['Report'].find({'BusinessKey':chiller,'AlgFrom':'CH_Rule_COP_V','FaultContent':AC['FaultContent']}).sort('EndTime',-1).limit(1)
            try: last_end = last_end[0]['EndTime']
            except: last_end = -1
            if AC['StartTime'] == last_end + 60:
                db['Report'].update_one({'BusinessKey':chiller,'EndTime':last_end,'AlgFrom':'CH_Rule_COP_V','FaultContent':AC['FaultContent']},{'$set':{'EndTime':AC['EndTime']}})
            else:
                db['Report'].insert(AC)
    else:
        plotinfo = rule_RP(data,CH_DB,DEG_ben,i,r)
        return plotinfo
    
def outlier_filter(data,paras):
    
    data['inlier'] = True
    for para in paras:
        if para in data.columns:
            data75 = data[para].rolling(100,1,center = True).quantile(0.75)
            data25 = data[para].rolling(100,1,center = True).quantile(0.25)
            dataH = data75 + 1.5 * (data75 - data25)
            dataL = data25 - 1.5 * (data75 - data25)
            data['inlier'][(data[para]>dataH)|(data[para]<dataL)|(data[para]<=0)] = False
        
    data = data[data['inlier']]
    
    return data

def Cut_Dict(dictionary, key_list):
    return {key: value for key, value in dictionary.items() if key in key_list}
    
def rule_RP(data,CH_DB,DEG_ben,i,r=1):
    chiller = CH_DB[i]
    data = outlier_filter(data, ['COP','COP_w','eta_comp','eta_evap','eta_cond','eta_motor'])
    data['COOLDT'] = data['CHRT'] - data['CHST']
    data['CONDDT'] = data['CDLT'] - data['CDET']
    col_x = {}
    for para in ['T_evap','T_cond','CHST','CHRT','CDLT','CDET','COOLDT','CONDDT','PLR']:
        col_x[para] = data[para].mean()
        data[para+'_n'] = -data[para]
    # if 'GV' in data.columns:
    #     data = data[(data.GV==data.GV)&(data.GV>60)]
    
    # data = Standardization(data, 'COP', Cut_Dict(col_x, ['CHST','CHRT','CDLT','CDET','PLR']), 'COP_std', chiller)
    # data = Standardization(data, 'COP_w', Cut_Dict(col_x, ['CHST','CHRT','CDLT','CDET','PLR']), 'COP_w_std', chiller)
    # data = Standardization(data, 'eta_comp', Cut_Dict(col_x, ['T_evap_n','T_cond','PLR']), 'ETA_comp', chiller, positive = True)
    data['ETA_comp'] = data['eta_comp']
    data['ETA_evap'] = data['eta_evap']
    data['ETA_cond'] = data['eta_cond']
    data[['ETA_comp','ETA_evap','ETA_cond']]=data[['ETA_comp','ETA_evap','ETA_cond']].fillna(1)
    data.dropna(axis=1,how='all',inplace=True)
    # data = Standardization(data, 'eta_evap', Cut_Dict(col_x, ['PLR_n']), 'ETA_evap', chiller, positive = True)
    # data = Standardization(data, 'eta_cond', Cut_Dict(col_x, ['PLR_n']), 'ETA_cond', chiller, positive = True)
    # data = Standardization(data, 'eta_motor', Cut_Dict(col_x, ['CHST','CHRT','CDLT','CDET','PLR']), 'ETA_motor', chiller)
    

    data = outlier_filter(data, ['COP_std','ETA_comp','ETA_evap','ETA_cond','ETA_motor'])
    
    return Alarm_Plot(data,CH_DB,DEG_ben,col_x,i,r)

def Alarm_Plot(data,CH_DB,DEG_ben,col_x,i,r):
    chiller = CH_DB[i]
    alarm_content = []
    for para in [
            # 'COP',
            'COP_w']:
        if para in data.columns:
            data.drop([para],axis=1,inplace=True)
    data.rename(columns = {
        # 'COP_std':'COP',
                           'COP_w_std':'COP_w'},
                inplace = True)
    para_ETA = ['ETA_evap','ETA_cond','ETA_comp','ETA_motor']
    para_DEG = para_ETA + ['COP','COP_w']
    AC_list = {'ETA_evap':['evaporator','1.Please check evaporator heat exchanger status; 2.Please check refrigerant charge status.'],
               'ETA_cond':['condenser','1.Please check condenser heat exchanger status; 2.Please check purge system status (for 19DV chillers).'],
               'ETA_comp':['compressor efficiency','Please check compressor health status.'],
               'ETA_motor':['motor efficiency','1.Please check motor health status; 2.Please check heat insulation of the system.'],
               'COP':['refrigerant side COP','Please check chiller health status.'],
               'COP_w':['water side COP','Please check chiller health status.']}
    limit = {'max':{},
             'ben':{}}
    heatmap = {'xlabel':[],
               'ylabel':[],
               'contour':[],
               'para':[]}
    heatmap['para'] = set(['VFD','GV','EXV']).intersection(set(data.columns))
    heatmap['para'] = list(heatmap['para'])
    heatmap['para'].sort()
    for para in para_DEG:
        limit['max'][para], limit['ben'][para] = [], []

    '''Data regulation'''

    for para in para_ETA:
        if para in data.columns:
            data[para][data[para]>1]=1
    data['ETA_comp'][data['ETA_comp']>0.85] = 0.85

    starttime, endtime = data['Time'].min(), data['Time'].max()

    chst, cdlt, plr = [col_x[para] for para in ['CHST', 'CDLT', 'PLR']]
    max_eta_cond = get_COP(cdlt+3/1.8,chst)/get_COP(cdlt,chst)
    max_eta_evap = get_COP(cdlt,chst-3/1.8)/get_COP(cdlt,chst)
    max_COP = 0.8 * (chst + 273) / (cdlt - chst)

    '''COP regulation'''

    for para in ['COP','COP_w']:
        if para in data.columns:
            data[para][data[para]>max_COP]=max_COP

    if len(data)>5:
        if r:
            info = {'AlgFrom':'CH_Rule_COP_V',
                    'Level':'high',
                    'BusinessKey':chiller,
                    'Version':'V3.2.1'}

        '''Degradation check'''

        for j, para in enumerate(para_DEG):
            if para in data.columns:
                if para == 'COP': continue
                maxi = max(data[para][(data[para] == data[para])].rolling(max(100,len(data)//20),
                                                                          max(30,len(data)//50),
                                                                          center=True).median())
                if maxi > max_COP: maxi = max_COP
                if (para == 'ETA_cond') & (maxi < max_eta_cond): maxi = max_eta_cond
                if (para == 'ETA_evap') & (maxi < max_eta_evap): maxi = max_eta_evap
                data[para][data[para]>maxi] = maxi
                ben = DEG_ben[j] * maxi
                limit['max'][para] = maxi
                limit['ben'][para] = ben
        
        data['COP'] = 1
        for para in ['ETA_evap','ETA_cond','ETA_comp']:
            data['COP'] -= (1-data[para]/limit['max'][para])
        limit['max']['COP'] = 1
        limit['ben']['COP'] = DEG_ben[4]

        for j, para in enumerate(para_DEG):
            if para in data.columns:        
                if r&(para not in ['COP_w','ETA_motor']):
                    alarm = pd.DataFrame(data.Time)
                    alarm['alarm'] = (data[para] < limit['ben'][para])
                    alarm['n'] = (alarm.alarm & (alarm.alarm.shift(1)==0)).cumsum()
                    alarm = alarm[alarm.alarm]
                    alarm['n'] = alarm.alarm.groupby(alarm.n).cumsum()
                    alarm = alarm[(alarm.n==1)|(~(alarm.n<alarm.n.shift(-1)))]
                    alarm['dt'] = alarm.Time-alarm.Time.shift(1)
                    alarm = alarm[(alarm.dt>60*60*6)&(alarm.n>=30)]
                    for k in range(len(alarm)):
                        temp = {'FaultContent': chiller + ' ' + AC_list[para][0] + ' performance degradation.',
                                'Suggestion': AC_list[para][1],
                                'StartTime':alarm.Time.iloc[k]-alarm.dt.iloc[k],
                                'EndTime':alarm.Time.iloc[k],
                                }
                        temp.update(info)
                        alarm_content.append(temp)

    '''heatmap data'''

    if (not r) & (len(heatmap['para']) == 2):
        heatmap['xlabel'] = [int(data[heatmap['para'][0]].min()),int(data[heatmap['para'][0]].max())]
        heatmap['ylabel'] = [int(data[heatmap['para'][1]].min()),int(data[heatmap['para'][1]].max())]
        contour = []
        for ii in range(heatmap['ylabel'][0],heatmap['ylabel'][1]+1):
            contour.append([])
            for jj in range(heatmap['xlabel'][0],heatmap['xlabel'][1]+1):
                contour_datum = data['ETA_comp'][(data[heatmap['para'][0]].round()==jj)&(data[heatmap['para'][1]].round()==ii)]
                if len(contour_datum) > 0:
                    contour[-1].append(min(1,contour_datum.mean()/limit['max']['ETA_comp']))
                else:
                    contour[-1].append(np.nan)
        heatmap['contour'] = np.array(contour)

    '''Control optimize opportunity'''

    if r:
        for para in heatmap['para']:
            data[para] = data[para].round()
            deg_ctrl = 0
            if 'ETA_comp' in data.columns:
                groups_ctrl = group_COP(data[data['ETA_comp']>0],[para],30)
                if len(groups_ctrl)>0:
                    for j, _ in enumerate(groups_ctrl):
                        groups_ctrl[j] = groups_ctrl[j]['ETA_comp'].mean()
                    if min(groups_ctrl)/max(groups_ctrl) < DEG_ben[6]: deg_ctrl = 1
            if deg_ctrl:
                temp = {'FaultContent':'Opportunity in improving '+chiller+' efficiency by optimizing ' + para + ' control strategy',
                        'Suggestion':'Optimize ' + para + ' control strategy'}
                info['StartTime'] = starttime
                info['EndTime'] = endtime
                info['BusinessKey']=CH_DB[i]
                temp.update(info)
                alarm_content.append(temp)
                break
        return alarm_content
    else:
        return {'data': data, 'limit': limit, 'CH_DB': CH_DB, 'heatmap':heatmap}

def plot_COP(data,i):
    
    df = data['data']
    # df['COP'][((df.Time-df.Time.shift(1))>5*24*60*60)
    #           |((df.Time.shift(-1)-df.Time)>5*24*60*60)
    #           ] = data['limit']['max']['COP']
    for para in ['COP','COP_w','ETA_cond','ETA_evap','ETA_comp','ETA_motor']:
        if para in df.columns:
            df[para][df[para]>data['limit']['max'][para]] = data['limit']['max'][para]
            df[para][((df.Time-df.Time.shift(1))>2*24*60*60)
                     |((df.Time.shift(-1)-df.Time)>2*24*60*60)] = data['limit']['max'][para]*1.1
            # if para in ['COP','COP_w']:
            #     df = df[df[para]>0.5*data['limit']['max'][para]]
    x = df['Time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    
    # x = data['groups'][k]['Time']/60/60/24
    # s = min(x)
    # x -= s
#    x = data['groups'][k]['Time']
    # x_max, x_min = list(x)[-1],list(x)[0]
    # CHST, CDLT, PLR = [[] for k in range(3)]
    # for j in range(len(data['groups'])):
    #     try:
    #         for para in ['CHST','CDLT','PLR']:
    #             exec(para+".append(round(list(data['groups'][j]['"+para+"'])[0]))")
    #     except: pass

    '''Plot ETA COP'''

    # for para in ['COP','COP_w','ETA_motor','ETA_comp','ETA_evap','ETA_cond']:
    #     try:
    #         y = data['groups'][k][para]
    #         ben = data['limit']['ben'][para]
    #         plt.figure(figsize=(10,4))
    #         plt.scatter(x,y,s=10)
    #         plt.axis()
    #         plt.grid()
    #         plt.title(data['CH_DB'][i])
    #         plt.axhline(ben,color='r')
    #         # if para[:3] == 'ETA':
    #         #     if para[-4:] == 'comp': plt.ylim(0.6,1)
    #         #     elif para[-5:] == 'motor': plt.ylim(0.7,1.1)
    #         #     else: plt.ylim(0.8,1.1)
    #         plt.ylim(0,)
    #         plt.ylabel(para)
    #         plt.xlabel('time/d')
    #         plt.show()
    #     except: pass

    '''Plot COP COP_w'''

    plt.figure(figsize=(10,4))
    for para in ['COP','COP_w']:
        try:
            y = df[para]/data['limit']['max'][para]
            plt.scatter(x,y,label=para,s=10)
        except: continue
    plt.legend(loc = 'upper right')
    plt.axis()
    plt.grid()
    plt.title(data['CH_DB'][i])
    try:
        ben = data['limit']['ben']['COP']/data['limit']['max']['COP']
        plt.axhline(y = ben,color='r')
    except: pass
    plt.ylim(0.5,1)
    plt.ylabel('COP')
    plt.xlabel('time/d')
    plt.savefig('charts/'+data['CH_DB'][i]+' COP std degradation.jpg')
    plt.clf()

    '''Plot degradation distribution'''

    df_dist = df[df.COP==df.COP]
    plt.figure(figsize=(10,4))
    x = df_dist['Time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    y = []
    for para in ['ETA_cond','ETA_evap','ETA_comp']:
        if para in df_dist.columns:
            df_dist[para+'_deg'] = 1 - df_dist[para]/data['limit']['max'][para]
            df_dist[para+'_deg'][df_dist[para+'_deg']!=df_dist[para+'_deg']] = 0
            df_dist[para+'_deg'][df_dist[para+'_deg']<0] = 0
    ETA_total = df_dist[['ETA_cond_deg','ETA_evap_deg','ETA_comp_deg']].apply(lambda x: x.sum(),axis=1)
    for j, para in enumerate(['ETA_cond','ETA_evap','ETA_comp','ETA_motor']):
        try:
            if para in ['ETA_motor']:
                y.append((1-df_dist[para]/data['limit']['max'][para])*100)
            else:
                y.append((1-df_dist['COP']/data['limit']['max']['COP'])/ETA_total*df_dist[para+'_deg']*100)
            if j == 0: plt.fill_between(x,y[0],label=para[4:]+'_loss')
            else: plt.fill_between(x,sum(y),sum(y[:-1]),label=para[4:]+'_loss')
        except: continue
    
    # for j, para in enumerate(['ETA_cond','ETA_evap','ETA_comp','ETA_motor']):
    #     try:
    #         if para in ['ETA_motor']:
    #             y.append((1-df_dist[para]/data['limit']['max'][para])*100)
    #         else:
    #             y.append((1-df_dist[para]/data['limit']['max'][para])*100)
    #         if j == 0: plt.fill_between(x,y[0],label=para[4:]+'_loss')
    #         else: plt.fill_between(x,sum(y),sum(y[:-1]),label=para[4:]+'_loss')
    #     except: continue
    
    plt.legend(loc='upper left')
    plt.axis()
    plt.grid()
    plt.title(data['CH_DB'][i] +' COP loss')
    plt.ylabel('COP loss/%')
    plt.xlabel('time/d')
    plt.ylim(0,50)
    plt.savefig('charts/'+data['CH_DB'][i]+' COP degradation distribution.jpg')
    plt.clf()
    
    '''Plot control optimization'''

    plt.figure(figsize=(10,4))
    pending = 0
    for para in ['VFD','GV','EXV']:
        for para1 in ['ETA_comp']:
            try:
                # y = data['groups'][k][para1]/data['limit']['max'][para1][k]
                y = df[para1]/data['limit']['max'][para1]
                x = df[para]
                plt.scatter(x,y,label = para + ' Vs. '+para1,s=10)
                pending =1
            except: continue
    if pending:
        plt.axhline(y = data['limit']['ben']['ETA_comp']/data['limit']['max']['ETA_comp'],color='r')
        plt.legend(loc = 'upper right')
        plt.axis()
        plt.grid()
        plt.title(data['CH_DB'][i])
        plt.ylabel('ETA_comp')
        plt.xlabel('Per')
        plt.ylim(0,1)
        plt.savefig('charts/'+data['CH_DB'][i]+'compressor control.jpg')
        plt.clf()

    '''Control contour'''

    if data['heatmap']['contour'] != []:
        plt.figure(figsize=(10,4))
        plt.pcolor(np.arange(data['heatmap']['xlabel'][0],data['heatmap']['xlabel'][1]+2)-0.5,
                   np.arange(data['heatmap']['ylabel'][0],data['heatmap']['ylabel'][1]+2)-0.5,
                   data['heatmap']['contour'],
                   cmap='RdYlGn')
        plt.colorbar()
        plt.title(data['CH_DB'][i]+'\nETA_comp Vs. '+data['heatmap']['para'][0]+' & '+data['heatmap']['para'][1])
        plt.xlabel(data['heatmap']['para'][0])
        plt.ylabel(data['heatmap']['para'][1])
        plt.savefig('charts/'+data['CH_DB'][i]+'compressor contour.jpg')
        plt.clf

def chart_info(collection,i,k=0):
    info = COP_RP(collection,i,0)
    plot_COP(info,i,k)
    return info

def COP_DEG(db,plantName,starttime):
    try:
        Chiller_list = db['Device'].find_one({'_id':plantName})['Chillers']
        CH_DB=[CH['_id'] for CH in Chiller_list]
        try:
            rule_parameters = db['Device'].find_one({'_id':plantName})['rule_parameters']['CH_Rule_COP_V']
        except:
            rule_parameters = {'parameters':[0,0]}
        for CH in CH_DB:
            if not 'chiller' in CH: CH_DB.remove(CH)
        CH_DB = sorted(CH_DB)
        CH_DB.sort(key = len)
        ID_DB = CH_DB + [plantName]

        def getCommonTime(targets, starttime):
            starts = []
            ends = []
            for target in targets:
                for i in db['Telemetry'].find({'BusinessKey':target,'_id':{'$gte':starttime}},{'_id':1}).sort('_id',1).limit(1):
                    starts.append(i['_id'])
                for i in db['Telemetry'].find({'BusinessKey':target,'_id':{'$gte':starttime}},{'_id':1}).sort('_id',-1).limit(1):
                    ends.append(i['_id'])
            return min(starts),max(ends),min(ends)

        commonTime = getCommonTime(ID_DB, starttime)

        tasks = taskPool(commonTime)

        paras = {
                'plant':['DPM_pow'],
                'chiller':['Evap_Pressure','Evap_Sat_Temp','Entering_Chilled_Water','Leaving_Chilled_Water',
                           'Cond_Pressure','Cond_Sat_Temp','Entering_Condenser_Water','Leaving_Condenser_Water',
                           'Economizer_Pressure','Economizer_Gas_Temp',
                           'Comp_Discharge_Temp',
                           'Chilled_Water_Flow',
                           'Percent_Line_Current','Actual_VFD_Speed_Per','GV1_Position','EXV_Position']
                }

        fddress = [(pd.DataFrame(columns=('T_evap','T_cond','PLR'))) for i in range(len(CH_DB))]
        for task in tasks['times']:
            idx = tasks['times'].index(task)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' '+str(round(idx/(len(tasks['times']))*100))+'% complete')
            s = task[0]
            e = task[1]
            nums = (e-s)/60+1
            ids = np.arange(s,e+60,60)
            idxs = np.arange(nums)
            CH_TP = []
            res = {}

            try:
                for chiller in CH_DB:
                    CH_TP.append(pd.DataFrame(db['Device'].find_one({'_id': plantName})['Chillers']).set_index('_id').loc[chiller,'Type'])
            except: pass

            res = pd.DataFrame(idxs,index=ids,columns=['IDX'])
            for i,chiller in enumerate(CH_DB):
                try:
                    temp = pd.DataFrame(list(db['Telemetry'].find({'BusinessKey':plantName,'_id':{'$gte':s,'$lte':e}},{'CH'+str(i+1)+'_DPM_pow':1,'_id':1})))
                    temp.set_index('_id',inplace=True)
                    temp.fillna(0)
                    res = pd.concat([res,temp],axis=1)
                # except: pass
                # try:
                #     res['CH'+str(i+1)+'_DPM_pow']
                except: pass

            del res['IDX']
            res = res.sort_index()

            res_ch = {}
            chtemp = {}
            for chiller in CH_DB:
                res_ch[chiller] = pd.DataFrame(idxs,index=ids,columns=['IDX'])
                for para in paras['chiller']:
                    try:
                        chtemp = list(db['Telemetry'].find({'BusinessKey':chiller,'_id':{'$gte':s,'$lte':e}},{para:1,'_id':1}))
                        chtemp = pd.DataFrame(chtemp)
                        chtemp.set_index('_id',inplace=True)
                        chtemp.fillna(0)
                        res_ch[chiller] = pd.concat([res_ch[chiller],chtemp],axis=1)
                        res_ch[chiller][para]
                        if para in ['Evap_Sat_Temp','Entering_Chilled_Water','Leaving_Chilled_Water','Cond_Sat_Temp','Entering_Condenser_Water','Leaving_Condenser_Water','Economizer_Gas_Temp','Comp_Discharge_Temp',]:
                            res_ch[chiller][para]=(res_ch[chiller][para]-32)/1.8
                        elif para in ['Evap_Pressure','Cond_Pressure','Economizer_Pressure']:
                            res_ch[chiller][para]=res_ch[chiller][para]*6.89476
                    except: pass
                del res_ch[chiller]['IDX']
                res_ch[chiller].sort_index(inplace=True)

            # ---------- JS 输入数据定义 ------------------------------#
            data = {'parameters': [{'value': CH_TP},{'value': rule_parameters['parameters'][0]},{'value': rule_parameters['parameters'][1]}],
                    'last_trend_time1': tasks['indexs'][idx][0],
                    'last_trend_time2': tasks['indexs'][idx][1],
                    'sensors': []
                    }

            for i, chiller in enumerate(CH_DB):
                for para in paras['plant']:
                    try:
                        val = res['CH'+str(i+1)+'_DPM_pow'].tolist()
                    except:
                        val = []
                    data['sensors'].append({'display_name': 'CH'+str(i+1)+'_DPM_pow',
                                            'values': val})
                for para in paras['chiller']:
                    try:
                        val = res_ch[chiller][para].tolist()
                    except:
                        val = []
                    data['sensors'].append({'display_name': 'chiller #{} '.format(i + 1)+para,
                                            'values': val})

            # end = time.time()
            # print(str(end-start))
            try:
                fddres = rule_cop(data)
                for i, _ in enumerate(CH_DB):
                    try:
                        fddres[i]['Time'] = fddres[i]['Time']*60+commonTime[0]-60
                        fddres[i]['BusinessKey']=_
                        fddress[i]=pd.concat([fddress[i],fddres[i]])
                    except:continue
            except: 
                pass

        for i, chiller in enumerate(CH_DB):
            db['COP'].remove({'BusinessKey':chiller},multi=True)
            if not len(fddress[i]) == 0:
                db['COP'].insert_many(fddress[i].to_dict('records'))

        return True,commonTime[2]
    except:
        return False,starttime

def Main(db,plantName,starttime):
    runinfo,time = COP_DEG(db,plantName,starttime)
    try:
        Chiller_list = db['Device'].find_one({'_id': plantName})['Chillers']
        CH_DB = [CH['_id'] for CH in Chiller_list]
        CH_DB = sorted(CH_DB)
        CH_DB.sort(key = len)
        for i, _ in enumerate(CH_DB):
            try:
                COP_RP(db,plantName,i,1)
                # plot_info = COP_RP(db,plantName,i,0)
                # plot_COP(plot_info,i)
            except:
                print(_,'failed')
                continue
    except:
        print('COP_RP failed.')
    return runinfo,time,''

if __name__ == '__main__':
    
    import pymongo as mg
    db_auth = False
    db_ip = '192.168.168.213'  # '192.168.168.218'
    db_port = 27017
    print('Connecting to Data Base . . .')
    conn = mg.MongoClient(db_ip, db_port) # database ip and port
    db = conn.admin
    # db.authenticate("username", "password", mechanism='SCRAM-SHA-1') # 2.X version:MONGODB-CR; 3.X version:SCRAM-SHA-1
    try:
        db.authenticate("root", "root", mechanism='SCRAM-SHA-1')
        db_auth = True
    except Exception as e :
        db_auth = False
        print(e)
    db=conn.ChillerPlantDataV3
    # r = Main(conn.ChillerPlantData['plant_Orchard_plt1'], 0)
    # plts = pd.DataFrame(list(db['Device'].find({},{'_id':1})))['_id']
    plts = ['plant_Amara Hotel_plt1',
            'plant_Marina Sq_plt1',
            'plant_T1_MainPlant_plt1',
            'plant_SRDC_lytest_plt1',
            'plant_Changi Airport Terminal 4_plt1',
            'plant_Far East Shopping Centre_plt1',
            'plant_Grand Copthorne Waterfront Hotel_plt1',
            'plant_Liat Towers_plt1',
            'plant_Orchard_plt1',
            'plant_Sheraton Towers_plt1',
            'plant_National Heart Centre_plt1',
            'plant_GrandParkCityHotel_plt1',
            'plant_DHL_plt1',
            'plant_BeachCentre_plt1',
            'plant_SCO_plt1',
            'plant_Siglap Centre_plt1',]
    for plantName in plts:
        r = Main(db,plantName, 0)
    # start = time.time()
    # conn = mg.MongoClient('localhost', 27017)
    # db = conn.admin
    # db.authenticate('mongorootuser', '#m0n90$tr0ng#p!$$w0rd')
    # print('localhost connect successfully')
    # # conn = mg.MongoClient(
    # #     f"mongodb://gotest:KkshLnnBJCmqZx3poWl237Mk0MUygi0KDzWludlYDpIqQsYWstX4xHalL2sCUbYRghYaNDv3t7iW1D2cvxV1lg==@10.0.3.5:10255/?ssl=true",ssl_cert_reqs=ssl.CERT_NONE)  # host uri
    # # # f"mongodb://gotest:KkshLnnBJCmqZx3poWl237Mk0MUygi0KDzWludlYDpIqQsYWstX4xHalL2sCUbYRghYaNDv3t7iW1D2cvxV1lg==@gotest.mongo.cosmos.azure.com:10255/?ssl=true")  # host uri
    # # print('Azure connect successfully')
    # dbs = conn.ChillerPlantData
    # plantName = 'plant_HN1592_plt1'
    # collection = dbs[plantName]
    # # r = chart_info(collection,0,k=0)
    # r = Main(collection, 0)
    # end = time.time()
    # print(str(end - start))
#     import sys
#     import json
#     with open(sys.argv[1], 'r') as f:
# #    with open('Data.txt',"r") as f:
#         data = f.read()
#     DEG_ben = [0.9,0.9,0.9,0.85,0.85,0.85,0.9]
#     data = json.loads(data)
#     fddress = rule_cop(data)
#     CH_DB = []
#     for i, fddres in enumerate(fddress):
#         CH_DB.append('Chiller#'+str(i+1))
#         try:
#             copres = pd.read_csv('D:\\fdd_log\\COP_'+CH_DB[-1]+'.csv')
#             try:
#                 del copres['Unnamed: 0']
#             except: pass
#             copres1 = copres[copres.Time<data['last_trend_time1']]
#             copres2 = copres[copres.Time>data['last_trend_time2']]
#             copres = pd.concat([copres1,fddres],ignore_index=True)
#             copres = pd.concat([copres,copres2],ignore_index=True)
#             copres.to_csv('D:\\fdd_log\\COP_'+CH_DB[-1]+'.csv')
#         except:
#             fddres.to_csv('D:\\fdd_log\\COP_'+CH_DB[-1]+'.csv')
#     alarm_contents = []
#     for i in range(len(fddress)):
#         data_COP = pd.read_csv('D:\\fdd_log\\COP_Chiller#'+str(i+1)+'.csv')
#         try:
#             del data_COP['Unnamed: 0']
#         except: pass
#         try:
#             alarm_contents=alarm_contents+rule_RP(data_COP,CH_DB,DEG_ben,i)
#         except:pass
#     rule_change_records = []
#     for alarm_content in alarm_contents:
#         jasonRule = {
#                 'rule_status': True,
#                 'rule_status_changetime': alarm_content['StartTime'],
#                 'rule_status_message': alarm_content['FaultContent']
#                 }
#         rule_change_records.append(jasonRule)
#         jasonRule = {
#                 'rule_status': False,
#                 'rule_status_changetime': alarm_content['EndTime'],
#                 'rule_status_message': 'Return to normal.'
#                 }
#         rule_change_records.append(jasonRule)
#     ruleDataReturn = {
#     'rule_status': False,
#     'rule_change_records': rule_change_records,
#     'rule_delay_pendings': []
#     }
#
#     print(ruleDataReturn)
