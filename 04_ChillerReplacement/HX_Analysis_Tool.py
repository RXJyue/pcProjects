# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:52:49 2021

@author: chens6
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.switch_backend('agg')
plt.tight_layout()
import numpy as np
import seaborn as sns
from CoolProp.CoolProp import PropsSI
import datetime
import warnings
import joblib
import os, sys
from sklearn.neighbors import NearestNeighbors
from Utils.advanced_data_analytics_tool import Plot_Data, Mark_Data, Rename_Data
from scipy.interpolate import interp1d
import traceback
# from sklearn.linear_model import QuantileRegressor

warnings.filterwarnings("ignore")


def convert_unit(unit, units, data):
    '''
    Data unit conversion from English to Metric.

    Parameters
    ----------
    unit : string
        Unit serial number.
    units : dictionary
        List of unit serial number.
    data : DataFrame
        Input data before unit conversion.

    Returns
    -------
    data : DataFrame
        Output data after unit conversion.

    '''
    # if unit in units.keys():
    #     En_date = units[unit][0]
    #     for para in ['CDT','Control Point','ECW','ECDW','LCW','LCDW']:
    #         data[para][data.DateTime>=En_date] = (data[para][data.DateTime>=En_date]-32)/9*5
    #     for para in ['SP','DP']:
    #         data[para][data.DateTime>=En_date] = data[para][data.DateTime>=En_date]/0.145 

    for para in ['CDT', 'Control Point', 'ECW', 'ECDW', 'LCW', 'LCDW']:
        # F->C
        data[para] = (data[para] - 32) / 9 * 5
    for para in ['SP', 'DP']:
        # psi->kpa
        data[para] = data[para] / 0.145

    return data


def get_data(units, file='wuxi pilot 181108395.csv', data_unit='Metric', VFDretro='Y'):
    '''
    Function to read chiller running data from CSV file, data process
    and data unit conversion.

    Parameters
    ----------
    units : dictionary
        List of units to be analyzed.
    file : string, optional
        File name. The default is 'wuxi pilot 181108395.csv'.
    data_unit : string, optional
        Unit of data. The default is 'English'.

    Returns
    -------
    data : DataFrame
        Data from CSV file.
    unit : string
        Unit serial number.

    '''
    data = pd.read_csv(file)
    # data.rename(columns = {'Average Line Current':'Actual Line Current',
    #                        'Average Line Voltage':'Actual Line Voltage',
    #                        'Actual Guide Vane Pos':'Guide Vane 1 Actual Pos',
    #                        'Actual VFD Speed':'Actual VFD Speed %',
    #                        'Actual VFD Speed Percent':'Actual VFD Speed %',
    #                        'Line Kilowatts':'Line side Kilowatts',
    #                        'Service Ontime':'After Service Hrs'
    #                        },
    #             inplace = True)
    # columns = {'Serialnumber':'Serialnumber',
    #            'DateTime':'DateTime',
    #             'Actual Line Current':'ALC',
    #            # 'Actual Line Voltage':'ALV',
    #            'After Service Hrs':'Hrs',
    #            # 'Chilled Water Delta P':'CDP',
    #            'Comp Discharge Temp':'CDT',
    #            # 'Compressor Starts Num':'Compressor Starts Num',
    #            'Condenser Pressure':'DP',
    #            # 'Condenser Water Delta P':'CDDP',
    #            'Control Point':'Control Point',
    #            # 'Controlled Water Temp':'Controlled Water Temp',
    #            # 'Cooling/Heating Select':'Cooling/Heating Select',
    #            'Entering Chilled Water':'ECW',
    #            'Entering Condenser Water':'ECDW',
    #            # 'Evap Refrig Liquid Temp':'ERLT',
    #            'Evaporator Pressure':'SP',
    #             'Guide Vane 1 Actual Pos':'Guide Vane Position',
    #            'Leaving Chilled Water':'LCW',
    #            'Leaving Condenser Water':'LCDW',
    #            'Line side Kilowatts':'Power',
    #            'Actual VFD Speed %':'VFD',
    #             'Percent Line Current':'PLC',
    #            # 'Percent Line Voltage':'PLV',
    #            # 'Power Factor':'PF',
    #             }
    # data = data[columns.keys()]
    # data.replace(' - ',np.nan,inplace=True)
    # for col in columns.keys():
    #     if col not in ['Serialnumber','DateTime','Cooling/Heating Select']:
    #         data[col] = data[col].astype('float')

    # data.rename(columns = columns, inplace = True)
    data = Rename_Data(data, VFDretro)
    data = data.groupby(data.columns, axis=1).last()
    # data = data[['DateTime','Serialnumber','Control Point','CDT','SP','DP','LCW','ECW','LCDW','ECDW','PLC','ALC']]
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data.drop_duplicates(subset=['DateTime'], keep='first', inplace=True) 
    if isinstance(data['Serialnumber'].mode()[0], float):
        data['Serialnumber'] = data['Serialnumber'].astype('Int64')
    unit = str(data['Serialnumber'].mode()[0])
    if data_unit == 'English' or data_unit =='英制':
        data = convert_unit(unit, units, data)
    data.fillna(method='ffill', limit=5, inplace=True)

    return data, unit


def Props(a1, a2, a3, a4, a5, a6):
    '''
    Function for calculating thermodynamic properties.

    Parameters
    ----------
    a1 : string
        Name of output parameter.
    a2 : string
        Name of first input parameter.
    a3 : Series
        Data of first input parameter.
    a4 : string
        Name of second input parameter.
    a5 : Series
        Data of second input parameter.
    a6 : string
        Refrigerant name.

    Returns
    -------
    Array
        Data of output parameter.

    '''
    try:
        if isinstance(a3, pd.Series):
            a3 = np.array(a3)
        if isinstance(a5, pd.Series):
            a5 = np.array(a5)
        r = PropsSI(a1, a2, a3, a4, a5, a6)
        if isinstance(r, pd.Series):
            r[np.isinf(r)] = np.nan
        return r
    except:
        return np.nan


def Cal_COP(data, SST, SDT, COP, eta_isen=False, ref='R134a'):
    '''
    Function for calculating COP.

    Parameters
    ----------
    data : DataFrame
        Input data.
    SST : string
        Column name of saturated suction temperature from input data.
    SDT : string
        Column name of saturated discharge temperature from input data.
    COP : string
        Column name of output COP.
    eta_isen : boolean, optional
        Whether to calculate compressor isentropic efficiency from discharge 
        temperature or not. The default is False.
    ref : string, optional
        Refrigerant name. The default is 'R134a'.

    Returns
    -------
    data : DataFrame
        Output data.

    '''
    data['SP'] = Props('P', 'T', data[SST] + 273.15, 'Q', 0, ref)
    data['DP'] = Props('P', 'T', data[SDT] + 273.15, 'Q', 1, ref)
    data['h_cdo'] = Props('H', 'P', data.DP, 'Q', 0, ref)
    data['h_suc'] = Props('H', 'P', data.SP, 'Q', 1, ref)
    data['s_suc'] = Props('S', 'P', data.SP, 'Q', 1, ref)
    data['h_dis_i'] = Props('H', 'P', data.DP, 'S', data.s_suc, ref)
    if eta_isen:
        data['h_dis'] = Props('H', 'P', data.DP, 'T', data.CDT + 273.15, ref)
        data['eta_comp'] = (data.h_dis_i - data.h_suc) / (data.h_dis - data.h_suc)
        data['w_comp'] = data.h_dis - data.h_suc
    else:
        data['h_dis'] = data.h_suc + (data.h_dis_i - data.h_suc) / data.eta_comp

    data[COP] = (data.h_suc - data.h_cdo) / (data.h_dis - data.h_suc)

    return data


