# _*_ coding: utf-8 _*_
"""
Time:     6/8/2023 9:48 AM
Author:   XuLing
"""
import datetime
import numpy as np
import pandas as pd
import os
import time

class GetData:
    def __init__(self, chillertype, chillerSN, ton, COP, fill, tariff, invest, language):
        self.chillertype = chillertype
        self.SN = chillerSN
        self.ton = round(float(ton))
        self.COP = COP
        self.fill = fill
        self.tariff = float(tariff)
        self.Invest = round(float(invest))
        self.language = language #0英文 1中文
        self.Nominal_power = round(self.ton * 3.52/self.COP)
        self.parent_path = '.'
        self.path = self.parent_path + "/result/" + self.SN

    def get_data_path(self):
        #分析数据路径
        self.analysis_data_path = self.path + '/analysis/' + 'analysis' + self.SN + '_monthly_summary.csv'
        self.summary_analysis_data_path = self.path + '/analysis/' + 'analysis' + self.SN + 'summary.csv'
        self.data_path = self.path + '/analysis/' + self.SN + '.csv' #离心
        self.data_A_path = self.path + '/analysis/' + self.SN + '_A_Loop.csv'
        self.data_B_path = self.path + '/analysis/' + self.SN + '_B_Loop.csv'
        self.data_C_path = self.path + '/analysis/' + self.SN + '_C_Loop.csv'
        self.CPLV_result_path = self.path + "/" + "analysis" + "/" + self.SN + "_CPLV_result.csv"
        #预测数据路径
        self.predict_monthly_data_path = self.path + '/predict/' + self.fill + '/' + 'prediction' + self.SN + '_monthly_summary.csv'
        self.predict_summary_data_path = self.path + '/predict/' + self.fill + '/' + 'prediction' + self.SN + 'summary.csv'

    def get_figs_path(self):
        if self.language == 0:
            self.COP_path = self.path + '/analysis/' + self.SN + ' COP before and after retrofit.png'
            self.Efficiency_path = self.path + '/analysis/' + self.SN + 'Chiller efficiency before and after retrofit.png'
            self.Efficiency_Replace_path = self.path + '/analysis/' + self.SN + 'Chiller efficiency before and after replace.png'
        elif self.language == 1:
            self.COP_path = self.path + '/analysis/' + self.SN + '变频改造前后COP.png'
        self.PLC_path = self.path + '/analysis/' + self.SN + '冷机电流百分比.png' #若螺杆只有Aloop的数据，则读取这个路径的图片
        self.PLC_A_path = self.path + '/analysis/' + self.SN + '冷机负荷百分比_A_loop.png'
        self.PLC_B_path = self.path + '/analysis/' + self.SN + '冷机负荷百分比_B_loop.png'
        self.PLC_runtime_path = self.path + '/analysis/' + self.SN + 'PLC_RunTime.png'
        self.leak_index_path = self.path + "/analysis/" + self.SN + "制冷剂充注量指数.png"
        self.COP_PLC_path = self.path + '/analysis/' + self.SN + 'COP_PLC.png'
        self.Effi_PLC_path = self.path + '/analysis/' + self.SN + 'Efficiency_PLC.png'
        self.COP_PLC_Replace_path = self.path + '/analysis/' + self.SN + 'COP_PLC_replace.png'
        self.Effi_PLC_Replace_path = self.path + '/analysis/' + self.SN + 'Efficiency_PLC_replace.png'
        self.E_ES_EP_path = self.path + '/analysis/' + self.SN + 'E_ES_EP.png' #Power&EnergySaving&EnergySavingPercent
        self.Replace_E_ES_EP_path = self.path + '/analysis/' + self.SN + 'Replace_E_ES_EP.png' #Power&EnergySaving&EnergySavingPercent for chiller replacement
        # self.FCOP_T_fig_path = self.path + '/report/' + self.SN + 'COP_tp.png'
        self.F_E_ES_EP_path = self.path + '/analysis/' + self.SN + 'F_E_ES_EP.png'#Predict Power&EnergySaving&EnergySavingPercent在本文中执行
        self.cond_app_path = self.path + "/analysis/" + self.SN + "冷凝器趋近温度℃.png"
        self.evap_app_path = self.path + "/analysis/" + self.SN + "蒸发器趋近温度℃.png"
        self.cond_effi_path = self.path + "/analysis/" + self.SN + "冷凝器效率.png"
        self.evap_effi_path = self.path + "/analysis/" + self.SN + "蒸发器效率.png"
        self.cond_app_A_path = self.path + "/analysis/" + self.SN + "冷凝器趋近温度℃_A_loop.png"
        self.cond_app_B_path = self.path + "/analysis/" + self.SN + "冷凝器趋近温度℃_B_loop.png"
        self.evap_app_A_path = self.path + "/analysis/" + self.SN + "蒸发器趋近温度℃_A_loop.png"
        self.evap_app_B_path = self.path + "/analysis/" + self.SN + "蒸发器趋近温度℃_B_loop.png"
        self.cond_effi_A_path = self.path + "/analysis/" + self.SN + "冷凝器效率_A_loop.png"
        self.cond_effi_B_path = self.path + "/analysis/" + self.SN + "冷凝器效率_B_loop.png"
        self.evap_effi_A_path = self.path + "/analysis/" + self.SN + "蒸发器效率_A_loop.png"
        self.evap_effi_B_path = self.path + "/analysis/" + self.SN + "蒸发器效率_B_loop.png"
        self.EXV_A_path = self.path + "/analysis/" + self.SN + "EXV开度_A_loop.png"
        self.EXV_B_path = self.path + "/analysis/" + self.SN + "EXV开度_B_loop.png"
        self.DSH_path = self.path + "/analysis/" + self.SN + "压缩机排气过热度.png"
        self.LCW_path = self.path + "/analysis/" + self.SN + "LCW.png"
        self.ECW_path = self.path + "/analysis/" + self.SN + "ECW.png"
        self.ECDW_path = self.path + "/analysis/" + self.SN + "ECDW.png"
        self.LCDW_path = self.path + "/analysis/" + self.SN + "LCDW.png"
        self.PowerPLC_path = self.path + "/analysis/" + self.SN + "PowerPLC.png"
        self.COPPLC_path = self.path + "/analysis/" + self.SN + "COPPLC.png"
        self.COPPLCRunhrs_path = self.path + "/analysis/" + self.SN + "COPPLCRunhrs.png"
        self.EffiPLCRunhrs_path = self.path + "/analysis/" + self.SN + "EfficiencyPLCRunhrs.png"
        self.SaveRate_path = self.path + "/analysis/" + self.SN + "VFD retrofit saving potential.png"
        self.SaveRate_Replace_path = self.path + "/analysis/" + self.SN + "Chiller replace saving potential.png"
        self.effi_PLC_ECDW_path = self.path + "/analysis/" + self.SN + "effi_PLC_ECDW.png"
        self.COP_PLC_ECDW_path = self.path + "/analysis/" + self.SN + "COP_PLC_ECDW.png"
        self.effi_PLC_ECDW1_path = self.path + "/analysis/" + self.SN + "effi_PLC_ECDW1.png"
        self.COP_PLC_ECDW1_path = self.path + "/analysis/" + self.SN + "COP_PLC_ECDW1.png"
        self.fault_count_path = self.path + "/analysis/" + self.SN + "fault_count.png"
        self.LCW_STPT_path = self.path + "/analysis/" + self.SN + "LCW_STPT.png"
        self.box_performance_RLA_path = self.path + "/analysis/" + self.SN + "box_performance_RLA.png"
        self.box_performance_Ton_path = self.path + "/analysis/" + self.SN + "box_performance_Ton.png"
        self.year_month_avg_T_Ton_path = self.path + "/analysis/" + self.SN + "year_month_avg_T_Ton.png"
        self.year_month_avg_effi_energy_path = self.path + "/analysis/" + self.SN + "year_month_avg_effi_energy.png"
        self.year_month_avg_Ton_power_path = self.path + "/analysis/" + self.SN + "year_month_avg_Ton_power.png"


    def get_word_path(self, temeplate_name, report_name):
        self.docx_path = self.parent_path + "/word_template/" + temeplate_name + ".docx"
        self.report_path = self.path + "/report"
        self.report_name = self.SN + "_" + report_name + "_" + "report.docx"
        self.save_path = os.path.join(self.report_path, self.report_name)

    def get_ppt_path(self, template_name, report_name):
        self.ppt_template_path = self.parent_path + "/ppt_template/" + template_name + ".pptx"
        self.report_path = self.path + '/report/'
        self.report_name = self.SN + report_name + "_report.pptx"

    def set_path(self, path):
        self.parent_path = path
        self.path = self.parent_path + "/result/" + self.SN

    def get_language(self): #dict的key为一个list，第一个元素为中文，第二个元素为英文
        language_dict = {"M": ["Month", "月份"],
                         "T": ["Runtime/Hrs", "运行时间/Hrs"],
                         "T_A": ["Runtime/Hrs_A_loop", "运行时间/Hrs_A_loop"],
                         "T_B": ["Runtime/Hrs_B_loop", "运行时间/Hrs_B_loop"],
                         "P": ["Avg. percent line current", "平均电流百分比"],
                         "P_A": ["Avg. percent line current_A_loop", "平均负荷百分比_A_loop"],
                         "P_B": ["Avg. percent line current_B_loop", "平均负荷百分比_B_loop"],
                         "E": ["Power/kWh", "运行能耗/kWh"],
                         "DT_e": ["deltaT_evap/℃", "冷冻水温差/℃"],
                         "DT_c": ["deltaT_cond/℃", "冷却水温差/℃"],
                         "APP_e": ["app_evap/℃", "蒸发器趋近温度/℃"],
                         "APP_c": ["app_cond/℃", "冷凝器趋近温度/℃"],
                         "ES_e": ["ES_evap/kWh", "蒸发器节能空间/kWh"],
                         "ES_c": ["ES_cond/kWh", "冷凝器节能空间/kWh"],
                         "ES_c%": ["ES_cond%", "冷凝器节能空间%"],
                         "ES_e%": ["ES_evap%", "蒸发器节能空间%"],
                         "COP_before": ["Chiller running COP", '实际运行COP'],
                         "COP_after": ["COP after VFD retrofit", '变频改造后COP'],
                         "S_monthly": ["VFD retrofit saving/kWh", '变频节能空间/kWh'],
                         "S_monthly%": ["VFD retrofit saving %", '变频节能百分比'],
                         "S": ["VFD retrofit energy saving potential/kWh", "节能空间/kWh"],
                         "S%": ["VFD retrofit energy saving %", "节能百分比"],
                         "Leak": ["leakage_index", "制冷剂泄漏指数"],
                         "APP_e_A": ["app_evap/℃_A_loop", "蒸发器趋近温度/℃_A_loop"],
                         "APP_e_B": ["app_evap/℃_B_loop", "蒸发器趋近温度/℃_B_loop"],
                         "APP_c_A": ["app_cond/℃_A_loop", "冷凝器趋近温度/℃_A_loop"],
                         "APP_c_B": ["app_cond/℃_B_loop", "冷凝器趋近温度/℃_B_loop"],
                         "Leak_A": ["leakage_index_A_loop", "制冷剂泄漏指数_A_loop"],
                         "Leak_B": ["leakage_index_B_loop", "制冷剂泄漏指数_B_loop"],
                         "Ton": ["Ton/Ton", "制冷量/Ton"],
                         "Power_vs": ["Power_vs/kWh", "变频优化后运行能耗/kWh"],
                         "FR": ["Prediction reliability", "预测可信度"],
                         "FA.LCW": ["Avg. LCW/℃", "平均冷冻水温/℃"],
                         "FA.ECDW": ["Avg. ECDW/℃", "平均冷却水温/℃"],
                         "FA.OAT": ["Avg. OAT/℃", "平均干球温度/℃"],
                         "FA.OAWT": ["Avg. OAWT/℃", "平均湿球温度/℃"],
                         "FS_monthly%": ["VFD retrofit saving %", "变频节能百分比"],
                         "FS_monthly": ["VFD retrofit saving/kWh", "变频节能空间/kWh"],
                         "FE_monthly": ["Power/kWh", "运行能耗/kWh"],
                         "FP_monthly": ["Avg. PLR", "平均负荷百分比"],
                         "F_COP_before": ["Chiller running COP", "实际运行COP"],
                         "F_COP_after": ["COP after VFD retrofit", "变频改造后COP"],
                         "FA.P": ["Avg. PLR", "平均负荷百分比"],
                         "FE": ["Predicted annual energy consumption/kWh", "预测全年运行能耗/kWh"],
                         "FS": ["Predicted annual energy saving potential/kWh", "预测年节能量/kWh"],
                         "FS%": ["Predicted annual saving %", "预测年节能率%"],
                         "COP_B_A": ["COP before and after retrofit", "变频改造前后COP"],
                         "COP_B": ["Fix speed COP", "实际运行COP"],
                         "COP_A": ["Variable speed COP", "对比机组COP"],
                         "Time": ["Time", "时间"]

                       }

        language_df = pd.DataFrame.from_dict(language_dict)
        self.lan = language_df.loc[self.language]
        return self.lan

    def get_CPLV_result(self):
        df_CPLV_result = pd.read_csv(self.CPLV_result_path)
        CPLV_all_run_hours = df_CPLV_result["Runtime"].sum()/2  # 计算总共运行时间
        df_CPLV_result["Weighting factor"] = round(df_CPLV_result["Runtime"] / CPLV_all_run_hours, 2)  # 计算各PLR下运行时间占总运行时间比例
        df_CPLV_result["PLR"] = df_CPLV_result["PLR"].apply(lambda x: format(x, '.0%'))  # PLR取整并增加%
        df_CPLV_result["runtime"] = df_CPLV_result["Runtime"].apply(lambda x: '%.0f' % x)  # 运行小时取整
        df_CPLV_input = df_CPLV_result[["PLR", "ECWT", "LCHW", "Weighting factor", "Runtime"]]  # input需要的列名
        df_CPLV_input = df_CPLV_input.drop(df_CPLV_input.index[len(df_CPLV_input) - 1], axis=0)  # 删除input表格不需要用到的最后一行
        df_CPLV_input['ECWT'] = df_CPLV_input['ECWT'].astype('int')
        df_CPLV_input["LCHW"] = df_CPLV_input['LCHW'].astype('int')
        df_CPLV_input["Runtime"] = df_CPLV_input['Runtime'].astype('int')
        df_CPLV_result["Num"] = list(range(1, len(df_CPLV_result))) + ["Total"]  # output需要用到的num列
        df_CPLV_output = df_CPLV_result[
            ["Num", "PLR", "fs_cop", "vs_cop", 'fs_KW/Ton', 'vs_KW/Ton', 'power_fs', 'power_vs', 'ES%']]  # output需要的列名
        df_CPLV_output["power_fs"] = df_CPLV_output['power_fs'].astype('int')
        df_CPLV_output["power_vs"] = df_CPLV_output['power_vs'].astype('int')
        self.kW_Ton_fs = format(df_CPLV_result["fs_KW/Ton"].values[-1], "")
        self.kW_Ton_vs = format(df_CPLV_result["vs_KW/Ton"].values[-1], "")
        self.kW_Ton = round((float(self.kW_Ton_fs) - float(self.kW_Ton_vs)) / float(self.kW_Ton_fs) * 100)
        self.power_fs = format(df_CPLV_result["power_fs"].values[-1], "")
        self.power_vs = format(df_CPLV_result["power_vs"].values[-1], "")
        self.runhrs = format(round(df_CPLV_result["Runtime"].values[-1]), "")
        self.invest = format(round(self.Invest/1000), ',')
        self.FSavePower = df_CPLV_result["power_fs"].values[-1] - df_CPLV_result["power_vs"].values[-1]
        self.Fsavepower = format(round(self.FSavePower/1000), ",")
        self.FSaveMoney = round(self.FSavePower * self.tariff)
        self.Fsavemoney = format(round(self.FSaveMoney/1000), ",")
        self.FSaveCOO = round(self.FSavePower * 0.272)
        self.FsaveCOO = format(round(self.FSaveCOO/1000), ",")
        return df_CPLV_input, df_CPLV_output

    def get_VFD_analysis_data(self):
        monthly_data_df = pd.read_csv(self.analysis_data_path)
        summary_data_df = pd.read_csv(self.summary_analysis_data_path)
        if os.access(self.data_path, os.F_OK):  #离心
            self.runhrs = format(round(summary_data_df[self.lan["T"]].values[0]), ',')
            self.Type = "离心"
        elif not os.access(self.data_B_path, os.F_OK): #单回路螺杆
            self.runhrs_A = format(summary_data_df[self.lan["T_A"]].values[0], ',')
            self.runhrs_B = "-"
            self.runhrs = self.runhrs_A
            self.Type = "螺杆"
        else: #多回路螺杆
            self.runhrs_A = format(summary_data_df[self.lan["T_A"]].values[0], ',')
            self.runhrs_B = format(summary_data_df[self.lan["T_B"]].values[0], ',')
            self.runhrs = self.get_Total_COP()
            self.Type = "螺杆"
        self.months = len(monthly_data_df)
        self.draw_analysis = monthly_data_df.copy()
        self.draw_analysis = self.draw_analysis.fillna(0)
        for col in [self.lan["P"], self.lan["P_A"], self.lan["P_B"], self.lan["S_monthly%"]]:
            try:
                self.draw_analysis[col] = list(monthly_data_df[col].str.strip("%").astype(float).values / 100)
            except:
                continue
        self.Power = format(summary_data_df[self.lan["E"]].values[0], ',')
        save_power = summary_data_df[self.lan["S"]].values[0]
        self.save_power = float(save_power) #float
        self.SavePower = format(save_power, ',') #string
        self.SaveRate = summary_data_df[self.lan["S%"]].values[0]
        save_money = self.tariff * float(save_power)
        self.SaveMoney = format(int(save_money), ',')
        self.SaveCOO = 0.272 * float(save_power)
        self.saveCOO = format(round(self.SaveCOO), ',')
        self.Ton = float(summary_data_df[self.lan["Ton"]].values[0])
        self.kW_Ton_fs = format(round(float(summary_data_df[self.lan["E"]].values[0]) / float(summary_data_df[self.lan["Ton"]].values[0]), 2), ',')
        self.kW_Ton_vs = format(round(float(summary_data_df[self.lan["Power_vs"]].values[0])/float(summary_data_df[self.lan["Ton"]].values[0]), 2), ',')
        self.kW_Ton = round((float(self.kW_Ton_fs) - float(self.kW_Ton_vs)) / float(self.kW_Ton_fs) * 100)
        self.analysis_data = monthly_data_df
        self.summary_data = summary_data_df


    def get_VFD_predict_data(self):
        predict_monthly_data_df = pd.read_csv(self.predict_monthly_data_path)
        predict_monthly_data_df[self.lan["M"]].astype('str')
        self.predict_reliability = (predict_monthly_data_df[self.lan["FR"]] == 'low').sum()
        self.draw_predict = predict_monthly_data_df.copy()
        for col in [self.lan["FP_monthly"], self.lan["FS_monthly%"]]:
            try:
                self.draw_predict[col] = list(predict_monthly_data_df[col].str.strip(' %').astype(float).values / 100)
            except:
                continue
        self.draw_predict.rename(columns={self.lan["FS_monthly"]: '预测变频节能空间/kWh',
                                          self.lan["FS_monthly%"]: '预测变频节能百分比'}, inplace=True)
        predict_summary_data_df = pd.read_csv(self.predict_summary_data_path)
        self.FPower = predict_summary_data_df[self.lan["FE"]].values[0]
        self.Fpower = format(self.FPower, ',')
        self.FSavePower = predict_summary_data_df[self.lan["FS"]].values[0] #大写的变量输出int,小写的变量输出string
        self.FSaveRate = predict_summary_data_df[self.lan["FS%"]].values[0] #预测一年节省能源百分比
        self.FSaveMoney = round(self.tariff * float(self.FSavePower))
        self.Fsavemoney = format(round(self.FSaveMoney), ',')
        self.FSaveCOO = int(0.272 * float(self.FSavePower))
        self.FsaveCOO = format(round(self.FSaveCOO), ',')
        self.Fsavepower = format(round(self.FSavePower), ',')
        self.invest = format(round(self.Invest), ',')
        if self.FSaveMoney == 0:
            self.Payback_year = 0
        else:
            self.Payback_year = round(self.Invest/self.FSaveMoney, 1)
        self.predict_data = predict_monthly_data_df
        return predict_monthly_data_df

    def get_Total_COP(self):
        if os.access(self.data_B_path, os.F_OK): #拥有ABloop数据的螺杆机
            self.data_A = pd.read_csv(self.data_A_path)
            self.data_A["Q_current"] = self.data_A["psm_cop_current"] * self.data_A["power_fs"]
            self.data_A["Q_compare"] = self.data_A["psm_cop_compare"] * self.data_A["power_vs"]
            self.data_B = pd.read_csv(self.data_B_path)
            self.data_B["Q_current"] = self.data_B["psm_cop_current"] * self.data_B["power_fs"]
            self.data_B["Q_compare"] = self.data_B["psm_cop_compare"] * self.data_B["power_vs"]
            self.data_merge = pd.merge(self.data_A, self.data_B, on='DateTime', how="outer", suffixes=("_left", "_right"))
            self.data_merge.replace(np.nan, 0, inplace=True)
            self.data_merge = self.data_merge[['DateTime', "Q_compare_left", "Q_compare_right", "Q_current_left", "Q_current_right",
                                     "power_vs_left", "power_fs_left", "power_vs_right", "power_fs_right", "Power_left", "Power_right"]]
            self.data_merge['DateTime'] = pd.to_datetime(self.data_merge['DateTime'])
            dt = (self.data_merge.DateTime - self.data_merge.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
            Runhrs = len(self.data_merge.query("Power_left!=0 or Power_right!=0")) * dt
            self.data_merge["COP_all_compare"] = (self.data_merge["Q_compare_left"] + self.data_merge["Q_compare_right"])/(self.data_merge["power_vs_left"] + self.data_merge["power_vs_right"])
            self.data_merge["COP_all_current"] = (self.data_merge["Q_current_left"] + self.data_merge["Q_current_right"])/(self.data_merge["power_fs_left"] + self.data_merge["power_fs_right"])
        elif os.access(self.data_path, os.F_OK): #离心机
            self.data = pd.read_csv(self.data_path)
            self.data_merge = self.data
            self.data_merge['DateTime'] = pd.to_datetime(self.data_merge['DateTime'])
            dt = (self.data_merge.DateTime - self.data_merge.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
            Runhrs = len(self.data_merge.query("Power!=0")) * dt
            if "Hrs" in self.data_merge.columns:
                self.Max_Runhr = round(self.data_merge["Hrs"].max())
                self.Max_Runhr_str = format(self.Max_Runhr, ',')

            else:
                self.Max_Runhr_str = "Not available in telemetry"
            self.data_merge["COP_all_compare"] = self.data_merge["psm_cop_compare"]
            self.data_merge["COP_all_current"] = self.data_merge["psm_cop_current"]
            self.data_merge["Efficiency_all_compare"] = round(3.517/self.data_merge["COP_all_compare"], 2)
            self.data_merge["Efficiency_all_current"] = round(3.517/self.data_merge["COP_all_current"], 2)
        else: #只拥有Aloop的螺杆机
            self.data_A = pd.read_csv(self.data_A_path)
            self.data_merge = self.data_A
            self.data_merge['DateTime'] = pd.to_datetime(self.data_merge['DateTime'])
            dt = (self.data_merge.DateTime - self.data_merge.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
            Runhrs = len(self.data_merge.query("Power!=0")) * dt
            self.data_merge["COP_all_compare"] = self.data_merge["psm_cop_compare"]
            self.data_merge["COP_all_current"] = self.data_merge["psm_cop_current"]
        return Runhrs

    def get_cover_date(self):
        self.now_date = datetime.datetime.now().strftime("%Y-%m")

    def get_dis_PLC_df(self):
        """用于VFD改造英文版离心word报告中，所需提供的不同PLC的min/max/avg图, 此函数为以上图提供数据"""
        data = pd.read_csv(self.data_path, usecols=["DateTime", "LCW", "LCDW", "ECW", "ECDW", "PLC", "Power", "COP_ref"])
        self.StartDate = pd.to_datetime(data["DateTime"].min()).date()
        self.EndDate = pd.to_datetime(data["DateTime"].max()).date()
        self.StartDate_str = datetime.datetime.strftime(pd.to_datetime(data["DateTime"].min()).date(), "%d-%b-%Y")
        self.EndDate_str = datetime.datetime.strftime(pd.to_datetime(data["DateTime"].max()).date(), "%d-%b-%Y")
        self.duringDate = (self.EndDate - self.StartDate).days  #计算从报告开始时间至结束时间之间一共有多少天
        self.save_power_peryear = round(self.save_power / self.duringDate * 365)
        self.save_power_peryear_str = format(self.save_power_peryear, ",")
        self.lowloadsRate = format(len(data.query("PLC<0.6")) / len(data), '.0%')
        data["DateTime"] = pd.to_datetime(data["DateTime"])
        dt = (data.DateTime - data.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
        data["cut_PLC"] = pd.cut(data['PLC'], bins=[0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.2],
                                 labels=["<30", "30-40", "40-50",  "50-60", "60-70", "70-80", "80-90", ">90"])
        data.dropna(subset=["cut_PLC"], inplace=True)
        dis_PLC_df = data.groupby("cut_PLC").agg({"LCW": ["min", "max", "mean"], "ECW": ["min", "max", "mean"],
                                              "LCDW": ["min", "max", "mean"], "ECDW": ["min", "max", "mean"],
                                              "Power": ["min", "max", "mean"], "COP_ref": ["min", "max", "mean"]})
        # dis_PLC_df.dropna(how="all", axis=0, inplace=True)

        def cal_Runhrs(group):
            if not group.empty:
                Runhrs = len(group.query("Power!=0")) * dt
                return Runhrs
            else:
                return 0
        dis_PLC_df["Runhrs"] = data.groupby("cut_PLC").apply(cal_Runhrs)
        dis_PLC_df["RunhrsRate"] = round((dis_PLC_df["Runhrs"]/dis_PLC_df["Runhrs"].sum()), 2)
        dis_PLC_df["efficiency_mean"] = 3.517/dis_PLC_df["COP_ref"]["mean"]
        self.dis_PLC_df = dis_PLC_df.round(1)
        self.dis_PLC_df["PLC_label"] = self.dis_PLC_df.index
        self.dis_PLC_df.reset_index(inplace=True)
        self.dis_PLC_df.columns = ["_".join(x) for x in self.dis_PLC_df.columns.ravel()]
        self.dis_PLC_df.rename(columns=dict(zip([x for x in self.dis_PLC_df.columns if x[-1] == "_"], [x[0:-1] for x in self.dis_PLC_df.columns if x[-1] == "_"])), inplace=True)

    def get_dis_Ton_df(self, DesignRT):
        self.data["Ton"] = self.data["COP_ref"] * self.data["Power"] / 3.517
        data_Ton90 = self.data.query(f"Ton>{DesignRT * 0.9}")
        self.Ton90_COP = round(data_Ton90["COP_ref"].mean(), 1)
        self.Ton90_effi = round(3.517/self.Ton90_COP, 2)
        if DesignRT == "-":
            Ton_bins = list(range(0, int(self.data["Ton"].max())+50, 50))
        else:
            Ton_bins = list(range(0, int(DesignRT)+50, 50))

        self.data["cut_Ton"] = pd.cut(self.data['Ton'], bins=Ton_bins,
                                    labels=["%s-%s"%(value, Ton_bins[index+1]) for index, value in enumerate(Ton_bins) if index<len(Ton_bins)-1])
        self.data["DateTime"] = pd.to_datetime(self.data["DateTime"])
        dt = (self.data.DateTime - self.data.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
        def cal_Runhrs(group):
            if not group.empty:
                Runhrs = len(group.query("Power!=0")) * dt
                return Runhrs
            else:
                return 0

        self.data.dropna(subset=["cut_Ton"], inplace=True)
        self.dis_Ton_df = self.data.groupby("cut_Ton").agg({
                                                "Efficiency_all_current": ["min", "max", "mean"],
                                                "COP_ref": ["min", "max", "mean"]
                                                })
        # self.dis_Ton_df.dropna(how="all", axis=0, inplace=True)
        self.dis_Ton_df.replace(np.nan, 0, inplace=True)
        self.dis_Ton_df["Runhrs"] = self.data.groupby("cut_Ton").apply(cal_Runhrs)
        self.dis_Ton_df["RunhrsRate"] = round((self.dis_Ton_df["Runhrs"] / self.dis_Ton_df["Runhrs"].sum()), 2)
        self.maxium_running_time_Ton_range = self.dis_Ton_df[['Runhrs']].idxmax().values[0]
        self.maxium_running_time_effi = round(self.dis_Ton_df.loc[self.maxium_running_time_Ton_range, ("Efficiency_all_current", "mean")], 2)
        self.maxium_running_time_COP = round(self.dis_Ton_df.loc[self.maxium_running_time_Ton_range, ("COP_ref", "mean")], 1)
        self.dis_Ton_df["Ton_label"] = self.dis_Ton_df.index
        self.dis_Ton_df.reset_index(inplace=True)
        self.dis_Ton_df.columns = ["_".join(x) for x in self.dis_Ton_df.columns.ravel()]
        self.dis_Ton_df.rename(columns=dict(zip([x for x in self.dis_Ton_df.columns if x[-1] == "_"], [x[0:-1] for x in self.dis_Ton_df.columns if x[-1] == "_"])), inplace=True)
        self.MostRunhrsOFTon = round(100 * self.dis_Ton_df["RunhrsRate"].max())

    def get_alarm_analysis(self):
        """用于replacement报告，获取对应时间的alarm list"""
        alarm_csv_path = os.path.join(r"C:\02_SVN\16_alarm_records_download_analysis\description_alarm_csv", self.SN + ".csv")
        if os.access(alarm_csv_path, os.F_OK):
            df_alarm = pd.read_csv(alarm_csv_path)
            # 按照时间来筛选，alarm的eventdatetime列时间是一个区间，代码认为是一个时区，所以需要去除时区的信息
            df_alarm["datetime"] = pd.to_datetime(df_alarm["eventdatetime"]).apply(lambda x: x.replace(tzinfo=None))
            df_alarm = df_alarm[df_alarm["datetime"] > datetime.datetime.strptime(self.StartDate_str, "%d-%b-%Y")]
            df_alarm = df_alarm[df_alarm["datetime"] < datetime.datetime.strptime(self.EndDate_str, "%d-%b-%Y")]
            self.alarm_data = df_alarm["description"].value_counts()
            self.total_alarms = len(df_alarm)
            last_2month_str = datetime.datetime.now() + datetime.timedelta(days=-30 * 2)
            df_alarm_2months = df_alarm[df_alarm["datetime"] < last_2month_str]
            df_alarm_2months_valuecount = df_alarm_2months["description"].value_counts()
            self.df_alarm_2months_valuecount15 = len(df_alarm_2months_valuecount[df_alarm_2months_valuecount.gt(15)])
        else:
            print("alarm 数据未下载")
            self.alarm_data = pd.DataFrame()
            self.total_alarms = 0
            self.df_alarm_2months_valuecount15 = 0

    def get_maximun_data_ECDW(self):
        """获取data数量最多的ECDW的区间，以5为bin"""
        self.data["year"] = self.data.DateTime.dt.year
        self.data["ECDW_F"] = 1.8 * self.data["ECDW"] + 32
        # 先画英制
        # 先找出ECDW哪个区间点最多
        bins = list(range(0, 100, 5))
        s_F = pd.cut(self.data['ECDW_F'], bins).value_counts()
        s_C = pd.cut(self.data['ECDW'], bins).value_counts()
        self.maxium_data_ECDW_F = s_F.index[0]
        self.maxium_2nd_data_ECDW_F = s_F.index[1]
        self.maxium_data_ECDW_C = s_C.index[0]
        self.maxium_2nd_data_ECDW_C = s_C.index[1]

    def get_specific_bin_ECDW_data(self):
        data = self.data[self.data["ECDW"] < self.maxium_data_ECDW_C.right]
        data = data[data["ECDW"] > self.maxium_data_ECDW_C.left]
        self.maxium_data_mean_ECDW_C = np.average([self.maxium_data_ECDW_C.left, self.maxium_data_ECDW_C.right])
        self.maxium_data_mean_ECDW_F = round(self.maxium_data_mean_ECDW_C * 1.8 + 32, 1)
        self.maxium_data_mean_LCW_C = data["LCW"].mean()
        self.maxium_data_mean_LCW_F = round(data["LCW"].mean() * 1.8 + 32, 1)
        self.maxium_data_COP = round(3.517*data["Ton"].sum()/data["Power"].sum())
        self.maxium_data_efficiency = round(3.517 / self.maxium_data_COP, 2)

    def get_load_bool(self):
        if len(self.data.query("PLC>0.97")) / len(self.data) > 0.8:# chiller是否长期在高负荷下运行，超过97%的负荷下运行了超过80%时间？
            self.full_load_80 = "Yes"
        else:
            self.full_load_80 = "No"

        if (len(self.data.query("PLC<0.6")) / len(self.data) > 0.8):#chiller 是否长期在低负荷下运行，低于60%负荷超过80%时间？
            self.low_load_80 = "Yes"
        else:
            self.low_load_80 = "No"

    def get_specific_year_data(self, years): #for chiller replacement report
        self.years = years
        self.year_data = {}  # 获取每年的月平均数据
        for year in years:
            data_year = self.data[self.data["year"] == year]
            if data_year.empty:
                continue
            data_year["month"] = data_year.DateTime.dt.month
            dt = (data_year.DateTime - data_year.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
            data_year["LCW_F"] = data_year["LCW"] * 1.8 + 32
            df = pd.DataFrame(index=list(range(1, 13)))
            month_data_avg = data_year.groupby("month")["LCW", "LCW_F", "Power", "Efficiency_all_current", "COP_ref", "Ton", "ECDW", "ECDW_F"].agg("mean")
            month_data_avg["Energy/kWh"] = data_year.groupby("month")["Power"].agg("sum")
            month_data_avg["Energy/kWh"] = month_data_avg["Energy/kWh"] * dt
            month_data_avg = month_data_avg.round({"LCW": 1, "LCW_F": 1, "Power": 0, "Efficiency_all_current": 2, "COP_ref":1, "Ton": 0, "ECDW": 1, "ECDW_F": 1, "Energy/kWh": 0})
            month_data_avg["Energy/kWh_str"] = month_data_avg["Energy/kWh"].apply(lambda x: format(round(x), ','))
            # for col in ["LCW_F", "Power", "Ton", "ECDW_F", "Energy/kWh"]: #解决了round函数的一个bug：当decimal=0时，返回的是一个float，即。0
            #     month_data_avg[col] = month_data_avg[col].astype(int)
            month_data_avg_merge = pd.merge(df, month_data_avg, left_index=True, right_index=True, how="outer")
            month_data_avg_merge.replace(np.nan, "-", inplace=True)
            # for col in ["LCW_F", "Power", "Ton", "ECDW_F", "Energy/kWh"]: #解决了round函数的一个bug：当decimal=0时，返回的是一个float，即。0
            #     month_data_avg_merge[col] = month_data_avg_merge[col].astype(int)
            self.year_data[year] = month_data_avg_merge

    def get_VFD_bool(self):#用于判断是否安装了变频器
        if "VFD" in self.data.columns:
            if self.data["VFD"].median() > 30:
                self.VFD_install = "Yes"
            else:
                self.VFD_install = "No"
        else:
            self.VFD_install = "VFD not in data"

    def get_effi_case(self, design_lcw, design_ecdw):
        """
        设计温度上下偏差0.45F/0.25°C,PLC>0.9; 设计温度上下偏差5°C，PLC>0.8
        温度每偏差1F, effi修正2%，即每偏差1°C，effi偏差3.6%
        Parameters
        ----------
        design_lcw: 设计lcw
        design_ecdw：设计ecdw

        Returns
        ------- 关于case1~3的描述见word模板
        """
        deviation_Temp1 = 0.25
        deviation_PLC1 = 0.9
        deviation_Temp2 = 5
        deviation_PLC2 = 0.8
        if (design_lcw != "") & (design_ecdw != ""):
            design_ecdw = float(design_ecdw)
            design_lcw = float(design_lcw)
            data = pd.read_csv(self.data_path)
            data90 = data.query(f"PLC > {deviation_PLC1} & ({design_lcw}-{deviation_Temp1} < LCW < {design_lcw}+{deviation_Temp1}) & ({design_ecdw}-{deviation_Temp1} < ECDW < {design_ecdw} + {deviation_Temp1})")
            if len(data90) > 50:
                effi = round(3.517/data90["COP_ref"].mean(), 2)
                return "case1", effi, len(data90)
            else:
                data80 = data.query(f"PLC > {deviation_PLC2} & ({design_lcw}-{deviation_Temp2} < LCW < {design_lcw}+{deviation_Temp2}) & ({design_ecdw}-{deviation_Temp2} < ECDW < {design_ecdw} + {deviation_Temp2})")
                if len(data80) > 50:
                    COP80_mean = data80["COP_ref"] * (pow(1.036, data80["ECDW"] - design_ecdw)) / (pow(1.036, data80["LCW"] - design_lcw))
                    deviation_COP = COP80_mean.mean()
                    deviation_effi = round(3.517/deviation_COP, 2)
                    return "case2", deviation_effi, len(data80)
                else:
                    return "case3", None, None
        else:
            return "case3", None, None


if __name__ == "__main__":
    chillertype = '30HXC'
    chillerSN = 'M2017013698'
    fill = "no_fill"
    tariff = float(1)
    invest = float(400000)


    GetData_obj = GetData(chillertype, chillerSN, fill, tariff, invest)
    GetData_obj.set_path('..')
    GetData_obj.get_data_path()
    GetData_obj.get_ppt_path()
    # GetData_obj.get_CPLV_result()
    GetData_obj.get_csv_analysis_result()
    GetData_obj.get_csv_predict_data()
    GetData_obj.get_Total_COP()