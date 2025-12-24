# _*_ coding: utf-8 _*_
"""
Time:     1/3/2024 10:58 AM
Author:   XuLing
"""
"""
此文件用于换机报告前的数据预处理部分，数据来自于少杰离线计算的若干csv文件，需要做的预处理步骤如下：
1.创建跟SPT类似的文件夹层级；
2.文件的列重命名，PLC转换为小数；
3.计算出月度总结和总结的csv文档
"""

import os
import sys
import shutil

import numpy as np
import pandas as pd

class ReplaceChillerData:
    def __init__(self, ChillerSN):
        self.ChillerSN = ChillerSN
        # self.raw_data_path = os.path.join("C:/01_SVN/QT_VFD_1118_vDataCollection/test data/replacement data/", self.ChillerSN + ".csv")
        self.raw_data_path = os.path.join(".", "output_final_compare_to_psm", self.ChillerSN + ".csv")
            # "C:/01_SVN/QT_VFD_1118_vDataCollection/test data/replacement data/", self.ChillerSN + ".csv")
        self.project_path = os.path.abspath(os.path.join(os.getcwd(), "."))
        self.result_path = os.path.join(self.project_path, 'result')
        self.unit_path = os.path.join(self.project_path, 'result', self.ChillerSN)
        self.analysis_path = os.path.join(self.project_path, 'result', self.ChillerSN, 'analysis')
        self.VFD_weather_path = os.path.join(self.project_path, 'result', self.ChillerSN, 'VFD_weather')
        self.predict_path = os.path.join(self.project_path, 'result', self.ChillerSN, 'predict')
        self.report_path = os.path.join(self.project_path, 'result', self.ChillerSN, 'report')
        self.data_path = os.path.join(self.analysis_path, self.ChillerSN + ".csv")

    def create_folder(self):
        """先删除文件夹，再创建基本存储路径"""
        if os.path.exists(self.unit_path):
            shutil.rmtree(self.unit_path)
        os.mkdir(self.unit_path)
        os.mkdir(self.analysis_path)
        os.mkdir(self.VFD_weather_path)
        os.mkdir(self.predict_path)
        os.mkdir(self.report_path)

    def data_preprocess(self):
        """对复制好的数据做数据预处理并保存"""
        self.data = pd.read_csv(self.raw_data_path)
        self.data.rename(columns={"COP_Current": "COP_ref", "COP": "psm_cop_current", "psm_cop": "psm_cop_compare"}, inplace=True)
        self.data["PLC%"] = self.data["PLC"]
        self.data["PLC"] = self.data["PLC"]/100
        self.data["DateTime"] = pd.to_datetime(self.data["DateTime"])
        self.data.query("Power>0", inplace=True)
        self.data["Energy Saving"] = self.data["Energy Saving"] / 100
        self.data.to_csv(self.data_path)

    def get_monthly_data(self):
        self.dt = (self.data.DateTime - self.data.DateTime.shift(1)).mode()[0] / np.timedelta64(1, 'h')
        self.data["month"] = self.data["DateTime"].dt.month
        self.data["year-month"] = self.data["Year"].astype("str") + "/" + self.data["month"].astype("str")
        monthly_summary = pd.DataFrame(columns=["Month", "Power/kWh", "Runtime/Hrs", "Avg. PLR", "Chiller running COP",
                                                "COP after VFD retrofit", "VFD retrofit saving/kWh", "VFD retrofit saving %"])

        for key, group in self.data.groupby("year-month"):
            group["Ton"] = group["Power"] * group["psm_cop_current"]
            group["Power_replace"] = group["Ton"] / group["psm_cop_compare"]
            monthly_summary.loc[key, "Month"] = key
            monthly_summary.loc[key, "Power/kWh"] = (round(group["Power"].sum() * self.dt))
            monthly_summary.loc[key, "Runtime/Hrs"] = (round(len(group.query("Power!=0")) * self.dt))
            monthly_summary.loc[key, "Avg. percent line current"] = str(round(group["PLC%"].mean())) + "%"
            monthly_summary.loc[key, "Chiller running COP"] = (round(group["Ton"].sum() / group["Power"].sum(), 1))
            monthly_summary.loc[key, "COP after VFD retrofit"] = (round(group["Ton"].sum() / group["Power_replace"].sum(), 1))
            monthly_summary.loc[key, "VFD retrofit saving/kWh"] = (round(group["Energy Saving"].sum() * self.dt))
            monthly_summary.loc[key, "VFD retrofit saving %"] = str(round(group["Energy Saving"].sum()/group["Power"].sum()*100, 1)) + "%"
            monthly_summary.loc[key, "chiller efficiency_after"] = 3.517 / monthly_summary.loc[key, "COP after VFD retrofit"]
            monthly_summary.loc[key, "chiller efficiency_before"] = 3.517 / monthly_summary.loc[key, "Chiller running COP"]
        monthly_summary["DateTime"] = pd.to_datetime(monthly_summary["Month"], format="%Y/%m")
        monthly_summary.sort_values(by="DateTime", inplace=True)
        monthly_summary.drop(columns=["DateTime"], inplace=True)
        monthly_summary.to_csv(os.path.join(self.analysis_path, 'analysis' + self.ChillerSN + "_monthly_summary.csv"), index=False)


    def get_summary_data(self):
        self.data["Ton"] = (self.data["Power"] * self.data["psm_cop_current"]) / 3.517
        self.data["Power_replace"] = self.data["Ton"] * 3.517 / self.data["psm_cop_compare"]
        self.data["ES"] = self.data["Power"] - self.data["Power_replace"]
        Power_all_before = round(self.data["Power"].sum() * self.dt)
        Power_all_after = round(self.data["Power_replace"].sum() * self.dt)
        SaveRate_all = round((Power_all_before - Power_all_after)/Power_all_before*100)
        summary = pd.DataFrame({"Serial number": [self.ChillerSN],
                   "Power/kWh": [Power_all_before],
                   "Runtime/Hrs": [round(len(self.data.query("PLC>0"))*self.dt)],
                   "VFD retrofit energy saving potential/kWh": [round(self.data["ES"].sum() * self.dt)],
                   "VFD retrofit energy saving %": [SaveRate_all],
                   "Ton/Ton": [round(self.data["Ton"].sum() * self.dt)],
                   "Power_vs/kWh": [Power_all_after]})
        summary.to_csv(os.path.join(self.analysis_path, 'analysis' + self.ChillerSN + "summary.csv"))

        
if __name__ == "__main__":
    # for ChillerSN in [
    #     "1913Q22565", "2301Q65746", "2511Q20862", "2608Q18009", "2619Q27626", "4004Q69950", "4415Q24810", "4998J59038", "5111Q21335",
    #     "5200Q64908"
    # ]:
    for ChillerSN in ["4710Q20221", "4710q20220","1399J59406","1499J59408","1501Q65384"]:
    # ["xrcs1015", "189100182", "180100017", "180100019", "xres1039", "xrcs1016", "xres1038", "xr4p1473",
    #                   "xr3p1471", "xr4p1475", "xr3p1466", "xr4p1468", "xr3p1467", "xr4h1213", "xr4h1212", "2102q67026",
    #                   "2102q67027", "2102q67025", "xr4j1047", "xr5j1480", "xr5j1481"]


        print(ChillerSN)
        ReplaceChillerData_obj = ReplaceChillerData(ChillerSN)
        ReplaceChillerData_obj.create_folder()
        ReplaceChillerData_obj.data_preprocess()
        ReplaceChillerData_obj.get_monthly_data()
        ReplaceChillerData_obj.get_summary_data()