# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:07:24 2023

@author: chens6
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from advanced_data_analytics_tool import Rename_Data
import datetime
from CoolProp.CoolProp import PropsSI
# import HX_Analysis_Tool as HAT


def CHTP(fn='Backward_Verification_chiller_list.xlsx'):

    df = pd.read_excel(fn, header=0)
    df = df.astype({'Installed Product: Serial Number': 'str'})
    df.set_index(['Installed Product: Serial Number'], inplace=True)

    return df


def Read_Data(folder, chtp):

    fnss = os.walk(folder['data'])
    des, des_on, des_off = [], [], []
    for root, dirs, fns in fnss:
        for fn in fns:
            area = root.split('\\')[-1]
            if not 'XR' in fn:
                continue
            print('--'*20, area, fn, root)
            sn = fn.split('.')[-2]

            tp = chtp.loc[sn, 'Type']
            # if ('19XR' not in tp) and ('19DV' not in tp):
            #     continue
            if type(tp) != str:
                tp = chtp.loc[sn, 'Type'].values[0]
            # TD = chtp.loc[sn, 'Tentative date']
            try:
                TD = chtp.loc[(chtp.index == sn) & (
                    chtp['Location'] == area), 'Tentative date'].values[0]
            except:
                TD = chtp.loc[sn, 'Tentative date']

            df = pd.read_csv(os.path.join(root, fn))
            if ('XR' in tp) or ('19DV' in tp):
                # df.dropna(axis=1, thresh = int(0.2*df.shape[0]), inplace=True)
                tmp = Rename_Data(df)
                de, de_on, de_off = Resample_Data(tmp, sn, tp, folder, TD)
                des.append(de)
                des_on.append(de_on)
                des_off.append(de_off)
            else:
                for key in ['NA', 'NB', 'NC']:
                    tmp = df.copy()
                    # tmp.dropna(axis=1, thresh=int(0.2 * tmp.shape[0]), inplace=True)
                    tmp = Rename_Data(tmp, key)
                    de, de_on, de_off = Resample_Data(
                        tmp, sn, tp, folder, TD, key)
                    des.append(de)
                    des_on.append(de_on)
                    des_off.append(de_off)

    describe = pd.concat(des)
    describe.to_csv('describe.csv')
    describe_on = pd.concat(des_on)
    describe_on.to_csv('describe_on.csv')
    describe_off = pd.concat(des_off)
    describe_off.to_csv('describe_off.csv')


