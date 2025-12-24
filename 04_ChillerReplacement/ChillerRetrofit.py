# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:24:43 2023

@author: chens6
"""

import COP_DEG as COP
import os
import joblib
import pandas as pd
import numpy as np
import datetime
from advanced_data_analytics_tool import Rename_Data
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from CoolProp.CoolProp import PropsSI

import time
from dateutil import parser
def Ecat_map(chtp='19XR', tonnage='600'):
    '''
    Read chiller map data from local file.

    Parameters
    ----------
    chtp : String, optional
        Chiller type: '19XR' for fix speed, '19XRV' for variable speed. 
        The default is '19XR'.
    tonnage : string, optional
        Tonnage of chiller. The default is '600'.

    Returns
    -------
    joblib
        Chiller map regressor.

    '''
    # fn = 'Ecatdata/10coe'
    # if chtp == '19XR':
    #     fn += '/定频/%dTons.xlsx'%tonnage
    # elif chtp == '19XRV':
    #     fn += '/变频/%dTons.xlsx'%tonnage
    # clms = {'COP':'COP',
    #         'PLR':'PLR',
    #         'LWTe':'LCW',
    #         'EWTc':'ECDW'}
    # ecat = pd.read_excel(fn,sheet_name='Eff(10)')
    # ecat = ecat[ecat.columns[:6]]
    # ecat.columns = ecat.iloc[0]
    # ecat = ecat[clms.keys()]
    # ecat = ecat.iloc[2:]
    # ecat.rename(columns = clms, inplace=True)
    # # ecat = ecat[clms.values()]

    # ecat.dropna(how='any',inplace=True)
    # # ecat.columns=['PLR','COP','LCW','ECDW']

    # # regressor = KNNR(5,weights='distance')
    # regressor = KNNR(radius = 5,weights = 'distance')
    # ecat = ecat.astype('float')
    # ecatx = ecat[ecat.PLR==1]
    # LCWn = 7
    # ECDWn = 30
    # if not ecatx.empty:
    #     Q_evapn = PropsSI('H','T',LCWn+273.15,'Q',1,'R134a') - PropsSI('H','T',ECDWn+273.15,'Q',0,'R134a')
    #     Q_evapn *= PropsSI('D','T',LCWn+273.15,'Q',1,'R134a')
    #     Q_evap = Props('H','T',ecatx.LCW+273.15,'Q',1,'R134a') - Props('H','T',ecatx.ECDW+273.15,'Q',0,'R134a')
    #     Q_evap *= Props('D','T',ecatx.LCW+273.15,'Q',1,'R134a')
    #     ecatx.PLR = ecatx.PLR/Q_evapn*Q_evap
    #     if chtp == '19XRV':
    #         ecatx.PLR *=20
    #         knr = joblib.load('ecat/19XR/%dTon.joblib'%(tonnage))
    #         ecatx.COP = knr.predict(ecatx[['PLR','LCW','ECDW']])
    #         ecatx.PLR /=20
    #     ecat = pd.concat([ecat,ecatx])

    # ecat.PLR = ecat.PLR*20

    # regressor.fit(ecat[['PLR','LCW','ECDW']],ecat.COP)
    # try:
    #     os.mkdir('ecat')
    # except:
    #     pass
    # try:
    #     os.mkdir('ecat/%s'%chtp)
    # except:
    #     pass
    # joblib.dump(regressor,'ecat/%s/%sTon.joblib'%(chtp,tonnage))

    # ecat['COP_pre'] = regressor.predict(ecat[['PLR','LCW','ECDW']])
    # plt.title('%s %d ton COP (LCW = 7 C)'%(chtp,tonnage))
    # sns.scatterplot(ecat.PLR/20,ecat.ECDW,ecat.COP,palette='rainbow')
    # plt.show()       

    return joblib.load('ecat/%s/%dTon.joblib' % (chtp, tonnage))


def Ecat_COP(data, new_col='psm_cop', chtp='19XR', tonnage='600', PLR='PLR', LT='LCW', ECT='ECDW'):
    '''
    Get COP from working condition and chiller map.

    Parameters
    ----------
    data : DataFrame
        Input data.
    new_col : string, optional
        Column name of the calculated COP. The default is 'psm_cop'.
    chtp : string, optional
        '19XR' for fix speed chiller,
        '19XRV' for variable speed chiller.
        The default is '19XR'.
    tonnage : string, optional
        Chiller tonnage. The default is '600'.
    PLR : string, optional
        Column name for percent line current. The default is 'PLR'.
    LT : string, optional
        Column name for leaving water temperature. The default is 'LCW'.
    ECT : string, optional
        Column name for entering condenser water temperature. The default is 'ECT'.

    Returns
    -------
    data : DataFrame
        Output data.

    '''
    tons = [600, 650, 700, 750, 800, 900, 1000, 1100, 1700, 2000, 2100, 2300, 2400, 2500, 2600, 2700, 2800, 2900,
            3000]
    f = interp1d(tons, tons, kind='nearest', bounds_error=False, fill_value='extrapolate')
    tonnage = f([tonnage])[0]
    regressor = Ecat_map(chtp, tonnage)
    data.dropna(subset=[PLR, LT, ECT], inplace=True)
    data[PLR] = data[PLR] * 0.2
    # data = data.astype('float')
    data[new_col] = regressor.predict(data[[PLR, LT, ECT]])
    data[PLR] = data[PLR] / 0.2
    return data,tonnage

def Convert_Unit(df, fn='para_unit_f.csv'):
    # 因为SA项目的输入数据单位为公制，所以把以下comment了
    # para_unit = pd.read_csv(fn, index_col=0)
    # for col in df.columns:
    #     # if col == 'SP':
    #     #     print('col', col, para_unit)
    #     unit = ''
    #     if col in para_unit.index:
    #         unit = para_unit.loc[col, 'Unit']
    #     if unit == 'F':
    #         df.loc[df[col] == 0, col] = np.nan
    #         df[col] = (df[col]-32)/1.8
    #     elif unit == 'dF':
    #         df.loc[df[col] == 0, col] = np.nan
    #         df[col] /= 1.8
    #     elif unit == 'psi':
    #         df.loc[df[col] == 0, col] = np.nan
    #         df[col] *= 6.894757
    #     elif unit == 'Pa':
    #         df.loc[df[col] == 0, col] = np.nan
    #         df[col] /= 1000
    #         df[col] -= 101.325
    for para in [['SST','SP'],
                 ['SDT','DP']]:
        if para[0] not in df.columns:
            df[para[0]] = np.nan

        if df[para[0]].isnull().max():
            if para[1] in df.columns:
                df[para[0]][df[para[0]]!=df[para[0]]] = COP.Props('T',
                                                              'P',df[para[1]][df[para[0]]!=df[para[0]]]*1000+101325,
                                                              'Q',0,
                                                             ref) - 273.15 

    return df

def rule_cop(df):
    
    df = df[(df.PLC>30)&
            ((df.SDT-df.SST)>10)&
            (df.SST<20)&
            (df.CDT>df.SDT)]
    if df.empty:
        raise ValueError
    df = COP.Cal_HX(df, 0, 0)
    df = COP.Cal_COP(df, 'SST', 'SDT', 'COP', eta_isen = True)
    df = COP.Cal_COP(df, 'LCW', 'SDT', 'COP_ievap')
    df = COP.Cal_COP(df, 'SST', 'LCDW', 'COP_icond')
    df['eta_evap'] = df['COP'] / df['COP_ievap']
    df['eta_cond'] = df['COP'] / df['COP_icond']
    df.rename(columns = {'LCW':'CHST',
                           'ECW':'CHRT',
                           'LCDW':'CDLT',
                           'ECDW':'CDET',
                           'SST':'T_evap',
                           'SDT':'T_cond',
                           'CDT':'T_DC',
                           'PLC':'PLR'},
                inplace = True)
    # df.dropna(axis=1,how='all',inplace=True)

    return df

def rule_cop1(df):
    
    df = df[(df.PLC>30)&
            ((df.SDT-df.SST)>10)&
            (df.SST<20)&
            (df.CDT>df.SDT)]
    if df.empty:
        raise ValueError
    df = COP.Cal_HX(df, 0, 0)
    df = COP.Cal_COP(df, 'SST', 'SDT', 'COP', eta_isen = True)
    eta_comp = df.eta_comp
    df['eta_comp'] = 0.85
    df = COP.Cal_COP(df, 'LCW', 'LCDW', 'COP_i')
    df['eta'] = df['COP'] / df['COP_i']
    df['eta_comp'] = eta_comp

    return df

def Read_Data(folder):
    
    try:
        os.mkdir(folder['op'])
    except:
        pass
    try:
        os.mkdir('charts')
    except:
        pass
    
    fnss = os.walk(folder['data'])
    des = []
    acs = []
    for root, dirs, fns in fnss:
        # if not '2022' in root: continue
        for fn in fns:
            print(fn)
            # if not '0107Q73487.csv' in fn: continue
            df = pd.read_csv(os.path.join(root, fn))
            df = Rename_Data(df)
            df = df.groupby(df.columns, axis=1).last()
            df = Convert_Unit(df)
            # try:
            #df['DateTime'] = df['DateTime'].apply(
                #lambda x: datetime.datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M:%S'))
            df['DateTime'] = df['eventdatetime'].apply(
                lambda x: parser.parse(x).strftime('%Y-%m-%d %H:%M:%S'))
            # except:
            #     pass
    
            df['DT'] = df['DateTime']
            df['Time'] = (df['DT']-datetime.datetime(1970,1,1)).dt.total_seconds()
            df.set_index('DT',inplace=True)
            df = df.sort_index()
            df = df.resample('15min').ffill(limit=1)
            df.dropna(how='all', inplace=True)
            de = df.describe()
            de['fn'] = fn
            de['root'] = root
            des.append(de)
            try:
                df = rule_cop(df)
                if fn in os.listdir(folder['op']):
                    df1 = pd.read_csv(os.path.join(folder['op'],fn),
                                      index_col=0)
                    df1['DT'] = pd.to_datetime(df1['DateTime'])
                    df1.set_index('DT',inplace=True)
                    df = pd.concat([df1,df])
                    df = df.sort_index()
                if not df.empty:
                    df.to_csv(os.path.join(folder['op'],fn))
                    try:
                        alarmcontent = COP.rule_RP(df,[fn[:-4]],DEG_ben,0)
                        acs += alarmcontent
                        print(alarmcontent)
                        plot_info = COP.rule_RP(df,[fn[:-4]],DEG_ben,0,0)
                        COP.plot_COP(plot_info,0)
                    except:
                        print('RP failed')

            except:
                print('rule_cop failed')
            
            
    describe = pd.concat(des)
    describe.to_csv('describe.csv')
    
    return acs

def Read_Data1(folder):
    
    char_folder = 'charts_final'
    try:
        os.mkdir(folder['op'])
    except:
        pass
    try:
        os.mkdir(char_folder)
    except:
        pass
    
    fnss = os.walk(folder['data'])
    des = []
    acs = []
    summaries = []
    
    YOM = pd.read_csv('summary_v4.csv',index_col=0)
    for root, dirs, fns in fnss:
        # if not '2023' in root: continue
        for fn in fns:
            print(fn)
            # if fn[:4]!='0211': continue
            # if not '0421Q28503' in fn: continue
            df = pd.read_csv(os.path.join(root, fn))
            df = Rename_Data(df)
            # df['DateTime'] = df['DateTime'].apply(
            #     lambda x: datetime.datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M:%S'))
            df['DateTime'] = df['DateTime'].str.split('+',expand=True)[0]
            df['DateTime'] = pd.to_datetime(df['DateTime'],format = '%Y-%m-%d %H:%M:%S')
            df.set_index('DateTime',inplace=True)
            
            df = df.sort_index()
            sn = df['Serialnumber'].mode()[0]
            df.drop('Serialnumber',axis=1,inplace=True)
            df = df.groupby(df.columns, axis=1).max()
            
            df = Convert_Unit(df)
            
            df = df[~df.index.duplicated(keep='first')]
            df = df.resample('15min').first()
            df.dropna(how='all', inplace=True)
            df['Year'] = df.index.year
            df['Serialnumber'] = sn
            # de = df.describe()
            # de['fn'] = fn
            # de['root'] = root
            # des.append(de)
            try:
                df = rule_cop1(df)
                de = df.describe()
                de['fn'] = fn
                de['root'] = root
                des.append(de)
                
                df23 = df[df.Year==2023] 
                summary = {'SN':[sn],
                            # 'Control error':[((df23.LCW-df23['Control Point'])>1).sum()/len(df23)],
                            # 'YOM':[YOM.loc[sn,'Age']],
                            # 'runhour':df.Hrs.max(),
                            # 'Average eta':[df23['eta'].mean()]
                            }
                if sn in YOM.index:
                    summary['YOM'] = [YOM.loc[sn,'Age']]
                if 'Hrs' in df.columns:
                    summary['total runhour'] = [df.Hrs.max()]
                    summary['runhours'] = [df.Hrs.max()-df.Hrs.min()]
                if 'Control Point' in df.columns:
                    if 'LCW' in df.columns:
                        summary['Control error'] = [((df23.LCW-df23['Control Point'])>1).sum()/len(df23)]
                if 'eta' in df.columns:
                    summary['Average eta'] = [df23['eta'].mean()]
                    summary['Average eta 80'] = [df23.loc[df23.PLC>80,'eta'].mean()]
                    summary['Average eta 90'] = [df23.loc[df23.PLC>90,'eta'].mean()]
                    if 'GV' in df.columns:
                        summary['Average eta GV 50'] = [df23.loc[df23.GV>50,'eta'].mean()]
                summary = pd.DataFrame(summary)
                print(summary)
                summaries.append(summary)
                if fn in os.listdir(folder['op']):
                    df1 = pd.read_csv(os.path.join(folder['op'],fn),
                                      index_col=0)
                    df1.index = pd.to_datetime(df1.index)
                    df = pd.concat([df1,df])
                    df = df.sort_index()
                if not df.empty:
                    df.to_csv(os.path.join(folder['op'],fn))
            except:
                continue
            
            sns.set_style('darkgrid')
            plt.figure(figsize=(22,9))
            plt.subplots_adjust(left=0.04,right=0.99,top=0.95,bottom=0.05,
                                hspace=0.35,wspace=0.15)
            sn = fn[:-4]
            
            title = sn+' COP'
            plt.subplot(3,3,1)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.COP, s=2)
            plt.ylim(0,)
            
            title = sn+' efficiency'
            plt.subplot(3,3,5)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.eta,label='eta_COP', s=2)
            sns.scatterplot(x=df.index,y=df.eta_comp,label='eta_comp', s=2)
            plt.ylim(0,1.2)
            plt.axhline(1,ls='--',c='r')  
            
            if 'Hrs' in df.columns:
                title = sn + ' run hours'
                plt.subplot(3,3,2)
                plt.title(title)
                sns.scatterplot(x=df.index, y=df.Hrs, s=2)

            title = sn+' leaving water temperature'
            plt.subplot(3,3,4)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.LCW,label='LCW', s=2)
            sns.scatterplot(x=df.index,y=df.LCDW,label='LCDW', s=2)
            plt.ylabel('WaterT/C')
            
            title = sn+' percent line current'
            plt.subplot(3,3,7)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.PLC, s=2)
            plt.ylim(0,120)
            
            if 'GV' in df.columns:
                title = sn+' compression efficiency'
                plt.subplot(3,3,8)
                plt.title(title)
                # sns.scatterplot(x=df.PLC,y=df.SDT-df.SST,hue=df.eta_comp,
                #                 palette='rainbow',s=2)
                # plt.xlabel('Percent line current')
                # plt.ylabel('Lift/C')
                sns.scatterplot(x=df.GV,y=df.eta_comp,hue=df.Year,
                                palette='rainbow')
                plt.xlabel('Guide Vane Opening')
                plt.ylabel('eta_comp')
                plt.ylim(0,1)
                plt.xlim(0,120)
                plt.axhline(0.8,ls='--',c='r')
            
            title = sn+' evaporator leaving temperature difference'
            plt.subplot(3,3,3)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.LCW-df.SST,hue=df.Year,
                            palette='rainbow')
            plt.xlabel('Percent line current')
            plt.ylabel('Evaporator LTD/C')
            plt.ylim(0,)
            plt.xlim(0,120)
            plt.axhline(2.8,ls='--',c='r')
            
            title = sn+' condenser leaving temperature difference'
            plt.subplot(3,3,6)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.SDT-df.LCDW,hue=df.Year,
                            palette='rainbow')
            plt.xlabel('Percent line current')
            plt.ylabel('Condenser LTD/C')
            plt.ylim(0,)
            plt.xlim(0,120)
            plt.axhline(3.3,ls='--',c='r')
            
            title = sn+' compression efficiency'
            plt.subplot(3,3,9)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.eta_comp,hue=df.Year,
                            palette='rainbow')
            plt.ylabel('Compression efficiency')
            plt.ylim(0,1)
            plt.xlim(0,120)
            plt.axhline(0.8,ls='--',c='r')
            
            plt.savefig(os.path.join(char_folder,sn))
            plt.clf()
            
            # break
            
    # describe = pd.concat(des)
    #describe.to_csv('describe.csv')
    #summary = pd.concat(summaries)
    #summary.to_csv('summary.csv')
    
    # return acs
    
def rule_cop2(df):
    
    df = df[(df.PLC>30)&
            ((df.SDT-df.SST)>10)&
            (df.SST<20)&
            (df.LCW<20)&
            (df.CDT>df.SDT)]
    if df.empty:
        raise ValueError
    df = COP.Cal_HX(df, 0, 0)
    df = COP.Cal_COP(df, 'SST', 'SDT', 'COP', eta_isen = True)
    LCWn, LCDWn = 7, 37
    Q_evapn = PropsSI('H', 'T', LCWn + 273.15, 'Q', 1, ref) - PropsSI('H', 'T', LCDWn + 273.15, 'Q', 0, ref)
    Q_evapn *= PropsSI('D', 'T', LCWn + 273.15, 'Q', 1, ref)
    Q_evap = (df.h_suc - df.h_cdo) * COP.Props('D', 'T', df.LCW + 273.15, 'Q', 1, ref)
    tonnage = (df.Power / df.PLC *100 * df.COP / 3.52 / Q_evap * Q_evapn).median()
    print(tonnage)
    df, ton = Ecat_COP(df, new_col='psm_cop', chtp='19XRV', tonnage=tonnage, PLR='PLC')
    df.loc[df.psm_cop<df.COP,'psm_cop'] = df.COP
    df['eta'] = df['COP'] / df['psm_cop']

    return df, tonnage
    
def Read_Data2(folder):
    
    char_folder = 'charts_final1'
    try:
        os.mkdir(folder['op'])
    except:
        pass
    try:
        os.mkdir(char_folder)
    except:
        pass
    
    fnss = os.walk(folder['data'])
    des = []
    acs = []
    summaries = []
    global Ton_SN
    Ton_SN = {}
    YOM = pd.read_csv('summary_v4.csv',index_col=0)
    for root, dirs, fns in fnss:
        # if not '2023' in root: continue
        # fns = ["2301Q65746.csv"] #两个HRDC的需求
        fns = ["4710Q20221.csv", "4710q20220.csv", "1399J59406.csv","1499J59408.csv","1501Q65384.csv"]
        for fn in fns:
            print(fn)
            # if fn[:4]!='0211': continue
            # if not '5200Q64908' in fn: continue
            df = pd.read_csv(os.path.join(root, fn))
            df = Rename_Data(df)
            # df['DateTime'] = df['DateTime'].apply(
            #     lambda x: datetime.datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M:%S'))
            df['DateTime'] = df['DateTime'].str.split('+',expand=True)[0]
            df['DateTime'] = pd.to_datetime(df['DateTime'],format = '%Y-%m-%d %H:%M:%S')
            #df['DateTime'] = df['eventdatetime'].apply(
                #lambda x: parser.parse(x).strftime('%Y-%m-%d %H:%M:%S'))

            df.set_index('DateTime',inplace=True)
            df = df.sort_index()
            sn = df['Serialnumber'].mode()[0]
            df.drop('Serialnumber',axis=1,inplace=True)
            df = df.groupby(df.columns, axis=1).max()
            
            df = Convert_Unit(df)
            
            df = df[~df.index.duplicated(keep='first')]
            df = df.resample('15min').first()
            df.dropna(how='all', inplace=True)
            df['Year'] = df.index.year
            df['Serialnumber'] = sn
            # de = df.describe()
            # de['fn'] = fn
            # de['root'] = root
            # des.append(de)
            try:
                df, tonnage = rule_cop2(df)
                Ton_SN[sn] = tonnage
                print("SerialNumber:", sn, "Tonnage:", tonnage)

                eta75 = df.eta.quantile(0.75)
                eta25 = df.eta.quantile(0.25)
                etal = eta25 - 1.5 * (eta75 - eta25)
                df = df[df.eta>etal]
                df['COP_Current'] = df.COP
                df['COP_New'] = df.psm_cop
                df['Energy Saving%'] = (1 - df.COP_Current/df.COP_New)*100
                df['Energy Saving'] = df['Energy Saving%'] * df.Power
                de = df.describe()
                de['fn'] = fn
                de['root'] = root
                des.append(de)
                
                df23 = df[df.Year==2023] 
                summary = {'SN':[sn],
                            # 'Control error':[((df23.LCW-df23['Control Point'])>1).sum()/len(df23)],
                            # 'YOM':[YOM.loc[sn,'Age']],
                            # 'runhour':df.Hrs.max(),
                            # 'Average eta':[df23['eta'].mean()]
                            }
                df['Time'] = df.index
                dt = (df['Time'].diff(1)).mode()[0] / np.timedelta64(1, 'h')
                summary['tonnage'] = [tonnage]
                summary['starttime'] = [df['Time'].values[0]]
                summary['endtime'] = [df['Time'].values[-1]]
                summary['days'] = [(df['Time'].values[-1]-df['Time'].values[0]) / np.timedelta64(1, 'D')]
                if sn in YOM.index:
                    summary['YOM'] = [YOM.loc[sn,'Age']]
                if 'Hrs' in df.columns:
                    summary['total runhour'] = [df.Hrs.max()]
                    summary['runhours'] = [df.Hrs.max()-df.Hrs.min()]
                if 'Control Point' in df.columns:
                    if 'LCW' in df.columns:
                        summary['Control error'] = [((df23.LCW-df23['Control Point'])>1).sum()/len(df23)]
                if 'eta' in df.columns:
                    summary['Average eta'] = [df23['eta'].mean()]
                    summary['Average eta 80'] = [df23.loc[df23.PLC>80,'eta'].mean()]
                    summary['Average eta 90'] = [df23.loc[df23.PLC>90,'eta'].mean()]
                    if 'GV' in df.columns:
                        summary['Average eta GV 50'] = [df23.loc[df23.GV>50,'eta'].mean()]
                    if 'Power' in df.columns:
                        summary['kWh']= [df23.Power.sum() * dt]
                        if 'psm_cop' in df.columns:
                            summary['ES'] = [(df23.Power*(1-df23.COP/df23.psm_cop)*dt).sum()]
                summary = pd.DataFrame(summary)
                print(summary)
                summaries.append(summary)
                if fn in os.listdir(folder['op']):
                    df1 = pd.read_csv(os.path.join(folder['op'],fn),
                                      index_col=0)
                    df1.index = pd.to_datetime(df1.index)
                    df = pd.concat([df1,df])
                    df = df.sort_index()
                if not df.empty:
                    df.to_csv(os.path.join(folder['op'],fn))
            except:
                continue
            
            sns.set_style('darkgrid')
            plt.figure(figsize=(22,9))
            plt.subplots_adjust(left=0.04,right=0.99,top=0.95,bottom=0.05,
                                hspace=0.35,wspace=0.15)
            sn = fn[:-4]
            
            title = sn+' COP'
            plt.subplot(3,3,1)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.COP, s=2)
            plt.ylim(0,)
            
            title = sn+' efficiency'
            plt.subplot(3,3,5)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.eta,label='eta_COP', s=2)
            sns.scatterplot(x=df.index,y=df.eta_comp,label='eta_comp', s=2)
            plt.ylim(0,1.2)
            plt.axhline(1,ls='--',c='r')  
            
            if 'Hrs' in df.columns:
                title = sn + ' run hours'
                plt.subplot(3,3,2)
                plt.title(title)
                sns.scatterplot(x=df.index, y=df.Hrs, s=2)

            title = sn+' leaving water temperature'
            plt.subplot(3,3,4)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.LCW,label='LCW', s=2)
            sns.scatterplot(x=df.index,y=df.LCDW,label='LCDW', s=2)
            plt.ylabel('WaterT/C')
            
            title = sn+' percent line current'
            plt.subplot(3,3,7)
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.PLC, s=2)
            plt.ylim(0,120)
            
            if 'GV' in df.columns:
                title = sn+' compression efficiency'
                plt.subplot(3,3,8)
                plt.title(title)
                # sns.scatterplot(x=df.PLC,y=df.SDT-df.SST,hue=df.eta_comp,
                #                 palette='rainbow',s=2)
                # plt.xlabel('Percent line current')
                # plt.ylabel('Lift/C')
                sns.scatterplot(x=df.GV,y=df.eta_comp,hue=df.Year,
                                palette='rainbow')
                plt.xlabel('Guide Vane Opening')
                plt.ylabel('eta_comp')
                plt.ylim(0,1)
                plt.xlim(0,120)
                plt.axhline(0.8,ls='--',c='r')
            
            title = sn+' evaporator leaving temperature difference'
            plt.subplot(3,3,3)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.LCW-df.SST,hue=df.Year,
                            palette='rainbow')
            plt.xlabel('Percent line current')
            plt.ylabel('Evaporator LTD/C')
            plt.ylim(0,)
            plt.xlim(0,120)
            plt.axhline(2.8,ls='--',c='r')
            
            title = sn+' condenser leaving temperature difference'
            plt.subplot(3,3,6)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.SDT-df.LCDW,hue=df.Year,
                            palette='rainbow')
            plt.xlabel('Percent line current')
            plt.ylabel('Condenser LTD/C')
            plt.ylim(0,)
            plt.xlim(0,120)
            plt.axhline(3.3,ls='--',c='r')
            
            title = sn+' compression efficiency'
            plt.subplot(3,3,9)
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.eta_comp,hue=df.Year,
                            palette='rainbow')
            plt.ylabel('Compression efficiency')
            plt.ylim(0,1)
            plt.xlim(0,120)
            plt.axhline(0.8,ls='--',c='r')
            
            plt.savefig(os.path.join(char_folder,sn))
            plt.clf()
            
            title = sn + " COP comparison"
            plt.figure(figsize=(10,4))
            plt.title(title)
            sns.scatterplot(x=df.index,y=df.COP,label='Current COP')
            sns.scatterplot(x=df.index,y=df.psm_cop,label='New chiller COP')
            plt.xlabel('Date')
            plt.ylabel('COP')
            plt.savefig(os.path.join(char_folder,title))
            plt.clf()
            
            title = sn + " energy saving%"
            plt.figure(figsize=(6,4))
            plt.title(title)
            sns.scatterplot(x=df.PLC,y=df.ECDW,hue=(1-df.eta)*100,palette='rainbow')
            plt.xlabel('Percent Line current')
            plt.ylabel('Entering condenser water/C')
            plt.savefig(os.path.join(char_folder,title))
            plt.clf()
            # break
            
    # describe = pd.concat(des)
    # describe.to_csv('describe.csv')
    # summary = pd.concat(summaries)
    # summary.to_csv('summary.csv')
            
if __name__ == '__main__':
    
    folder = {'data':'North_America_chiller_retrofit',
              'op':'output_final_compare_to_psm'}
    ref = 'R134a'
    DEG_ben = [0.9,0.9,0.9,0.85,0.85,0.85,0.9]
    # acs = Read_Data1(folder)
    
    Read_Data2(folder)
    print(Ton_SN)
    # pd.DataFrame(acs).to_csv('alarms.csv')