def Convert_Data(data, unit, EVAP, COND, nvol,ref,loop):
    '''
    This function is for thermodynamic property calculation, data filtering 
    and logarithmic mean temperature difference calcution.

    Parameters
    ----------
    data : DataFrame
        Input data.
    ref : string
        Refrigerant name.

    Returns
    -------
    data : DataFrame
        Output data.
    hA_evap_max : float
        maximum of the product of evaporator heat transfer coefficient and area.
    hA_cond_max : float
        maximum of the product of condenser heat transfer coefficient and area.

    '''
    for para in ['DP', 'SP']:
        data[para] = data[para] * 1000 + 101325
    for para in [['SST', 'SP'],
                 ['SDT', 'DP']]:
        data[para[0]] = Props('T', 'P', data[para[1]], 'Q', 0, ref) - 273.15
    data['PLC'] = data['PLC'] / 100

    if 'Power' not in data.columns:
        if 'ALV' in data.columns:
            print(data.ALC)
            print(data.ALV)

            data['Power'] = data.ALC * data.ALV * (3 ** 0.5) / 1000 * 0.9
        else:
            nvol = int(nvol)
            data['Power'] = data.ALC * nvol * (3 ** 0.5) / 1000 * 0.9
    # 保存temp文件，当作处理好的data文件，后续用来预测处理
    data.to_pickle('result/data/%s%s.pkl' % (unit, loop))
    # if VFDretro == 'N':
    #
    # else:
    #     data.to_pickle('result/data/%s.pkl' % unit)
    # data['Guide Vane Position'] /= 100
    
    print(data.info(),'-----------------------------------------------------------------------------')
    print(data)
    print(data.describe())
    data = data[(data.ALC > 1)
                & (data.PLC > 0)
                & (data.ECDW > 15)
                & (data.LCDW > 15)
                & (data.SDT > 15)
                & (data.CDT > 0)
                & (data.LCW > -15)
                & (data.ECW > -15)
                & (data.SST > -15)
        # &((data.SDT-data.SST)>5)
               ]
    data = data[abs(data['LCW'] - data['Control Point']) < 0.5]
    print(data.describe())
    if len(data) > 0:

        # data = data[(data.SDT-data.SST)>15]
        # data = data[(data['SST']<data['LCW'])
        #             &(data['LCW']<data['ECW'])
        #             &(data['SDT']>data['LCDW'])
        #             &(data['LCDW']>data['ECDW'])]
        # data['SST'][data.SST>data.LCW] = data.LCW-0.01
        # data['SDT'][data.SDT<data.LCDW] = data.LCW+0.01
        # data['ECW'][data.ECW<data.LCW] = data.LCW+0.01
        # data['ECDW'][data.ECDW>data.LCDW] = data.LCDW-0.01
        data.loc[data.SST > data.LCW, 'SST'] = data.LCW - 0.01
        data.loc[data.SDT < data.LCDW, 'SDT'] = data.LCDW + 0.01
        data.loc[data.ECW < data.LCW, 'ECW'] = data.LCW + 0.01
        data.loc[data.ECDW > data.LCDW, 'ECDW'] = data.LCDW - 0.01
        data = data[(data.SDT - data.SST) > 5]

        data['COOLDT'] = data.ECW - data.LCW
        data['CONDDT'] = data.LCDW - data.ECDW

        data['app_evap'] = (data['COOLDT']) / (
            ((data['ECW'] - data['SST']) / (data['LCW'] - data['SST'])).apply(np.log))
        data['app_cond'] = (data['CONDDT']) / (
            ((data['SDT'] - data['ECDW']) / (data['SDT'] - data['LCDW'])).apply(np.log))
        # data['P_comp'] = data.ALC * data.ALV * math.sqrt(3) / 1000

        data = Cal_COP(data, 'SST', 'SDT', 'COP_ref', eta_isen=True)

        temp = data[data.PLC > 0.3]
        LCWn, LCDWn = 7, 37
        Q_evapn = PropsSI('H', 'T', LCWn + 273.15, 'Q', 1, ref) - PropsSI('H', 'T', LCDWn + 273.15, 'Q', 0, ref)
        Q_evapn *= PropsSI('D', 'T', LCWn + 273.15, 'Q', 1, ref)
        Q_evap = (temp.h_suc - temp.h_cdo) * Props('D', 'T', temp.LCW + 273.15, 'Q', 1, ref)
        tonnage = (temp.Power / temp.PLC * temp.COP_ref / 3.52 / Q_evap * Q_evapn).median()
        data['Q_evap'] = data.Power * data.COP_ref
        data['Q_cond'] = data['Q_evap'] + data['Power']
        data['evap_water_flow'] = data['Q_evap'] / data['COOLDT'] / 4.2 * 3.6
        data['cond_water_flow'] = data['Q_cond'] / data['CONDDT'] / 4.2 * 3.6
        data['hA_evap'] = data['Q_evap'] / data['app_evap']
        data['hA_cond'] = data['Q_cond'] / data['app_cond']
        data = outlier_filter(data, ['hA_evap', 'hA_cond'])
        hA_evap_max = data['hA_evap'][
            (data['hA_evap'] == data['hA_evap']) & (data['hA_evap'] < data['hA_evapH'])].rolling(
            min(100, len(data) // 5), min(len(data) // 5, 10)).mean().max()
        hA_cond_max = data['hA_cond'][
            (data['hA_cond'] == data['hA_cond']) & (data['hA_cond'] < data['hA_condH'])].rolling(
            min(100, len(data) // 5), min(len(data) // 5, 10)).mean().max()
        data['SST_i'] = data['LCW'] - data['COOLDT'] / (
                    (data['COOLDT'] / (data['Q_evap'] / hA_evap_max)).apply(np.exp) - 1)
        data['SDT_i'] = data['LCDW'] + data['CONDDT'] / (
                    (data['CONDDT'] / (data['Q_cond'] / hA_cond_max)).apply(np.exp) - 1)
        print(EVAP, '----------------')
        if EVAP is not None and COND is not None:
            data['SST_i'][data['SST_i'] < (data['LCW'] - EVAP)] = data['LCW'] - EVAP  # EVAP
            data['SDT_i'][data['SDT_i'] > (data['LCDW'] + COND)] = data['LCDW'] + COND  # COND
            print(EVAP, COND)
        return data, hA_evap_max, hA_cond_max, tonnage

    else:
        return data, 0, 0, 0


def Cal_eta(data, unit, EVAP, COND, nvol,loop, ref='R134a'):
    '''
    Function for calculating heat exchanger efficiency and energy waste.

    Parameters
    ----------
    data : DataFrame
        Input data.
    ref : string, optional
        Refrigerant name. The default is 'R134a'.

    Returns
    -------
    data : DataFrame
        Output data.
    hA_evap_max : float
        maximum of the product of evaporator heat transfer coefficient and area.
    hA_cond_max : float
        maximum of the product of condenser heat transfer coefficient and area.
    tonnage : float
        the cooling capacity
    '''
    data, hA_evap_max, hA_cond_max, tonnage = Convert_Data(data, unit, EVAP, COND, nvol, ref,loop)
    if data.empty:
        return data, 0, 0, 0
    data = Cal_COP(data, 'SST_i', 'SDT', 'COP_ievap')
    data = Cal_COP(data, 'SST', 'SDT_i', 'COP_icond')
    data['eta_evap'] = data['COP_ref'] / data['COP_ievap']
    data['eta_cond'] = data['COP_ref'] / data['COP_icond']

    data['P_evap_opt'] = 0
    data['P_cond_opt'] = 0
    data['P_act'] = 0
    for i in range(100):
        data['P_evap_opt'] += data['eta_evap'].shift(i) * data['Power'].shift(i)
        data['P_cond_opt'] += data['eta_cond'].shift(i) * data['Power'].shift(i)
        data['P_act'] += data['Power'].shift(i)
    data['EW_evap'] = data['P_evap_opt'] / data['P_act']
    data['EW_cond'] = data['P_cond_opt'] / data['P_act']
    data['EW_evap'][data['EW_evap'] > 1] = 1
    data['EW_cond'][data['EW_cond'] > 1] = 1

    return data, hA_evap_max, hA_cond_max, tonnage


def Mod_ECDW_Temp(data, weather_path, limit_ECDW=20):
    """
    Function for modify the entering condenser water temperature by the wet bulb temperature

    Parameters
    ----------
    data : DataFrame
        Input data.
    weather_path : string, optional
        Input weather data
    limit_ECDW : Float
        the minimum entering condenser water temperature

    :param data:
    :param weather_path:
    :return:
    ----------
    data : DataFrame
        Input data.
    Mod_ECDW:
        Mod the entering condenser water temperature

    """
    try:
        # get the weather data
        data_weather = pd.read_pickle(weather_path)
        data['month'] = data['DateTime'].dt.month
        data['dayofyear'] = data['DateTime'].dt.dayofyear
        data['hour'] = data['DateTime'].dt.hour
        # time transfer to the hour
        data['Time'] = data['hour'] + 1 + 24 * (data['dayofyear'] - 1)
        # mod the condenser temperature
        data = pd.merge(data, data_weather.loc[:, ['Time', 'OAT_wb']], on='Time', how='left')
        data.loc[data.ECDW < data.OAT_wb, 'OAT_wb'] = data.ECDW - 0.1
        # get the non reasonable data
        data['ECDW_diff'] = data['ECDW'] - data['OAT_wb']
        data.loc[data.ECDW_diff < 3, 'ECDW_diff'] = 3
        # calculate the cooling tower heat transfer efficiency
        # data_number = int(len(data.loc[(data.ECDW - data.OAT_wb < 3)]) * 5)
        data['app_cooling_tower'] = (data['CONDDT']) / (
            ((data['CONDDT'] + data['ECDW_diff']) / (data['ECDW_diff'])).apply(np.log))
        data['hA_cooling_tower'] = data['Q_cond'] / data['app_cooling_tower']
        data = outlier_filter(data, ['hA_cooling_tower'])
        # get the max hA
        hA_cooling_tower_max = data['hA_cooling_tower'][
            (data['hA_cooling_tower'] == data['hA_cooling_tower']) & (
                    data['hA_cooling_tower'] < data['hA_cooling_towerH'])].rolling(
            min(100, len(data) // 5), min(len(data) // 5, 10)).mean().max()
        # get the new entering condenser temperature
        data['Mod_ECDW'] = data['OAT_wb'] + data['CONDDT'] / (
                (data['CONDDT'] / (data['Q_cond'] / hA_cooling_tower_max)).apply(np.exp) - 1)
        # adjust the condenser temperature if temperature is below 20
        # if the Mod_ECDW low than ECDW, Mod_ECDW = ECDW
        data.loc[data.Mod_ECDW > data.ECDW, 'Mod_ECDW'] = data['ECDW']
        data.loc[data.Mod_ECDW < limit_ECDW, 'Mod_ECDW'] = limit_ECDW
        # delete the useless columns in data
        data.drop(['dayofyear', 'hour', 'Time'], axis=1, inplace=True)
        # return the result
        return data
    except Exception as err:
        print(err)
        raise
    pass


def outlier_filter(data, paras, number =100):
    '''
    Function for calculating outlier filter threshold.

    Parameters
    ----------
    data : DataFrame
        Input data.
    paras : list
        Columns where high low limit calculation are needed.
    number : int
        the number

    Returns
    -------
    data : DataFrame
        Output data containing calculated high low limits.

    '''
    # data['inlier'] = True
    for para in paras:
        # data = data[data[para]==data[para]]
        data75 = data[para].rolling(number, 1, center=True).quantile(0.75)
        data25 = data[para].rolling(number, 1, center=True).quantile(0.25)
        data[para + 'H'] = data75 + 1.5 * (data75 - data25)
        data[para + 'L'] = data25 - 1.5 * (data75 - data25)
        # data['inlier'][(data[para] > dataH) | (data[para] < dataL)] = False
    # data = data[data['inlier']]
    return data


def PSM_coe():
    folder = 'PSM/10 coe'
    psm_coe = {}
    for chtp in os.listdir(folder):
        psm_coe[chtp] = {}
        for fn in os.listdir(os.path.join(folder, chtp)):
            coe = [float(x) for x in pd.read_table(os.path.join(folder, chtp, fn)).columns]
            psm_coe[chtp][int(fn.split('T')[0])] = coe
    return psm_coe


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
    regressor = Ecat_map(chtp, tonnage)
    data.dropna(subset=[PLR, LT, ECT], inplace=True)
    data.PLR = data.PLR * 20
    # data = data.astype('float')
    data[new_col] = regressor.predict(data[[PLR, LT, ECT]])
    data.PLR = data.PLR / 20
    return data


def Ecat_COP_chart():
    for tonnage in (list(range(300, 3001, 100)) + list(range(350, 751, 100))):
        # if tonnage != 500: continue
        # for tonnage in range(1800,2001,200):

        data = {'LCW': [7] * 15000,
                'PLR': [(i + 1) / 100 for i in range(150)] * 100,
                'ECDW': [15 + 0.2 * (i // 150) for i in range(15000)]}
        data = pd.DataFrame.from_dict(data)
        data = Ecat_COP(data, 'psm_cop_fs', '19XR', tonnage)
        data = Ecat_COP(data, 'psm_cop_vs', '19XRV', tonnage)
        data.ES = 1 - data.psm_cop_fs / data.psm_cop_vs

        plt.title('%d ton FS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, data.psm_cop_fs, palette='rainbow')
        plt.show()

        plt.title('%d ton VS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, data.psm_cop_vs, palette='rainbow')
        plt.show()
        plt.figure(figsize=(4, 3))
        plt.title('%d ton FS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.psm_cop_fs, data.ECDW, palette='rainbow')
        plt.ylim(0, 12)
        plt.show()
        plt.figure(figsize=(4, 3))
        plt.title('%d ton VS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.psm_cop_vs, data.ECDW, palette='rainbow')
        plt.ylim(0, 12)
        plt.show()
        data = data[(data.ES < 1) & (data.ES > 0)]

        plt.title('%d ton (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, 1 - data.psm_cop_fs / data.psm_cop_vs, palette='rainbow')
        plt.show()


def PSM_COP(data, new_col='psm_cop', chtp='19XR', tonnage='600', PLR='PLR'):
    psm_coe = PSM_coe()[chtp][tonnage]
    data[new_col] = psm_coe[0]
    for i, para in enumerate([PLR, 'LCW', 'ECDW']):
        data[new_col] += data[para] * psm_coe[i + 1]
        data[new_col] += data[para] * data[para] * psm_coe[i + 4]
        data[new_col] += data[PLR] * data['LCW'] * data['ECDW'] / data[para] * psm_coe[9 - i]

    return data


def PSM_COP_chart():
    # for i in range(3,31):
    for tonnage in range(1800, 2001, 200):
        data = {'LCW': [7] * 15000,
                'PLR': [(i + 1) / 100 for i in range(150)] * 100,
                'ECDW': [15 + 0.2 * (i // 150) for i in range(15000)]}
        data = pd.DataFrame.from_dict(data)
        data = PSM_COP(data, 'psm_cop_fs', '19XR', tonnage)
        data = PSM_COP(data, 'psm_cop_vs', '19XRV', tonnage)
        data.ES = 1 - data.psm_cop_fs / data.psm_cop_vs

        data.PLR = data.PLR
        plt.title('%d ton FS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, data.psm_cop_fs, palette='rainbow')
        plt.show()

        plt.title('%d ton VS COP (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, data.psm_cop_vs, palette='rainbow')
        plt.show()

        data = data[(data.ES < 1) & (data.ES > 0)]

        plt.title('%d ton (LCW = %d C)' % (tonnage, data['LCW'].iloc[0]))
        sns.scatterplot(data.PLR, data.ECDW, 1 - data.psm_cop_fs / data.psm_cop_vs, palette='rainbow')
        plt.show()


def PSM_ES(data, unit, tonnage, hA_evap_max=0, hA_cond_max=0, VSFS='FS', plot=False, save_path=None,
           cop_mod_ECDW=False):
    '''
    Function for estimating energy saving potential from chiller map.

    Parameters
    ----------
    data : DataFrame
        Input data.
    hA_evap_max : float
        maximum of the product of evaporator heat transfer coefficient and area.
    hA_cond_max : float
        maximum of the product of condenser heat transfer coefficient and area.
    unit : string
        Unit serial number.
    tonnage : float
        Nominal tonnage of chiller.
    LCWn : float
        Design LCW.
    ECDWn : float
        Design ECDW.
    VSFS : string
        Is the calculated chiller a variable speed or fix speed chiller. 'VS' 
        for variable speed, 'FS' for fix speed.
    cop_mod_ECDW: bool
        calculate cop by the new ECDW under a variable speed(VS) and fix speed (FS)
    Returns
    -------
    data : DataFrame
        Output data.

    '''
    tons = [600, 650, 700, 750, 800, 900, 1000, 1100, 1700, 2000, 2100, 2300, 2400, 2500, 2600, 2700, 2800, 2900,
            3000]
    f = interp1d(tons, tons, kind='nearest', bounds_error=False, fill_value='extrapolate')
    ton_sel = f([tonnage])[0]
    residuals = []
    hx_cal = False if (hA_evap_max == 0) & (hA_cond_max == 0) else True
    if VSFS == 'FS':
        model_current = '19XR'
        model_compare = '19XRV'
        compare = '变频'

    elif VSFS == 'VS':
        model_current = '19XRV'
        model_compare = '19XR'
        compare = '定频'

    else:
        # default mode
        model_current = '19XR'
        model_compare = '19XRV'
        compare = '变频'
        pass

    if hx_cal:
        data['ECDW1'] = data['ECDW']
        data['LCW1'] = data['LCW']
        data['LCW'] = data['SST'] + data['COOLDT'] / ((hA_evap_max * data['COOLDT'] / data['Q_evap']).apply(np.exp) - 1)
        data['ECDW'] = data['SDT'] - data['CONDDT'] / (
                1 - (-hA_cond_max * data['CONDDT'] / data['Q_cond']).apply(np.exp))
        data['PLR'] = data['PLC']

    else:
        data['LCW'] = data['LCW_cal']
        data['ECDW'] = data['ECDW_cal_fs']

    for i in range(1000):
        pPLR = data['PLR'].copy()
        # data = PSM_COP(data, 'psm_cop_current', model_current, tonnage, 'PLR')
        data = Ecat_COP(data, 'psm_cop_current', model_current, ton_sel, 'PLR')
        if hx_cal:
            eta = (data.COP_ref/data['psm_cop_current']).median()
            data['PLR'] = data['psm_cop_current'] * eta * data['Power'] / tonnage / 3.52
            data.loc[data['PLR'] > 1, 'PLR'] = 1
        residual = (pPLR - data['PLR']).std() / (data['PLR'].mean())
        residuals.append(residual)
        if not hx_cal: break
        if len(residuals) > 2:
            if (residuals[-2] - residual) < 1E-8:
                break

    if cop_mod_ECDW:
        data = Ecat_COP(data, 'psm_cop_modECDW_current', model_current, ton_sel, 'PLR', ECT='Mod_ECDW')

    data['LCW_cal'] = data['LCW']
    data['ECDW_cal_fs'] = data['ECDW']
    # plt.scatter(range(len(residuals)),residuals)
    # plt.show()
    # data = PSM_COP(data, 'psm_cop_compare', model_compare, tonnage, 'PLR')
    data = Ecat_COP(data, 'psm_cop_compare', model_compare, ton_sel, 'PLR')
    residuals = []
    if not hx_cal:
        data['ECDW'] = data['ECDW_cal_vs']
    for i in range(1000):
        cop = data['psm_cop_compare'].copy()
        if hx_cal:
            data['SDT1'] = data['ECDW1'] + data['CONDDT'] * (1 + 1 / data['psm_cop_compare']) / (
                    1 + 1 / data['psm_cop_current']) / (
                                   1 - (-data['hA_cond'] * data['CONDDT'] / data['Q_cond']).apply(np.exp))
            data['ECDW'] = data['SDT1'] - data['CONDDT'] * (1 + 1 / data['psm_cop_compare']) / (
                    1 + 1 / data['psm_cop_current']) / (
                                   1 - (-hA_cond_max * data['CONDDT'] / data['Q_cond']).apply(np.exp))
        # data = PSM_COP(data, 'psm_cop_compare', model_compare, tonnage, 'PLR')     
        data = Ecat_COP(data, 'psm_cop_compare', model_compare, ton_sel, 'PLR')
        residual = (cop - data['psm_cop_compare']).std() / data['psm_cop_compare'].mean()
        residuals.append(residual)
        if not hx_cal: break
        if len(residuals) > 2:
            if (residuals[-2] - residual) < 1E-8:
                break

    if cop_mod_ECDW:
        data = Ecat_COP(data, 'psm_cop_modECDW_compare', model_compare, ton_sel, 'PLR', ECT='Mod_ECDW')

    data['ECDW_cal_vs'] = data['ECDW']

    # plt.scatter(range(len(residuals)),residuals)
    # plt.show()

    if hx_cal:
        data['ECDW'] = data['ECDW1']
        data['LCW'] = data['LCW1']
        data['PLC_compare'] = data['PLC'] * data.psm_cop_current / data.psm_cop_compare
    if VSFS == 'FS':
        data.psm_cop_compare = data[['psm_cop_compare', 'psm_cop_current']].max(axis=1)
        data['ES_VFD'] = data.Power * (1 - data.psm_cop_current / data.psm_cop_compare)
        data['节能百分比'] = 1 - data.psm_cop_current / data.psm_cop_compare
    elif VSFS == 'VS':
        data.psm_cop_current = data[['psm_cop_compare', 'psm_cop_current']].max(axis=1)
        data['ES_VFD'] = data.Power * (1 - data.psm_cop_compare / data.psm_cop_current)
        data['节能百分比'] = 1 - data.psm_cop_compare / data.psm_cop_current
    if plot:
        PSM_ES_Charts(data, unit, compare, save_path)

    return data  # , unit, compare, save_path


def PSM_ES_Charts(data, unit, compare, save_path):
    '''
    Save chiller map method results in "result" folder

    Parameters
    ----------
    data : DataFrame
        Input data.
    unit : string
        Unit serial number.
    compare : string
        Is the calculated chiller a variable speed or fix speed chiller. '变频' 
        for variable speed, '定频' for fix speed..

    Returns
    -------
    None.

    '''

    plt.clf()

    title = '%s变频改造前后COP Vs. 电流百分比' % unit
    plt.title(title)
    # sns.scatterplot(data.PLC,data.COP_ref,label = '制冷剂侧COP')
    sns.scatterplot(data.PLC, data.psm_cop_current, label='实际运行COP')
    sns.scatterplot(data.PLC, data.psm_cop_compare, label='对比%s机组COP' % compare)
    plt.xlim(0, 1)
    plt.ylim(0, 15)
    plt.legend()
    plt.xlabel('电流百分比')
    plt.ylabel('COP')
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    title = '%s变频改造前后COP Vs. 冷却水进水水温' % unit
    plt.title(title)
    # sns.scatterplot(data.ECDW,data.COP_ref,label = '制冷剂侧COP')
    sns.scatterplot(data.ECDW, data.psm_cop_current, label='实际运行COP')
    sns.scatterplot(data.ECDW, data.psm_cop_compare, label='对比%s机组COP' % compare)
    # plt.xlim(0,1)
    plt.ylim(0, 15)
    plt.legend()
    plt.xlabel('冷却水进水水温(℃)')
    plt.ylabel('COP')
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    title = '%s节能百分比' % unit
    plt.title(title)

    # temp = outlier_filter(data, ['节能百分比'])
    # temp = temp[temp['节能百分比']>temp['节能百分比L']]
    sns.scatterplot(data.PLC, data.ECDW, data['节能百分比'], palette='rainbow')
    plt.xlabel('电流百分比')
    plt.ylabel('冷却水进水水温(℃)')
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    plt.figure(figsize=(10, 4))
    title = '%s变频改造前后COP' % unit
    plt.title(title)
    # sns.scatterplot(data.DateTime,data.COP_ref,label = '制冷剂侧COP')
    sns.scatterplot(data.DateTime, data.psm_cop_current, label='实际运行COP')
    sns.scatterplot(data.DateTime, data.psm_cop_compare, label='对比%s机组COP' % compare)
    plt.xlim(data.DateTime.min(), data.DateTime.max())
    plt.xlabel('时间')
    plt.ylabel('COP')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.legend()
    
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    plt.figure(figsize=(10, 4))
    title = '%s COP before and after retrofit' % unit
    plt.title(title)
    # sns.scatterplot(data.DateTime,data.COP_ref,label = '制冷剂侧COP')
    if compare == '定频' or compare == 'FS':
        sns.scatterplot(data.DateTime, data.psm_cop_current, label='Variable speed COP')
        sns.scatterplot(data.DateTime, data.psm_cop_compare, label='Fix speed COP')
    else:
        sns.scatterplot(data.DateTime, data.psm_cop_current, label='Fix speed COP')
        sns.scatterplot(data.DateTime, data.psm_cop_compare, label='Variable speed COP')

    plt.xlim(data.DateTime.min(), data.DateTime.max())
    plt.xlabel('Time')
    plt.ylabel('COP')
    plt.legend()
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    plt.figure(figsize=(10, 5))
    title = '%s变频改造前后电流百分比' % unit
    plt.title(title)
    sns.scatterplot(data.DateTime, data.PLC, label='实际运行')
    sns.scatterplot(data.DateTime, data.PLC_compare, label='对比%s机组' % compare)
    plt.xlim(data.DateTime.min(), data.DateTime.max())
    plt.xlabel('时间')
    plt.ylabel('电流百分比')
    plt.legend()
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()

    plt.figure(figsize=(10, 4))
    title = '%s变频改造前后输入功率kW' % unit
    plt.title(title)
    sns.scatterplot(data.DateTime, data.Power, label='实际运行')
    sns.scatterplot(data.DateTime, data.Power / data.PLC * data.PLC_compare, label='对比%s机组' % compare)
    plt.xlim(data.DateTime.min(), data.DateTime.max())
    plt.xlabel('时间')
    plt.ylabel('功率kW')
    plt.legend()
    plt.savefig(os.path.join(save_path, '%s.png' % title))
    plt.close()


def unit_summary(data, VSFS, unit, dt, save_path, VFDretro, type, language=1):
    """
    Generate VFD retrofit benefit monthly summary.

    Parameters
    ----------
    data : DataFrame
        Input data.
    VSFS : string
        Is the calculated chiller a variable speed or fix speed chiller. 'VS'
        for variable speed, 'FS' for fix speed.
    unit : string
        Unit serial number.

    Returns
    -------
    DataFrame.

    2022/7/8 Update : Add parameters
    ----------
    VFDretro : string
        This is to determine whether to VFD. 'Y' or 'N'

    """

    data['Month'] = data['DateTime'].apply(lambda x: x.strftime('%Y/%m'))
    months = data.Month.unique()
    if VSFS == 'FS':
        compare = '变频改造后COP' if language else 'COP after VFD retrofit'
    elif VSFS == 'VS':
        compare = '变频改造前COP' if language else 'COP before VFD retrofit'
    if language:
        m_ana = {'月份': [],
                 '运行能耗/kWh': [],
                 '运行时间/Hrs': [],
                 '平均冷冻水出水温度/℃': [],
                 '平均冷却水进水温度/℃': [],
                 '平均电流百分比': [],
                 '平均负荷百分比': [],
                 '冷却水温差/℃': [],
                 '冷凝器趋近温度/℃': [],
                 '冷凝器节能空间/kWh': [],
                 '冷凝器节能空间%': [],
                 '冷冻水温差/℃': [],
                 '蒸发器趋近温度/℃': [],
                 '蒸发器节能空间/kWh': [],
                 '蒸发器节能空间%': [],
                 '制冷剂泄漏指数':[],
                 '实际运行COP': [],
                 compare: [],
                 '变频节能空间/kWh': [],
                 '变频节能百分比': []}
        for m in months:
            temp = data[data.Month == m]
            m_ana['月份'].append(m)
            m_ana['运行能耗/kWh'].append('%.0f' % (temp.Power.sum() * dt))
            if 'Hrs' in temp.columns:
                dHrs = temp.Hrs - temp.Hrs.shift(1)
                m_ana['运行时间/Hrs'].append('%.0f' % (max((dHrs[(dHrs > 0) & (dHrs < 10)]).sum(),
                                                     len(temp) * dt)))
            else:
                m_ana['运行时间/Hrs'].append('%.0f' % (len(temp) * dt))
            m_ana['平均冷冻水出水温度/℃'].append('%.1f' % (temp.LCW.mean()))
            m_ana['平均冷却水进水温度/℃'].append('%.1f' % (temp.ECDW.mean()))
            m_ana['平均电流百分比'].append('%.1f' % (temp.PLC.mean() * 100) + ' %')
            if 'PLR' in temp.columns:
                m_ana['平均负荷百分比'].append('%.1f' % (temp.PLR.mean() * 100) + ' %')
            else:
                m_ana['平均负荷百分比'] = 'plholder'
                del m_ana['平均负荷百分比']
            m_ana['冷却水温差/℃'].append('%.1f' % (temp.LCDW - temp.ECDW).mean())
            m_ana['冷凝器趋近温度/℃'].append('%.1f' % ((temp.SDT - temp.LCDW).mean()))
            m_ana['冷凝器节能空间/kWh'].append('%.0f' % (max((temp.Power * (1 - temp.eta_cond)).sum() * dt, 0)))
            m_ana['冷凝器节能空间%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_cond)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            m_ana['冷冻水温差/℃'].append('%.1f' % (temp.ECW - temp.LCW).mean())
            m_ana['蒸发器趋近温度/℃'].append('%.1f' % ((temp.LCW - temp.SST).mean()))
            m_ana['蒸发器节能空间/kWh'].append('%.0f' % (max((temp.Power * (1 - temp.eta_evap)).sum() * dt, 0)))
            m_ana['蒸发器节能空间%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_evap)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            if 'CI' in temp.columns:
                m_ana['制冷剂泄漏指数'].append('%.2f' % (temp.CI.mean()))
            else:
                m_ana['制冷剂泄漏指数'] = 'plholder'
                del m_ana['制冷剂泄漏指数']
            if (VFDretro == 'Y') | ((VFDretro == 'N') & (VSFS == 'FS') & (type == '30XW')):
                m_ana['实际运行COP'].append('%.1f' % (temp.psm_cop_current.mean()))
                m_ana[compare].append('%.1f' % (temp.psm_cop_compare.mean()))
                m_ana['变频节能空间/kWh'].append('%.0f' % (temp.ES_VFD.sum() * dt))
                m_ana['变频节能百分比'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power.sum() * 100) + ' %')
            else:
                m_ana['实际运行COP'],m_ana[compare],m_ana['变频节能空间/kWh'],m_ana['变频节能百分比']= 'plholder','plholder','plholder','plholder'
                del m_ana['实际运行COP']
                del m_ana[compare]
                del m_ana['变频节能空间/kWh']
                del m_ana['变频节能百分比']
        m_ana = pd.DataFrame.from_dict(m_ana)
        m_ana.sort_values(by='月份', inplace=True)
    else:
        m_ana = {'Month': [],
                 'Power/kWh': [],
                 'Runtime/Hrs': [],
                 'Avg. LCW/℃': [],
                 'Avg. ECDW/℃': [],
                 'Avg. percent line current': [],
                 'Avg. PLR': [],
                 'deltaT_cond/℃': [],
                 'app_cond/℃': [],
                 'ES_cond/kWh': [],
                 'ES_cond%': [],
                 'deltaT_evap/℃': [],
                 'app_evap/℃': [],
                 'ES_evap/kWh': [],
                 'ES_evap%': [],
                 'leakage_index': [],
                 'Chiller running COP': [],
                 compare: [],
                 'VFD retrofit saving/kWh': [],
                 'VFD retrofit saving %': []}
        for m in months:
            temp = data[data.Month == m]
            m_ana['Month'].append(m)
            m_ana['Power/kWh'].append('%.0f' % (temp.Power.sum() * dt))
            if 'Hrs' in temp.columns:
                dHrs = temp.Hrs - temp.Hrs.shift(1)
                m_ana['Runtime/Hrs'].append('%.0f' % (max((dHrs[(dHrs > 0) & (dHrs < 10)]).sum(),
                                                        len(temp) * dt)))
            else:
                m_ana['Runtime/Hrs'].append('%.0f' % (len(temp) * dt))
            m_ana['Avg. LCW/℃'].append('%.1f' % (temp.LCW.mean()))
            m_ana['Avg. ECDW/℃'].append('%.1f' % (temp.ECDW.mean()))
            m_ana['Avg. percent line current'].append('%.1f' % (temp.PLC.mean() * 100) + ' %')
            if 'PLR' in temp.columns:
                m_ana['Avg. PLR'].append('%.1f' % (temp.PLR.mean() * 100) + ' %')
            else:
                m_ana['Avg. PLR'] = 'plholder'
                del m_ana['Avg. PLR']
        
            m_ana['deltaT_cond/℃'].append('%.1f' % (temp.LCDW - temp.ECDW).mean())
            m_ana['app_cond/℃'].append('%.1f' % ((temp.SDT - temp.LCDW).mean()))
            m_ana['ES_cond/kWh'].append('%.0f' % (max((temp.Power * (1 - temp.eta_cond)).sum() * dt, 0)))
            m_ana['ES_cond%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_cond)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            m_ana['deltaT_evap/℃'].append('%.1f' % (temp.ECW - temp.LCW).mean())
            m_ana['app_evap/℃'].append('%.1f' % ((temp.LCW - temp.SST).mean()))
            m_ana['ES_evap/kWh'].append('%.0f' % (max((temp.Power * (1 - temp.eta_evap)).sum() * dt, 0)))
            m_ana['ES_evap%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_evap)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            if 'CI' in temp.columns:
                m_ana['leakage_index'].append('%.2f' % (temp.CI.mean()))
            else:
                m_ana['leakage_index'] = 'plholder'
                del m_ana['leakage_index'] 
            if (VFDretro == 'Y') | ((VFDretro == 'N') & (VSFS == 'FS') & (type == '30XW')):
                m_ana['Chiller running COP'].append('%.1f' % (temp.psm_cop_current.mean()))
                m_ana[compare].append('%.1f' % (temp.psm_cop_compare.mean()))
                m_ana['VFD retrofit saving/kWh'].append('%.0f' % (temp.ES_VFD.sum() * dt))
                m_ana['VFD retrofit saving %'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power.sum() * 100) + ' %')
            else:
                m_ana['Chiller running COP'],m_ana[compare],m_ana['VFD retrofit saving/kWh'],m_ana['VFD retrofit saving %']= 'plholder','plholder','plholder','plholder'
                del m_ana['Chiller running COP']
                del m_ana[compare]
                del m_ana['VFD retrofit saving/kWh']
                del m_ana['VFD retrofit saving %']

        m_ana = pd.DataFrame.from_dict(m_ana)
        m_ana.sort_values(by='Month', inplace=True)
    if VFDretro == 'Y':
        m_ana.to_csv(os.path.join(save_path, 'analysis' + unit + '_monthly_summary.csv'),
                     index=False,
                     encoding='utf_8_sig')
    else:
        # m_ana = m_ana.drop(m_ana.columns[-3:], axis=1, inplace=False)
        m_ana.to_csv(os.path.join(save_path, 'analysis' + unit + '_monthly_summary.csv'),
                            index=False,
                            encoding='utf_8_sig')
    return m_ana


def unit_summary_1(data, VSFS, unit, dt, save_path, language=1):
    """
    Generate VFD retrofit benefit monthly summary.

    Parameters
    ----------
    data : DataFrame
        Input data.
    VSFS : string
        Is the calculated chiller a variable speed or fix speed chiller. 'VS'
        for variable speed, 'FS' for fix speed.
    unit : string
        Unit serial number.

    Returns
    -------
    None.

    """
    months = data.month.unique()

    if VSFS == 'FS':
        compare = '变频改造后COP' if language else 'COP after VFD retrofit'
    elif VSFS == 'VS':
        compare = '变频改造前COP' if language else 'COP before VFD retrofit'
    if language:
        m_ana = {'月份': [],
                 'flag': [],
                 '预测可信度': [],
                 '平均干球温度/℃': [],
                 '平均湿球温度/℃': [],
                 '变频节能百分比': [],
                 '变频节能空间/kWh': [],
                 '运行能耗/kWh': [],
                 '平均冷冻水温/℃': [],
                 '平均冷却水温/℃': [],
                 '平均负荷百分比': [],
                 '实际运行COP': [],
                 compare: []}

        for m in months:
            temp = data[data.month == m].copy()
            m_ana['月份'].append(m)
            if temp['flag'].unique().shape[0] == 1:
                m_ana['flag'].append('%d' % temp['flag'].unique()[0])
            elif temp['flag'].unique().shape[0] == 2:
                m_ana['flag'].append(('{},{}').format(temp['flag'].unique()[0], temp['flag'].unique()[1]))
            elif temp['flag'].unique().shape[0] == 3:
                m_ana['flag'].append(('{},{},{}').format(temp['flag'].unique()[0],
                                                         temp['flag'].unique()[1], temp['flag'].unique()[2]))
            elif temp['flag'].unique().shape[0] == 4:
                m_ana['flag'].append(('{},{},{},{}').format(temp['flag'].unique()[0],
                                                            temp['flag'].unique()[1],
                                                            temp['flag'].unique()[2],
                                                            temp['flag'].unique()[3]))
            else:
                m_ana['flag'].append(('{},{},{},{},{}').format(temp['flag'].unique()[0],
                                                               temp['flag'].unique()[1],
                                                               temp['flag'].unique()[2],
                                                               temp['flag'].unique()[3],
                                                               temp['flag'].unique()[4]))

            if temp.empty:
                m_ana['预测可信度'].append('%s' % ('None'))
            elif temp['reliability'].isin(['high']).sum() > 5:
                m_ana['预测可信度'].append('%s' % ('high'))
            else:
                m_ana['预测可信度'].append('%s' % ('low'))

            m_ana['平均干球温度/℃'].append('%.1f' % (temp.OAT.mean()))
            m_ana['平均湿球温度/℃'].append('%.1f' % (temp.OAT_wb.mean()))
            if temp.Power_kWh.sum() == 0:
                m_ana['变频节能百分比'].append('%.1f' % (0) + ' %')
            else:
                m_ana['变频节能百分比'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power_kWh.sum() * 100) + ' %')
            m_ana['变频节能空间/kWh'].append('%.0f' % (temp.ES_VFD.sum() * dt))
            m_ana['运行能耗/kWh'].append('%.0f' % (temp.Power_kWh.sum() * dt))

            temp = temp[temp['Power_kWh'] > 0]
            if temp.LCW.mean() == temp.LCW.mean():
                m_ana['平均冷冻水温/℃'].append('%.1f' % (temp.LCW.mean()))
            else:
                m_ana['平均冷冻水温/℃'].append('%.1f' % (0))
            if temp.ECDW.mean() == temp.ECDW.mean():
                m_ana['平均冷却水温/℃'].append('%.1f' % (temp.ECDW.mean()))
            else:
                m_ana['平均冷却水温/℃'].append('%.1f' % (0))

            if temp.PLR.mean() == temp.PLR.mean():
                m_ana['平均负荷百分比'].append('%.1f' % (temp.PLR.mean() * 100) + ' %')
            else:
                m_ana['平均负荷百分比'].append('%.1f' % (0) + ' %')
            if temp.psm_cop_current.mean() == temp.psm_cop_current.mean():
                m_ana['实际运行COP'].append('%.1f' % (temp.psm_cop_current.mean()))
            else:
                m_ana['实际运行COP'].append('%.1f' % (0))
            if temp.psm_cop_compare.mean() == temp.psm_cop_compare.mean():
                m_ana[compare].append('%.1f' % (temp.psm_cop_compare.mean()))
            else:
                m_ana[compare].append('%.1f' % (0))

        m_ana = pd.DataFrame.from_dict(m_ana)
        m_ana.sort_values(by='月份', inplace=True)

    else:
        m_ana = {'Month': [],
                 'flag': [],
                 'Prediction reliability': [],
                 'Avg. OAT/℃': [],
                 'Avg. OAWT/℃': [],
                 'VFD retrofit saving %': [],
                 'VFD retrofit saving/kWh': [],
                 'Power/kWh': [],
                 'Avg. LCW/℃': [],
                 'Avg. ECDW/℃': [],
                 'Avg. PLR': [],
                 'Chiller running COP': [],
                 compare: [],
                 }

        for m in months:
            temp = data[data.month == m].copy()
            m_ana['Month'].append(m)
            if temp['flag'].unique().shape[0] == 1:
                m_ana['flag'].append('%d' % temp['flag'].unique()[0])
            elif temp['flag'].unique().shape[0] == 2:
                m_ana['flag'].append(('{},{}').format(temp['flag'].unique()[0], temp['flag'].unique()[1]))
            elif temp['flag'].unique().shape[0] == 3:
                m_ana['flag'].append(('{},{},{}').format(temp['flag'].unique()[0],
                                                         temp['flag'].unique()[1], temp['flag'].unique()[2]))
            elif temp['flag'].unique().shape[0] == 4:
                m_ana['flag'].append(('{},{},{},{}').format(temp['flag'].unique()[0],
                                                            temp['flag'].unique()[1],
                                                            temp['flag'].unique()[2],
                                                            temp['flag'].unique()[3]))
            else:
                m_ana['flag'].append(('{},{},{},{},{}').format(temp['flag'].unique()[0],
                                                               temp['flag'].unique()[1],
                                                               temp['flag'].unique()[2],
                                                               temp['flag'].unique()[3],
                                                               temp['flag'].unique()[4]))

            if temp.empty:
                m_ana['Prediction reliability'].append('%s' % ('None'))
            elif temp['reliability'].isin(['high']).sum() > 5:
                m_ana['Prediction reliability'].append('%s' % ('high'))
            else:
                m_ana['Prediction reliability'].append('%s' % ('low'))

            m_ana['Avg. OAT/℃'].append('%.1f' % (temp.OAT.mean()))
            m_ana['Avg. OAWT/℃'].append('%.1f' % (temp.OAT_wb.mean()))

            if temp.Power_kWh.sum() == 0:
                m_ana['VFD retrofit saving %'].append('%.1f' % (0) + ' %')
            else:
                m_ana['VFD retrofit saving %'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power_kWh.sum() * 100) + ' %')
            m_ana['VFD retrofit saving/kWh'].append('%.0f' % (temp.ES_VFD.sum() * dt))
            m_ana['Power/kWh'].append('%.0f' % (temp.Power_kWh.sum() * dt))

            temp = temp[temp['Power_kWh'] > 0]
            if temp.LCW.mean() == temp.LCW.mean():
                m_ana['Avg. LCW/℃'].append('%.1f' % (temp.LCW.mean()))
            else:
                m_ana['Avg. LCW/℃'].append('%.1f' % (0))
            if temp.ECDW.mean() == temp.ECDW.mean():
                m_ana['Avg. ECDW/℃'].append('%.1f' % (temp.ECDW.mean()))
            else:
                m_ana['Avg. ECDW/℃'].append('%.1f' % (0))

            if temp.PLR.mean() == temp.PLR.mean():
                m_ana['Avg. PLR'].append('%.1f' % (temp.PLR.mean() * 100) + ' %')
            else:
                m_ana['Avg. PLR'].append('%.1f' % (0) + ' %')
            if temp.psm_cop_current.mean() == temp.psm_cop_current.mean():
                m_ana['Chiller running COP'].append('%.1f' % (temp.psm_cop_current.mean()))
            else:
                m_ana['Chiller running COP'].append('%.1f' % (0))
            if temp.psm_cop_compare.mean() == temp.psm_cop_compare.mean():
                m_ana[compare].append('%.1f' % (temp.psm_cop_compare.mean()))
            else:
                m_ana[compare].append('%.1f' % (0))

        m_ana = pd.DataFrame.from_dict(m_ana)
        m_ana.sort_values(by='Month', inplace=True)
    # m_ana.to_csv(os.path.join(save_path, 'prediction' + unit + '_monthly_summary.csv'),
    #              index=False,
    #              encoding='utf_8_sig')
    return m_ana


def annual_summary(summary, temp, dt, unit, VSFS, type, VFDretro):
    summary['SN'].append(unit)
    if (VFDretro == 'Y') | ((VFDretro == 'N') & (VSFS == 'FS') & (type == '30XW')):
        #modified by xuling 23/6/27, 计算Ton和改造后的power
        temp["Ton"] = temp["Power"] * temp["psm_cop_current"]/3.517
        summary['Ton'].append('%d' % (temp["Ton"].sum() * dt))
        temp["Power_vs"] = temp["Ton"]*3.517 / temp["psm_cop_compare"]
        summary['Power_vs'].append('%d' % (temp["Power_vs"].sum()*dt))
    # else:#modified by xuling 23/4/28, 螺杆机暂时不支持计算psm_cop.所以增加了一个if loop。将螺杆Ton_current&Ton_compare赋值为NaN
    #     summary['Ton_current'].append(np.nan)
    #     summary['Ton_compare'].append(np.nan)

    # modified by xuling 23/4/24, 计算年度合计PLR
    summary["PLR_avg"].append("%d" % (temp["PLC"].mean()*100) +"%")
    summary['ES_cond'].append('%d' % (max((temp.Power * (1 - temp.eta_cond)).sum() * dt, 0)))
    summary['ES_cond%'].append(
        '%.1f' % (max((temp.Power * (1 - temp.eta_cond)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
    summary['deltaT_cond'].append('%.1f' % ((temp.LCDW - temp.ECDW).mean()))
    summary['app_cond'].append('%.1f' % ((temp.SDT - temp.LCDW).mean()))
    summary['ES_evap'].append('%d' % (max((temp.Power * (1 - temp.eta_evap)).sum() * dt, 0)))
    summary['ES_evap%'].append(
        '%.1f' % (max((temp.Power * (1 - temp.eta_evap)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
    summary['deltaT_evap'].append('%.1f' % ((temp.ECW - temp.LCW).mean()))
    if (VFDretro == 'Y') | ((VFDretro == 'N') & (VSFS == 'FS') & (type == '30XW')):
        summary['ES_VFD'].append('%d' % (temp.ES_VFD.sum() * dt))
        summary['ES_VFD%'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power.sum() * 100) + '%')
    summary['app_evap'].append('%.1f' % ((temp.LCW - temp.SST).mean()))
    summary['total_power'].append('%d' % (temp.Power.sum() * dt))
    if 'Hrs' in temp.columns:
        dHrs = temp.Hrs - temp.Hrs.shift(1)
        summary['runhr'].append('%d' % (max((dHrs[(dHrs > 0) & (dHrs < 10)]).sum(),
                                            len(temp) * dt)))
    else:
        summary['runhr'].append('%d' % (len(temp) * dt))

    return summary


def annual_summary_1(summary, temp, dt, unit, VSFS, VFDretro):
    summary['SN'].append(unit)
    summary['total_power'].append('%d' % (temp.Power_kWh.sum() * dt))
    summary['real_power'].append('%d' % (temp[temp['flag'] == 0].Power_kWh.sum() * dt))
    summary['predict_power'].append('%d' % (temp[temp['flag'] != 0].Power_kWh.sum() * dt))
    if (VFDretro == 'Y') | ((VFDretro == 'N') & (VSFS == 'FS')):
        summary['ES_VFD'].append('%d' % (temp.ES_VFD.sum() * dt))
        summary['real_ES_VFD'].append('%d' % (temp[temp['flag'] == 0].ES_VFD.sum() * dt))
        summary['predict_ES_VFD'].append('%d' % (temp[temp['flag'] != 0].ES_VFD.sum() * dt))

        summary['ES_VFD%'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power_kWh.sum() * 100) + '%')
        summary['real_ES_VFD%'].append(
            '%.1f' % (temp[temp['flag'] == 0].ES_VFD.sum() / temp[temp['flag'] == 0].Power_kWh.sum() * 100) + '%')
        summary['predict_ES_VFD%'].append(
            '%.1f' % (temp[temp['flag'] != 0].ES_VFD.sum() / temp[temp['flag'] != 0].Power_kWh.sum() * 100) + '%')

    return summary


def FH_max(data, eta_d, LCW_nor=7, ECDW_nor=32, ref='R134a'):
    P_0d = Props('P', 'T', LCW_nor - 1.8 + 273.15, 'Q', 1, ref)
    P_2d = Props('P', 'T', ECDW_nor + 5 + 2.8 + 273.15, 'Q', 1, ref)
    P_0 = data.SP.median()
    P_2 = data.DP[data.DP < (data.DP.mean() + 3 * data.DP.std())].max()
    P_2 = P_2d if P_2 < P_2d else P_2
    P_0 = P_0d if P_0 > P_0d else P_0
    v_0 = 1 / Props('D', 'P', P_0, 'Q', 1, ref)
    s_suc = Props('S', 'P', P_0, 'Q', 1, ref)
    h_dis_i = Props('H', 'P', P_2, 'S', s_suc, ref)
    h_suc = Props('H', 'P', P_0, 'Q', 1, ref)
    h_dis = h_suc + (h_dis_i - h_suc) / eta_d

    v_2_is = 1 / Props('D', 'P', P_2, 'S', s_suc, ref)
    v_2 = 1 / Props('D', 'P', P_2, 'H', h_dis, ref)

    F_emp = v_0 / (h_dis - h_suc)
    H_emp = (h_dis_i - h_suc)
    H_emp *= (P_2 * v_2 - P_0 * v_0) / (np.log(P_2 * v_2 / P_0 / v_0))
    H_emp /= (P_2 * v_2_is - P_0 * v_0) / (np.log(P_2 * v_2_is / P_0 / v_0))

    return F_emp, H_emp


def FS_Map(data, DP, CDT, unit):
    '''
    Function for generating fix speed polytropic efficiency from suction
    pressure, discharge pressure and discharge temperature.

    Parameters
    ----------
    data : DataFrame
        Input data.
    DP : string, optional
        Column name of discharge pressure.
    CDT : string, optional
        Column name of discharge temperature.

    Returns
    -------
    data : DataFrame
        Output data.
    regressor : regressor
        KNN regressor for polytropic efficiency.

    '''

    ref = 'R134a'
    v_0 = 1 / Props('D', 'P', data.SP, 'Q', 1, ref)
    P_0 = data.SP
    # h_cdo = Props('H','P',data[DP],'Q',0,ref)
    h_dis_i = Props('H', 'P', data[DP], 'S', data.s_suc, ref)
    h_dis = Props('H', 'P', data[DP], 'T', data[CDT] + 273.15, ref)

    v_2_is = 1 / Props('D', 'P', data[DP], 'S', data.s_suc, ref)
    v_2 = 1 / Props('D', 'P', data[DP], 'T', data[CDT] + 273.15, ref)
    P_2 = data[DP]

    data['F_emp'] = data.PLC * v_0 / (h_dis - data.h_suc)
    data['H_emp'] = (h_dis_i - data.h_suc)
    data['H_emp'] *= (P_2 * v_2 - P_0 * v_0) / ((P_2 * v_2 / P_0 / v_0).apply(np.log))
    data['H_emp'] /= (P_2 * v_2_is - P_0 * v_0) / ((P_2 * v_2_is / P_0 / v_0).apply(np.log))
    # eta_d = Eta_Design(data)
    # eta_d = 0.8 if eta_d>0.8 else eta_d
    eta_d = 0.8
    F_nor, H_nor = FH_max(data, eta_d)
    data['eta_poly'] = data.H_emp / (h_dis - data.h_suc)

    # F_max = data.F_emp[data['GV']>80].median()
    # H_max = data.H_emp[data['GV']>80].median()
    # F_max = data.F_emp[data.F_emp<(data.F_emp.mean()+3*data.F_emp.std())].max()
    H_max = data.H_emp[data.H_emp < (data.H_emp.mean() + 3 * data.H_emp.std())].max()
    # lr = FS_lrmap(data)

    # F_max = F_nor if F_nor>F_max else F_max
    H_nor = H_nor if H_nor > H_max else H_max

    data['F_emp'] /= F_nor
    # data['H_emp'] /= data['H_emp'].max()
    data['H_emp'] /= H_nor
    # data['H_emp'] /= H_max
    # regressor = KNNR(5)
    # regressor.fit(data[['F_emp','H_emp']],data.eta_poly)

    return data, eta_d
    # return data, regressor


# def QuantileFitting(data, X, Y, intercept = True, quantile = 0.999,nbins = 20, nsample = 500):
#
#     train = []
#     X_min, X_max = data[X].min(), data[X].max()
#     for i in range(nbins):
#         temp = data[(data[X]>=(X_min+i/nbins*(X_max-X_min)))
#                     &(data[X]<(X_min+(i+1)/nbins*(X_max-X_min)))]
#         ntemp = len(temp)
#         if ntemp>0:
#             if ntemp>int(nsample/nbins):
#                 train.append(temp.sample(int(nsample/nbins),random_state=1))
#             else:
#                 train.append(temp)
#     train = pd.concat(train)
#
#     x=train[[X]]
#     qr = QuantileRegressor(quantile = quantile,
#                            alpha = 0,
#                            fit_intercept = intercept).fit(x,train[Y])
#
#     return qr

def Eta_Design(data):
    poly = PolynomialFeatures(degree=2)
    X = poly.fit_transform(data[['LCW', 'ECDW', 'PLC']])
    Y = data.eta_comp
    lr = LinearRegression()
    lr.fit(X, Y)

    return lr.predict(poly.fit_transform([[7, 32, 1]]))[0]


# def FH_VS(data, N_lim):
#     '''
#
#     Calculate flow fraction and head fraction if it is a variable speed chiller.
#     ----------
#     data : DataFrame
#         Input data.
#     N_lim : float
#         VFD speed percentage low limit.
#
#     Returns
#     -------
#     data : DataFrame
#         Output data.
#
#     '''
#
#     qr1 = QuantileFitting(data, 'F_emp', 'H_emp')
#     data['H_emp_n'] = data.H_emp - 1
#     data['F_emp_n'] = data.F_emp - 1
#     qr2 = QuantileFitting(data, 'F_emp_n', 'H_emp_n', False)
#     a1 = qr1.coef_[0]
#     b1 = qr1.intercept_
#     a2 = qr2.coef_[0]
#     b2 = qr2.intercept_ + 1 - a2
#     x_intercept = (b2 - b1) / (a1 - a2)
#     c = data.H_emp/(data.F_emp**2)
#     F_surge1 = (a1+(a1**2+4*c*b1)**0.5)/2/c
#     F_surge2 = (a2+(a2**2+4*c*b2)**0.5)/2/c
#     F_surge1[F_surge1>F_surge2] = F_surge2
#     F_surge1[F_surge1>1] = 1
#     N = data.F_emp/F_surge1
#     # data['H_sqrt'] = data.H_emp**0.5
#     # N = data[['F_emp','H_sqrt']].max(axis=1)
#     N[N<N_lim] = N_lim
#     N[N>1] = 1
#     data['F_vs'] = data.F_emp/N
#     data['H_vs'] = data.H_emp/(N**2)
#
#     return data, qr1, qr2, x_intercept

def FS_lrmap(train, eta_d):
    poly = PolynomialFeatures(degree=2)
    train['F_emp_n'] = 1 - train['F_emp']
    train['H_emp_n'] = 1 - train['H_emp']
    X = poly.fit_transform(train[['F_emp_n', 'H_emp_n']])[:, 1:]
    Y = train.eta_poly - eta_d
    lr = LinearRegression(fit_intercept=False)
    lr.fit(X, Y)

    return lr

def merge_monthly_analysis_result(dfa,dfb, language):
    st_cname = dfa.columns
    dfa.index = dfa[st_cname[0]]
    dfb.index = dfb[st_cname[0]]
    df = pd.DataFrame()
    sub_name = [['leakage_index','Chiller running COP','COP after VFD retrofit','VFD retrofit saving/kWh','VFD retrofit saving %'],
            ['制冷剂泄漏指数','实际运行COP','变频改造后COP','变频节能空间/kWh','变频节能百分比']]

    if len(dfa)>len(dfb):
        longer = [dfa,dfb]
    else:
        longer = [dfb,dfa]

    df[st_cname[1]] = dfa[st_cname[1]].astype('int')+dfb[st_cname[1]].astype('int')
    df[st_cname[1]] = df[st_cname[1]].fillna(value=longer[0][st_cname[1]].astype('int')).astype('int')

    df[st_cname[2]+'_A_loop'] = dfa[st_cname[2]]
    df[st_cname[2]+'_A_loop'] = df[st_cname[2]+'_A_loop'].fillna(value='0').astype('int')
    df[st_cname[2]+'_B_loop'] = dfb[st_cname[2]]
    df[st_cname[2]+'_B_loop'] = df[st_cname[2]+'_B_loop'].fillna(value='0').astype('int')

    df[st_cname[3]] = longer[0][st_cname[3]]
    df[st_cname[4]] = longer[0][st_cname[4]]

    df[st_cname[5]+'_A_loop'] = dfa[st_cname[5]]
    df[st_cname[5]+'_A_loop'] = df[st_cname[5]+'_A_loop'].fillna(value='0%')
    df[st_cname[5]+'_B_loop'] = dfb[st_cname[5]]
    df[st_cname[5]+'_B_loop'] = df[st_cname[5]+'_B_loop'].fillna(value='0%')

    # df[st_cname[6]+'_A_loop'] = dfa[st_cname[6]]
    # df[st_cname[6]+'_A_loop'] = df[st_cname[6]+'_A_loop'].fillna(value='0%')
    # df[st_cname[6]+'_B_loop'] = dfb[st_cname[6]]
    # df[st_cname[6]+'_B_loop'] = df[st_cname[6]+'_B_loop'].fillna(value='0%')

    df[st_cname[6]] = longer[0][st_cname[6]]

    df[st_cname[7]+'_A_loop'] = dfa[st_cname[7]]
    df[st_cname[7]+'_A_loop'] = df[st_cname[7]+'_A_loop'].fillna(value='-')
    df[st_cname[7]+'_B_loop'] = dfb[st_cname[7]]
    df[st_cname[7]+'_B_loop'] = df[st_cname[7]+'_B_loop'].fillna(value='-')

    df[st_cname[8]] = dfa[st_cname[8]].astype('int')+dfb[st_cname[8]].astype('int')
    df[st_cname[8]] = df[st_cname[8]].fillna(value=longer[0][st_cname[8]].astype('int')).astype('int')

    df[st_cname[9]] = (df[st_cname[8]]/df[st_cname[1]]*100).round(1).astype('str')+"%"

    df[st_cname[10]] = longer[0][st_cname[10]]

    df[st_cname[11]+'_A_loop'] = dfa[st_cname[11]]
    df[st_cname[11]+'_A_loop'] = df[st_cname[11]+'_A_loop'].fillna(value='-')
    df[st_cname[11]+'_B_loop'] = dfb[st_cname[11]]
    df[st_cname[11]+'_B_loop'] = df[st_cname[11]+'_B_loop'].fillna(value='-')

    df[st_cname[12]] = dfa[st_cname[12]].astype('int')+dfb[st_cname[12]].astype('int')
    df[st_cname[12]] = df[st_cname[12]].fillna(value=longer[0][st_cname[12]].astype('int')).astype('int')

    df[st_cname[13]] = (df[st_cname[12]]/df[st_cname[1]]*100).round(1).astype('str')+"%"

    if dfb.empty:
        del df[st_cname[2]+'_B_loop']
        del df[st_cname[5]+'_B_loop']
        del df[st_cname[7] + '_B_loop']
        del df[st_cname[11]+'_B_loop']

    if sub_name[language][1] in st_cname:
        if not dfb.empty:
            qa_before, qb_before = dfa[sub_name[language][1]].astype('float') * dfa[st_cname[1]].astype('int'), dfb[sub_name[language][1]].astype(
                'float') * dfb[st_cname[1]].astype('int')
            df[sub_name[language][1]] = round(
                qa_before.add(qb_before, fill_value=0)/ dfa[st_cname[1]].astype('int').add(dfb[st_cname[1]].astype('int'), fill_value=0), 1)
        else:
            qa_before = dfa[sub_name[language][1]].astype('float') * dfa[st_cname[1]].astype('int')
            df[sub_name[language][1]] = round(qa_before / dfa[st_cname[1]].astype('int'), 1)

    if sub_name[language][2] in st_cname:
        if not dfb.empty:
            qa_after, qb_after = dfa[sub_name[language][2]].astype('float') * dfa[st_cname[1]].astype('int'), dfb[sub_name[language][2]].astype(
                'float') * dfb[st_cname[1]].astype('int')
            df[sub_name[language][2]] = round(qa_after.add(qb_after, fill_value=0) / dfa[st_cname[1]].astype('int').add(dfb[st_cname[1]].astype('int'), fill_value=0) ,1)
        else:
            qa_after = dfa[sub_name[language][2]].astype('float') * dfa[st_cname[1]].astype('int')
            df[sub_name[language][2]] = round(qa_after / dfa[st_cname[1]].astype('int'), 1)

    if sub_name[language][3] in st_cname:
        if not dfb.empty:
            df[sub_name[language][3]] = dfa[sub_name[language][3]].astype('int').add(dfb[sub_name[language][3]].astype('int'), fill_value=0)
        else:
            df[sub_name[language][3]] = dfa[sub_name[language][3]].astype('int')
        df[sub_name[language][3]] = df[sub_name[language][3]].fillna(value=longer[0][sub_name[language][3]].astype('int')).astype('int')

    if sub_name[language][4] in st_cname:
        if not dfb.empty:
            df[sub_name[language][4]] = (dfa[sub_name[language][3]].astype('int').add(dfb[sub_name[language][3]].astype('int'),fill_value=0) /
                                dfa[st_cname[1]].astype('int').add(dfb[st_cname[1]].astype('int'),fill_value=0) * 100).round(1).astype('str') + "%"
        else:
            df[sub_name[language][4]] = (dfa[sub_name[language][3]].astype('int') /
                                         dfa[st_cname[1]].astype('int') * 100).round(1).astype('str') + "%"

    if sub_name[language][0] in st_cname:
        df[sub_name[language][0]+'_A_loop'] = dfa[sub_name[language][0]].astype('float')
        if not dfb.empty:
            df[sub_name[language][0]+'_B_loop'] = dfb[sub_name[language][0]].astype('float')

    if language == 1:
        df.rename(columns={'平均电流百分比_A_loop': '平均负荷百分比_A_loop',
                            '平均电流百分比_B_loop': '平均负荷百分比_B_loop'},
                            inplace=True)
    else:
        df.rename(columns={'Avg. percent line current_A_loop': 'Avg. part load ratio_A_loop',
                           'Avg. percent line current_B_loop': 'Avg. part load ratio_B_loop'},
                  inplace=True)

    return df

def merge_analysis_prediction_result(dfa,dfb):
    st_cname = dfa.columns
    df = pd.DataFrame(index=dfa.index)

    df[st_cname[0]] = dfa[st_cname[0]]
    df[st_cname[1]] = dfa[st_cname[1]]
    df[st_cname[2]] = dfa[st_cname[2]]
    df[st_cname[3]] = dfa[st_cname[3]]
    df[st_cname[4]] = dfa[st_cname[4]]

    df[st_cname[5]] = ((dfa[st_cname[6]].astype('int') + dfb[st_cname[6]].astype('int')) /
                            (dfa[st_cname[7]].astype('int') + dfb[st_cname[7]].astype('int')) * 100).round(1).astype(
            'str') + "%"
    df[st_cname[6]] = dfa[st_cname[6]].astype('int') + dfb[st_cname[6]].astype('int')
    df[st_cname[7]] = dfa[st_cname[7]].astype('int') + dfb[st_cname[7]].astype('int')
    df[st_cname[8]] = round((dfa[st_cname[8]].astype('float') + dfb[st_cname[8]].astype('float')) / 2, 1)
    df[st_cname[9]] = round((dfa[st_cname[9]].astype('float') + dfb[st_cname[9]].astype('float')) / 2, 1)
    df[st_cname[10]] = round((dfa[st_cname[10]].str.split('%').str[0].astype('float')+ dfb[st_cname[10]].str.split('%').str[0].astype('float')) / 2,1).astype('str') + "%"

    df[st_cname[11]] = round((dfa[st_cname[11]].astype('float') * dfa[st_cname[7]].astype('int') + dfb[st_cname[11]].astype('float') * dfb[st_cname[7]].astype('int')) /
                             df[st_cname[7]], 1)
    df[st_cname[12]] = round((dfa[st_cname[12]].astype('float') * dfa[st_cname[7]].astype('int') + dfb[st_cname[12]].astype('float') * dfb[st_cname[7]].astype('int')) /
                             df[st_cname[7]], 1)

    return df

def merge_annual_analysis_result(dfa,dfb):
    st_cname = dfa.columns
    df = pd.DataFrame()

    df[st_cname[0]] = dfa[st_cname[0]]
    if not dfb.empty:
        df[st_cname[1]] = dfa[st_cname[1]].astype('int')+dfb[st_cname[1]].astype('int')
        df[st_cname[9]] = dfa[st_cname[9]].astype('int')+dfb[st_cname[9]].astype('int')
        df[st_cname[5]] = dfa[st_cname[5]].astype('int') + dfb[st_cname[5]].astype('int')
        df[st_cname[4] + '_B_loop'] = dfb[st_cname[4]]
        df[st_cname[8] + '_B_loop'] = dfb[st_cname[8]]
        df[st_cname[10] + '_B_loop'] = dfb[st_cname[10]]
        df[st_cname[11] + '_B_loop'] = dfb[st_cname[11]]
    else:
        df[st_cname[1]] = dfa[st_cname[1]].astype('int')
        df[st_cname[9]] = dfa[st_cname[9]].astype('int')
        df[st_cname[5]] = dfa[st_cname[5]].astype('int')
    df[st_cname[2]] = (df[st_cname[1]]/df[st_cname[9]]*100).round(1).astype('str')+"%"
    df[st_cname[3]] = dfa[st_cname[3]]
    df[st_cname[4]+'_A_loop'] = dfa[st_cname[4]]
    df[st_cname[6]] = (df[st_cname[5]]/df[st_cname[9]]*100).round(1).astype('str')+"%"
    df[st_cname[7]] = dfa[st_cname[7]]
    df[st_cname[8]+'_A_loop'] = dfa[st_cname[8]]
    df[st_cname[10]+'_A_loop'] = dfa[st_cname[10]]
    df[st_cname[11] + '_A_loop'] = dfa[st_cname[11]]  # added PLR_avg by xuling 23/4/28


    if 'ES_VFD' in st_cname:
        if not dfb.empty:
            df['ES_VFD'] = dfa['ES_VFD'].astype('int') + dfb['ES_VFD'].astype('int')
        else:
            df['ES_VFD'] = dfa['ES_VFD'].astype('int')
    if 'ES_VFD%' in st_cname:
        df['ES_VFD%'] = (df['ES_VFD'] / df[st_cname[9]] *100).round(1).astype('str')+"%"
    #Modified by xuling 6/27, 以前新增的两列为Ton_current和Ton_compare,现在修改为：新增的两列为power_vs和Ton
    if 'Ton' in st_cname:
        if not dfb.empty:
            df['Ton'] = dfa['Ton'].astype('int') + dfb['Ton'].astype('int')
        else:
            df['Ton'] = dfa['Ton'].astype('int')
    if 'Power_vs' in st_cname:
        if not dfb.empty:
            df['Power_vs'] = dfa['Power_vs'].astype('int') + dfb['Power_vs'].astype('int')
        else:
            df['Power_vs'] = dfa['Power_vs'].astype('int')

    return df

def merge_annual_analysis_prediction_result(dfa,dfb):
    df = {}
    df['SN'] = dfa['SN']
    df['total_power'] = int(dfa['total_power'][0]) + int(dfb['total_power'][0])
    df['predict_power'] = int(dfa['predict_power'][0]) + int(dfb['predict_power'][0])
    df['real_power'] = int(dfa['real_power'][0]) + int(dfb['real_power'][0])
    df['real_ES_VFD'] = int(dfa['real_ES_VFD'][0]) + int(dfb['real_ES_VFD'][0])
    df['predict_ES_VFD'] = int(dfa['predict_ES_VFD'][0]) + int(dfb['predict_ES_VFD'][0])
    df['ES_VFD'] = int(dfa['ES_VFD'][0]) + int(dfb['ES_VFD'][0])
    df['real_ES_VFD%'] = str(round(df['real_ES_VFD'] / df['real_power'] * 100,1)) + "%"
    df['predict_ES_VFD%'] = str(round(df['predict_ES_VFD'] / df['predict_power'] * 100,1)) + "%"
    df['ES_VFD%'] = str(round(df['ES_VFD'] / df['total_power'] * 100,1)) + "%"

    return df
    

# def EMP_ES(data,unit,DP='DP',CDT='CDT',N_lim=0.65):
#     '''
#     VFD retrofit benefit estimation from empirical method.
#
#     Parameters
#     ----------
#     data : DataFrame
#         Input data.
#     unit : string
#         Unit serial number.
#     DP : string, optional
#         Column name of discharge pressure. The default is 'DP'.
#     CDT : string, optional
#         Column name of discharge temperature. The default is 'CDT'.
#     N_lim : float, optional
#         VFD speed percentage low limit. The default is 0.65.
#
#     Returns
#     -------
#     None.
#
#     '''
#
#     # data, regressor = FS_Map(data,DP,CDT,unit)
#     data, eta_d = FS_Map(data,DP,CDT,unit)
#     FS_lr = FS_lrmap(data,eta_d)
#     data, qr1, qr2, x_intercept = FH_VS(data, N_lim)
#
#     data['Fn'] = 1 - data.F_vs
#     data['Hn'] = 1 - data.H_vs
#     poly = PolynomialFeatures(degree=2)
#     X = poly.fit_transform(data[['Fn','Hn']])[:,1:]
#     data['eta_emp_vs'] = FS_lr.predict(X) + eta_d
#     # data['eta_emp_vs'] = regressor.predict(data[['F_vs','H_vs']])
#     data['ES_EMP'] = data.Power*(1-data.eta_poly/data.eta_emp_vs)
#
#     sns.scatterplot(data.SDT,data.COP_ref, label = 'before retrofit')
#     sns.scatterplot(data.SDT,data.COP_ref/data.eta_comp * data.eta_emp_vs, label = 'after retrofit')
#     plt.ylim(0,)
#     plt.legend()
#     plt.show()
#
#     sns.scatterplot(data.F_emp,data.H_emp,data.eta_poly,palette='rainbow')
#     plt.plot([0.1,x_intercept],qr1.predict([[0.1],[x_intercept]]),c='r',ls='--')
#     plt.plot([x_intercept,1],qr2.predict([[x_intercept-1],[1-1]])+1,c='r',ls='--')
#     plt.plot([1,1.05],[1,0.91],c='r',ls='--')
#     plt.plot([1.05,1.05],[0.91,0],c='r',ls='--')
#     plt.xlim(0,)
#     plt.ylim(0,)
#     plt.show()
#
#     sns.scatterplot(data.F_emp,data.H_emp,data.eta_emp_vs,palette='rainbow')
#     plt.plot([0.1,x_intercept],qr1.predict([[0.1],[x_intercept]]),c='r',ls='--')
#     plt.plot([x_intercept,1],qr2.predict([[x_intercept-1],[1-1]])+1,c='r',ls='--')
#     plt.plot([1,1.05],[1,0.91],c='r',ls='--')
#     plt.plot([1.05,1.05],[0.91,0],c='r',ls='--')
#     plt.xlim(0,)
#     plt.ylim(0,)
#     plt.show()
#
#     sns.scatterplot(data['GV'],data.F_emp,palette='rainbow')
#     plt.xlim(0,100)
#     plt.ylim(0,1)
#     plt.show()
#
#     sns.scatterplot(data.F_emp,data.eta_poly,palette='rainbow')
#     plt.xlim(0,1)
#     plt.ylim(0,1)
#     plt.show()
#
#     sns.scatterplot(data['GV'],data.H_emp,palette='rainbow')
#     plt.xlim(0,100)
#     plt.ylim(0,1)
#     plt.show()
#
#     sns.scatterplot(data.H_emp,data.eta_poly,palette='rainbow')
#     plt.xlim(0,1)
#     plt.ylim(0,1)
#     plt.show()
#
#     if 'psm_fs_cop' in data.columns:
#         plt.title(unit+' FS COP from chiller & compressor map')
#         sns.scatterplot(data.psm_fs_cop,data.COP_comp_fs)
#         l = min(data.psm_fs_cop.min(),data.COP_comp_fs.min())*0.9
#         h = max(data.psm_fs_cop.max(),data.COP_comp_fs.max())*1.1
#         plt.plot([l,h],[l,h],c='r',ls='--')
#         plt.xlim(l,h)
#         plt.ylim(l,h)
#         plt.show()
#
#         plt.title(unit+' VS COP from chiller & compressor map')
#         sns.scatterplot(data.psm_vs_cop,data.COP_comp_vs)
#         l = min(data.psm_vs_cop.min(),data.COP_comp_vs.min())*0.9
#         h = max(data.psm_vs_cop.max(),data.COP_comp_vs.max())*1.1
#         plt.plot([l,h],[l,h],c='r',ls='--')
#         plt.xlim(l,h)
#         plt.ylim(l,h)
#         plt.show()
#
#         ES_PSM_per = (data.Power*(1-data.psm_fs_cop/data.psm_vs_cop)).sum()/data.Power.sum()*100
#         print('Energy saving potential from PSM: %.1f'%ES_PSM_per+' %')
#
#         ES_comp_per = (data.Power*(1-data.COP_comp_fs/data.COP_comp_vs)).sum()/data.Power.sum()*100
#         print('Energy saving potential from compressor map: %.1f'%ES_comp_per+' %')
#
#     ES_EMP_per = data.ES_EMP.sum()/data.Power.sum()*100
#     print(unit)
#     print('Total kWh: %d kWh'%(data.Power.sum()/4))
#     # print('Total runtime: %d hrs'%(data.Hrs.max()-data.Hrs.min()))
#     print('Energy saving potential from empirical: %.1f'%ES_EMP_per+' %')
#
#     return data

sns.set_style('darkgrid')
# plt.rcParams['font.sans-serif'] = ['simhei','Arial']
# plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if __name__ == '__main__':

    # Ecat_COP_chart()
    # PSM_COP_chart()
    VFDretro = input('Include VFD retrofit analysis?(Y/N): ')

    units = {
        '190401211': [datetime.datetime(2022, 2, 9, 10), 648, 805],
        '190401210': [datetime.datetime(2022, 2, 9, 10), 648, 805],
        '190300905': [datetime.datetime(2022, 2, 9, 10), 648, 805],
        '190300914': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190300998': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190401028': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190401249': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190401250': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190401230': [datetime.datetime(2021, 4, 23, 15), 648, 805],
        '190702422': [datetime.datetime(2020, 1, 1), 910, 1500],
        '200401026': [datetime.datetime(2000, 1, 1), 0, 0],
        'XR4L4006': [datetime.datetime(2000, 1, 1), 0, 0],
        'XR4L4008': [datetime.datetime(2000, 1, 1), 0, 0],
        'XR4L4007': [datetime.datetime(2000, 1, 1), 0, 0],
        'XR4L4009': [datetime.datetime(2000, 1, 1), 0, 0],
    }
    data = []
    summary = {'SN': [],
               'ES_cond': [],
               'ES_cond%': [],
               'deltaT_cond': [],
               'app_cond': [],
               'ES_evap': [],
               'ES_evap%': [],
               'deltaT_evap': [],
               'app_evap': [],
               'total_power': [],
               'runhr': []}
    folder = 'data'
    if VFDretro == 'Y':
        summary['ES_VFD'] = []
        summary['ES_VFD%'] = []
    try:
        os.mkdir(folder)
    except:
        pass
    fns = os.listdir(folder)
    for root, _, fns in os.walk(folder):
        for fn in fns:
            data_unit = input('Unit of %s data(English/Metric): ' % fn)
            temp, unit = get_data(units, os.path.join(root, fn), data_unit)
            # temp = temp[temp.Power<400]
            # temp['VFD'][temp['VFD']<20] = 100
            dt = (temp.DateTime - temp.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
            temp, hA_evap_max, hA_cond_max, tonnage = Cal_eta(temp, unit, None, None)
            current_working_dir = os.getcwd()
            file_path_and_name = os.path.abspath(__file__)
            file_full_path_up = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_weather_path = os.path.join(file_full_path_up, "weather", "CN_Henan_Zhengzhou_366.pkl")
            temp = Mod_ECDW_Temp(temp, file_weather_path)
            if temp.empty:
                print('%s no available data' % (unit))
                continue
            if VFDretro == 'Y':
                ton = input('Please input nominal capacity of %s (Ton): ' % unit)
                try:
                    tonnage = float(ton)
                except:
                    pass
                # while True:
                #     LCWn = input('Please input design LCW of %s (C): '%unit)
                #     if LCWn == '': 
                #         LCWn = 7
                #         break
                #     try:
                #         LCWn = float(LCWn)
                #         break
                #     except:
                #         pass
                # while True:
                #     ECDWn = input('Please input design ECDW of %s (C): '%unit)
                #     if ECDWn == '':
                #         ECDWn = 35
                #         break
                #     try:
                #         ECDWn = float(ECDWn)
                #         break
                #     except:
                #         pass
                while True:
                    VSFS = input('Is %s a fix speed or variable speed chiller?(FS/VS): ' % unit)
                    if VSFS in ['VS', 'FS']: break
                temp = PSM_ES(temp, unit, tonnage, hA_evap_max, hA_cond_max, VSFS, True, 'result', cop_mod_ECDW=True)
                # temp = EMP_ES(temp, unit)
                # temp = PSM_ES(temp, unit, int(tonnage))
            # plot_data(temp,unit,units)
            Mark_Data(temp)
            Plot_Data(temp, unit)
            data.append(temp)
            # continue
            if VFDretro == 'Y':
                unit_summary(temp, VSFS, unit, dt, 'result')
            temp.to_csv('result/%s.csv' % unit,
                        encoding='utf_8_sig')
            summary['SN'].append(unit)
            summary['ES_cond'].append('%d' % (max((temp.Power * (1 - temp.eta_cond)).sum() * dt, 0)))
            summary['ES_cond%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_cond)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            summary['deltaT_cond'].append('%.1f' % ((temp.LCDW - temp.ECDW).mean()))
            summary['app_cond'].append('%.1f' % ((temp.SDT - temp.LCDW).mean()))
            summary['ES_evap'].append('%d' % (max((temp.Power * (1 - temp.eta_evap)).sum() * dt, 0)))
            summary['ES_evap%'].append(
                '%.1f' % (max((temp.Power * (1 - temp.eta_evap)).sum() / (temp.Power.sum()) * 100, 0)) + '%')
            summary['deltaT_evap'].append('%.1f' % ((temp.ECW - temp.LCW).mean()))
            if VFDretro == 'Y':
                summary['ES_VFD'].append('%d' % (temp.ES_VFD.sum() * dt))
                summary['ES_VFD%'].append('%.1f' % (temp.ES_VFD.sum() / temp.Power.sum() * 100) + '%')
            summary['app_evap'].append('%.1f' % ((temp.LCW - temp.SST).mean()))
            summary['total_power'].append('%d' % (temp.Power.sum() * dt))
            if 'Hrs' in temp.columns:
                dHrs = temp.Hrs - temp.Hrs.shift(1)
                summary['runhr'].append('%d' % (max((dHrs[(dHrs > 0) & (dHrs < 10)]).sum(),
                                                    len(temp) * dt)))
            else:
                summary['runhr'].append('%d' % (len(temp) * dt))
            # summary['runhr'].append('%d'%(len(temp)*dt))
    data = pd.concat(data)
    summary = pd.DataFrame.from_dict(summary)
    summary.rename(columns={'SN': '序列号',
                            'ES_cond': '冷凝器节能空间kWh',
                            'ES_cond%': '冷凝器节能空间%',
                            'deltaT_cond': '冷却水温差℃',
                            'app_cond': '冷凝器趋近温度℃',
                            'ES_evap': '蒸发器节能空间kWh',
                            'ES_evap%': '蒸发器节能空间%',
                            'deltaT_evap': '冷冻水温差℃',
                            'ES_VFD': '变频改造节能空间kWh',
                            'ES_VFD%': '变频改造节能空间%',
                            'app_evap': '蒸发器趋近温度℃',
                            'total_power': '总功耗kWh',
                            'runhr': '运行时间Hrs'},
                   inplace=True)
    summary.to_csv('result/summary.csv',
                   index=False,
                   encoding='utf_8_sig')

    # VFD_ES(data,['XR4L4007','XR4L4009'],datetime.datetime(2021,4,10))