def Resample_Data(df, sn, tp, folder, TD, key=''):

    df = df.groupby(df.columns, axis=1).last()
    try:
        df['DateTime'] = df['DateTime'].apply(
            lambda x: datetime.datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M:%S'))
    except:
        pass

    ref = 'R410a' if tp == '30RB' else 'R134a'
    ref = 'R22' if tp == '30GT' else ref
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.set_index(['DateTime'], inplace=True)
    df = df.sort_index()
    df = df.resample('15min').ffill(limit=1)
    df.dropna(how='all', inplace=True)

    if 'cs' not in sn:
        df = Convert_Unit(df)
    df.dropna(axis=1, how='all', inplace=True)
    df = Physics_Based_Feature(df, ref)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    for fd in folder.values():
        if not os.path.exists(fd):
            os.mkdir(fd)
    if not df.empty:
        df.to_csv(os.path.join(folder['resample'],
                  '%s_%s_%s.csv' % (sn, tp, key)))
        des = df.describe()
        des_on, des_off = pd.DataFrame(), pd.DataFrame()
        des['sn'] = sn+key
        des['CHTP'] = tp
        des['EarliestData'] = df.index.min()
        des['latestData'] = df.index.max()
        if 'PLC' in df.columns:
            on = df[df.PLC >= 30]
            if 'ALC' in on.columns:
                on = on[(on.ALC > 10) | (on.ALC != on.ALC)]
            on.dropna(axis=1, how='all', inplace=True)
            if not on.empty:
                on = Cycle_Analysis(on, ref)
                on = On_Analysis(on, tp, '%s_%s_%s' %
                                 (sn, tp, key), TD, folder)
                on.to_csv(os.path.join(
                    folder['run'], '%s_%s_%s.csv' % (sn, tp, key)))
                des['EarliestRunData'] = on.index.min()
                des['latestRunData'] = on.index.max()
                des_on = on.describe()
                des_on['sn'] = sn+key
                des_on['CHTP'] = tp
            off = df[df.PLC == 0]
            if 'ALC' in off.columns:
                off = off[off.ALC < 10]
            off.dropna(axis=1, how='all', inplace=True)
            if not off.empty:
                off = Off_Analysis(off, sn, tp, key, TD, folder)
                off.to_csv(os.path.join(
                    folder['off'], '%s_%s_%s.csv' % (sn, tp, key)))
                des['EarliestRunData'] = off.index.min()
                des['latestRunData'] = off.index.max()
                des_off = off.describe()
                des_off['sn'] = sn+key
                des_off['CHTP'] = tp

    return des, des_on, des_off


def Convert_Unit(df, fn='para_unit.csv'):

    para_unit = pd.read_csv(fn, index_col=0)
    for col in df.columns:
        if col == 'SP':
            print('col', col, para_unit)
        unit = para_unit.loc[col, 'Unit']
        if unit == 'F':
            df.loc[df[col] == 0, col] = np.nan
            df[col] = (df[col]-32)/1.8
        elif unit == 'dF':
            df.loc[df[col] == 0, col] = np.nan
            df[col] /= 1.8
        elif unit == 'psi':
            df.loc[df[col] == 0, col] = np.nan
            df[col] *= 6.894757

    return df


def Physics_Based_Feature(df, ref):

    for para in ['ALC', 'CDT', 'MTRW', 'OilP']:
        if (para + '1') in df.columns:
            if (para + '2') in df.columns:
                df[para] = df[[para+'1', para+'2']].max(axis=1)
            else:
                df[para] = df[para+'1']
        elif (para + '2') in df.columns:
            df[para] = df[para+'2']

    if ('SP' in df.columns) & ('DP' in df.columns):
        df['SST'] = HAT.Props('T', 'P', df.SP*1000+101325, 'Q', 1, ref)-273.15
        df['SDT'] = HAT.Props('T', 'P', df.DP*1000+101325, 'Q', 1, ref)-273.15

        if 'CRT' in df.columns:
            df['RDT_c'] = df['SDT'] - df['CRT']
        if 'ERT' in df.columns:
            df['RDT_e'] = df['SST'] - df['ERT']

        if 'CDT' in df.columns:
            df['DSH'] = df['CDT'] - df['SDT']
        if 'OilP' in df.columns:
            if 'OilPD' in df.columns:
                df['OilPD'][df['OilPD'] == 0] = df['OilP'] - df['SP']
            else:
                df['OilPD'] = df['OilP'] - df['SP']
        if 'ST' in df.columns:
            df['SSH'] = df['ST'] - df['SST']

        '''HX'''

        df['LTD_e'] = df['LCW'] - df['SST']
        df['DT_e'] = df['ECW'] - df['LCW']
        df['LMTD_e'] = df['DT_e'] / \
            (((df['ECW']-df['SST'])/df['LTD_e']).apply(np.log))

        if 'OAT' in df.columns:
            df['LTD_c'] = df['SDT'] - df['OAT']
            df['LMTD_c'] = df['SDT'] - df['OAT']
        elif ('ECDW' in df.columns) & ('LCDW' in df.columns):
            df['LTD_c'] = df['SDT'] - df['LCDW']
            df['DT_c'] = df['LCDW'] - df['ECDW']
            if 'PLC' in df.columns:
                df['DT_cn'] = df['DT_c']/df['PLC']*100
            df['LMTD_c'] = df['DT_c'] / \
                (((df['SDT']-df['ECDW'])/df['LTD_c']).apply(np.log))
        if 'PLC' in df.columns:
            df['DT_en'] = df['DT_e']/df['PLC']*100
            df['LTD_en'] = df['LTD_e']/df['PLC']*100
            if 'LTD_c' in df.columns:
                df['LTD_cn'] = df['LTD_c']/df['PLC']*100
            if 'EXV' in df.columns:
                df['EXV_n'] = df['EXV']/df['PLC']*100
    if 'Control Point' in df.columns:
        df['CTRL_ERR'] = df['LCW'] - df['Control Point']

    return df


def Cycle_Analysis(df, ref):

    if ('SP' in df.columns) & ('DP' in df.columns):
        df['Hsuc'] = HAT.Props('H', 'P', df.SP*1000+101325, 'Q', 1, ref)
        df['Ssuc'] = HAT.Props('S', 'P', df.SP*1000+101325, 'Q', 1, ref)
        if ('ST' in df.columns):
            df.loc[df['ST'] > df['SST'], 'Hsuc'] = HAT.Props(
                'H', 'P', df.SP[df['ST'] > df['SST']]*1000+101325,
                'T', df.ST[df['ST'] > df['SST']]+273.15, ref)
            df.loc[df['ST'] > df['SST'], 'Ssuc'] = HAT.Props(
                'S', 'P', df.SP[df['ST'] > df['SST']]*1000+101325,
                'T', df.ST[df['ST'] > df['SST']]+273.15, ref)
        df['Hdisi'] = HAT.Props('H', 'P', df.DP*1000+101325, 'S', df.Ssuc, ref)
        df['Hco'] = HAT.Props('H', 'P', df.DP*1000+101325, 'Q', 0, ref)
        if 'CDT' in df.columns:
            df['Hdis'] = HAT.Props(
                'H', 'P', df.DP*1000+101325, 'T', df.CDT+273.15, ref)
            df.loc[df.Hdis < df.Hdisi, 'Hdis'] = df['Hdisi']
            df['COP'] = (df.Hsuc-df.Hco)/(df.Hdis-df.Hsuc)
            df['eta_comp'] = (df.Hdisi-df.Hsuc)/(df.Hdis-df.Hsuc)

    return df


def Off_Analysis(df, sn, tp, key, TD, folder, fn='Threshold.csv'):

    thrs = pd.read_csv(fn, index_col=0)
    if ('LCW' in df.columns) & ('ECW' in df.columns) & ('SST' in df.columns) & ('SDT' in df.columns):
        df['leak'] = (df[['LCW', 'ECW']].min(axis=1) -
                      df[['SST', 'SDT']].max(axis=1)) > 5
        count = thrs.loc['leak', 'Count']
        paras = thrs.loc['leak', 'Plot_Paras']
        df['leak_H'] = df['leak']
        df = Alarm_Count(df, 'leak_H', 0.5, count, TD,
                         '%s_%s_%s' % (sn, tp, key), folder['off_plot'], paras)

    return df


def On_Analysis(df, tp, title, TD, folder, fn='Threshold.csv'):

    thrs = pd.read_csv(fn, index_col=0)
    for para in thrs.index:
        if para in df.columns:
            count = thrs.loc[para, 'Count']
            paras = thrs.loc[para, 'Plot_Paras']
            for lh in ['L', 'H']:
                paralh = '%s_%s' % (para, lh)
                thr = thrs.loc[para, tp+'_'+lh]
                if thr == thr:
                    if lh == 'L':
                        df[paralh] = df[para] < thr
                    else:
                        df[paralh] = df[para] > thr
                    df = Alarm_Count(df, paralh, thr, count, TD,
                                     title, folder['run_plot'], paras)
    return df


def Alarm_Count(df, col, thr, count, TD, title, folder, paras):

    df[col+'_seq'] = (df[col].diff() != 0).cumsum()
    df[col] = df[[col, col+'_seq']
                 ].groupby(col+'_seq').transform(lambda x: x.cumsum())
    if df[col].max() > count:

        # if ('Oil' in col) | ('MTRW' in col) | ('eta_comp' in col) | ('ThT' in col):
        paras = paras.split(';')
        seqs = df.loc[df[col] > count, col+'_seq'].unique()
        plt.figure(figsize=(7.5, 3*len(paras)))

        for j in ['_all_data', '_zone_in']:
            flag = 1
            for i, para in enumerate(paras):
                plt.subplot(len(paras)*100+11+i)
                plt.subplots_adjust(left=0.05,
                                    right=0.95, top=0.95, bottom=0.05)
                mx, mn = -np.inf, np.inf
                par = para.split('|')
                if len(par) == 2:
                    x = df[par[1]]
                    xt = 0
                else:
                    x = df.index
                    xt = 1
                for p in par[0].split(','):
                    if p in df.columns:
                        if xt:
                            sns.scatterplot(x, df[p], label=p)
                        else:
                            sns.scatterplot(
                                x, df[p], df.index, palette='rainbow', legend=False)
                        mx = max(mx, df[p].max())
                        mn = min(mn, df[p].min())
                if flag:
                    plt.title(title)
                    plt.axhline(thr, ls='--', c='r')
                flag = 0
                if xt:
                    if j == '_zone_in':
                        xmn, xmx = df[df[col+'_seq'] == seqs[0]].index.min(
                        ), df[df[col+'_seq'] == seqs[-1]].index.max()
                    else:
                        xmn, xmx = df.index.min(), df.index.max()

                    if isinstance(TD, pd.Series):
                        for td in TD:
                            plt.axvline(td, ls='--', c='r')
                            plt.text(td, mx+0.5, 'Tentative Date',
                                     rotation='vertical', ha='right', va='top')
                            xmn = td if td < xmn else xmn
                            xmx = td if td > xmx else xmx
                    else:
                        plt.axvline(TD, ls='--', c='r')
                        plt.text(TD, mx+0.5, 'Tentative Date',
                                 rotation='vertical', ha='right', va='top')
                        xmn = TD if TD < xmn else xmn
                        xmx = TD if TD > xmx else xmx

                    plt.xlim(xmn - 0.05*(xmx-xmn), xmx+0.05*(xmx-xmn))
                    if not (np.isinf(mx) or np.isinf(mn)):
                        for seq in seqs:
                            plt.fill_between(df[df[col+'_seq'] == seq].index,
                                             mn-0.5, mx+0.5,
                                             color='r', alpha=0.1)
            plt.savefig('%s//%s' % (folder, title+'_'+col)+j)
            plt.clf()

    return df


if __name__ == '__main__':

    sns.set_style('darkgrid')
    folder = {'data': 'North_America_chiller_retrofit',
              'resample': 'resample_15min',
              'run': 'run_data',
              'off': 'off_data',
              'off_plot': 'off_data/plot',
              'run_plot': 'run_data/plot'}
    chtp = CHTP()
    # if not os.path.exists(folder['resample']):
    Read_Data(folder, chtp)
