# _*_ coding: utf-8 _*_
"""
Time:     1/3/2024 2:23 PM
Author:   XuLing
"""
"""此文件用于chiller replacement 的英文word报告"""
import os
import datetime
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

pd.Timestamp
pd.plotting.register_matplotlib_converters()
import matplotlib

# plot 全局设定
# matplotlib.use("Agg")
# matplotlib.rcParams["font.size"] = 14
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from Report.GetData import GetData
from Report.ModifyDocx import ModifyDocx
from Report.DrawFigs import DrawFigs


class ModifyDocx_VFD(ModifyDocx):
    def __init__(self, GetData, connect_date, projectname):
        super().__init__(GetData)
        self.connect_date = connect_date
        self.ProjectName = projectname


class OutputReport:
    def __init__(self, GetData, DrawFigs, ModifyDocx, locationname, customername, locationcity, postalcode, siteaddress, timezone, modelnumber,
                 year, IPLV_efficiency, design_efficiency, setpoint_deviation, Design_Ton, effi_case, same_conditon_effi, data_count):
        self.GetData = GetData
        self.DrawFigs = DrawFigs
        self.ModifyDocx = ModifyDocx
        self.lan = self.GetData.lan
        self.LocationName = locationname
        self.customername = customername
        self.LocationCity = locationcity
        self.PostalCode = postalcode
        self.SiteAddress = siteaddress
        self.TimeZone = timezone
        self.IPLV_efficiency = IPLV_efficiency
        self.design_efficiency = design_efficiency
        self.setpoint_deviation = setpoint_deviation
        self.Design_Ton = Design_Ton
        self.effi_case = effi_case
        self.same_conditon_effi = same_conditon_effi
        self.data_count = data_count
        if self.Design_Ton != "-":  # 初投资为$350/冷吨，电费为$0.129/kWh
            self.payback_year = round(self.Design_Ton * 350 / (0.129 * self.GetData.save_power_peryear), 1)
        else:
            self.payback_year = "-"
        self.year = year
        if self.year == "":
            self.Age = ""
        else:
            # self.Age = str(datetime.datetime.today().year - int(year))
            wk = "%s-W%s-1" % (year, self.GetData.SN[0:2])
            delta_days = (datetime.datetime.today() - datetime.datetime.strptime(wk, '%Y-W%W-%w')).days
            self.Age = str(int(delta_days / 365))
        self.ModelNum = modelnumber
        self.design_efficiency_str = self.design_efficiency
        if self.design_efficiency == "-":
            self.DesignChillerPower = "-"
        else:
            self.DesignChillerPower = round(self.Design_Ton * self.design_efficiency)
            if len(str(self.design_efficiency).split(".")[1]) == 1:  # 将一位小数后加个0，凑成两位小数
                self.design_efficiency_str = ".".join([str(self.design_efficiency).split(".")[0],
                                                       str(self.design_efficiency).split(".")[1] + "0"])
        self.maxium_data_efficiency_str = (round(self.GetData.maxium_data_efficiency, 2))
        if len(str(self.maxium_data_efficiency_str).split(".")[1]) == 1:  # 将一位小数后加个0，凑成两位小数
            self.maxium_data_efficiency_str = ".".join([str(self.maxium_data_efficiency_str).split(".")[0],
                                                        str(self.maxium_data_efficiency_str).split(".")[1] + "0"])
        self.TodayDate = datetime.datetime.strftime(datetime.datetime.today(), "%d-%b-%Y")



    def execute(self):
        imgs_dict = {
            '$Entering_Condenser_Water': [self.GetData.ECDW_path[:-4] + "_" + GetData_VFD_obj.T_unit + self.GetData.ECDW_path[-4:]],
            "$effi_PLC_ECDW": [self.GetData.COP_PLC_ECDW_path],
            "$Chiller efficiency vs %RLA vs Runhrs": [self.GetData.box_performance_RLA_path[0:-4] + "_" + GetData_VFD_obj.T_unit + "." + self.GetData.box_performance_RLA_path.split(".")[-1]],
            "$Chiller efficiency vs Cooling load vs Runhrs": [self.GetData.box_performance_Ton_path[0:-4] + "_" + GetData_VFD_obj.T_unit + "." + self.GetData.box_performance_Ton_path.split(".")[-1]],
            "$LCW_SP": [self.GetData.LCW_STPT_path[0:-4] + "_" + GetData_VFD_obj.T_unit + "." + self.GetData.LCW_STPT_path.split(".")[-1]]
        }
        if self.GetData.T_unit == "F":
            imgs_dict["$effi_PLC_ECDW"] = [self.GetData.effi_PLC_ECDW_path]

        if os.access(self.GetData.fault_count_path, os.F_OK):
            imgs_dict["$alarm_count"] = [self.GetData.fault_count_path]

        for year in self.GetData.years:
            if year in self.GetData.year_data.keys():
                imgs_dict["$Temperature_Ton_" + str(year)] = [(".").join(self.GetData.year_month_avg_T_Ton_path.split(".")[0:-1]) + "_" + str(year) + self.GetData.T_unit + ".png"]
                imgs_dict["$Effi_EnergyConsumption_" + str(year)] = [(".").join(self.GetData.year_month_avg_effi_energy_path.split(".")[0:-1]) + "_" + str(year) + self.GetData.T_unit + ".png"]
                imgs_dict["$Ton_power_" + str(year)] = [(".").join(self.GetData.year_month_avg_Ton_power_path.split(".")[0:-1]) + "_" + str(year) + ".png"]

        deter_effi = round(100 * (self.same_conditon_effi - float(self.design_efficiency_str)) / float(self.design_efficiency_str), 1)

        replace_text = {"$ChillerSN": self.GetData.SN, "$LocationName": self.LocationName, "$CustomerName": self.customername,
                        "$LocationCity": self.LocationCity, "$PostalCode": self.PostalCode, "$SiteAddress": self.SiteAddress,
                        "$TimeZone": self.TimeZone, "$Year_Age": self.year + " (" + self.Age + " Years)", "$Age": self.Age, "$ModelNum": self.ModelNum,
                        "$StartDate": self.GetData.StartDate_str, "$EndDate": self.GetData.EndDate_str,
                        "$runhrs": self.GetData.Max_Runhr_str, "$lowloadsRate": self.GetData.lowloadsRate,
                        "$DeterEffi": abs(deter_effi),
                        "$SaveRate": self.GetData.SaveRate, "$min_ECDW": self.GetData.dis_PLC_df["ECDW_mean"].min(),
                        "$max_ECDW": self.GetData.dis_PLC_df["ECDW_mean"].max(), "$SavePower": self.GetData.SavePower, "$SaveP_peryear": self.GetData.save_power_peryear_str,
                        "$Efficiency_before": self.GetData.kW_Ton_fs, "$Efficiency_after": self.GetData.kW_Ton_vs,
                        "$Efficiency_rate": self.GetData.kW_Ton, "$IPLV_Efficiency": self.IPLV_efficiency,
                        "$setpoint_deviation": self.setpoint_deviation,
                        "$DesignRT": self.Design_Ton,
                        "$full_load_80": self.GetData.full_load_80, "$low_load_80": self.GetData.low_load_80,
                        "$Ton_range": self.GetData.maxium_running_time_Ton_range, "$total_alarms": self.GetData.total_alarms,
                        "$setpoint_meet": 100 - self.setpoint_deviation, "$MostRunhrsOFTon": self.GetData.MostRunhrsOFTon,
                        "$DesignChillerPower": self.DesignChillerPower, "$Today_date": self.TodayDate, "$data_count": self.data_count}

        replace_text["$Tonrange_per"] = str(int(100 * float(self.GetData.maxium_running_time_Ton_range.split("-")[0]) / float(self.Design_Ton))) + "-" + str(
            int(100 * float(self.GetData.maxium_running_time_Ton_range.split("-")[1]) / float(self.Design_Ton)))

        exceed_alarm_count = self.GetData.df_alarm_2months_valuecount15
        if exceed_alarm_count == 0:
            exceed_alarm_count = "no"
        replace_text["$exceed_15"] = exceed_alarm_count

        if self.GetData.T_unit == "F":
            replace_text["$maxium_data_min_ECDW"] = str(self.GetData.maxium_data_ECDW_F.left)
            replace_text["$maxium_data_max_ECDW"] = str(self.GetData.maxium_data_ECDW_F.right)
            replace_text["$maxium_data_mean_ECDW"] = str(round(self.GetData.maxium_data_mean_ECDW_F, 2)) + "℉"
            replace_text["$maxium_data_mean_LCW"] = str(round(self.GetData.maxium_data_mean_LCW_F, 2)) + "℉"
            replace_text["$performance_str"] = "efficiency"
            replace_text["$performance_unit"] = "kW/RT"
            replace_text["$maxium_data_efficiency"] = self.maxium_data_efficiency_str
            replace_text["$trend"] = "rising"
            replace_text["$T_Unit"] = "℉"
            replace_text["$Design_Efficiency"] = self.design_efficiency_str
            replace_text["$same_condition_effi"] = self.same_conditon_effi
            replace_text["$deviation_per"] = "2"
            replace_text["$MostRunhrsPerformance"] = self.GetData.maxium_running_time_effi
            replace_text["$90TonPerformance"] = self.GetData.Ton90_effi
            replace_text["$Design_LCW"] = str(round(float(Design_LCW) * 1.8 + 32, 1))
            replace_text["$Design_ECDW"] = str(round(float(Design_ECDW) * 1.8 + 32, 1))

        elif self.GetData.T_unit == "C":
            replace_text["$maxium_data_min_ECDW"] = str(self.GetData.maxium_data_ECDW_C.left)
            replace_text["$maxium_data_max_ECDW"] = str(self.GetData.maxium_data_ECDW_C.right)
            replace_text["$maxium_data_mean_ECDW"] = str(round(self.GetData.maxium_data_mean_ECDW_C, 2)) + "°C"
            replace_text["$maxium_data_mean_LCW"] = str(round(self.GetData.maxium_data_mean_LCW_C, 2)) + "°C"
            replace_text["$performance_str"] = "COP"
            replace_text["$performance_unit"] = ""
            replace_text["$maxium_data_efficiency"] = self.GetData.maxium_data_COP
            replace_text["$trend"] = "decreasing"
            replace_text["$T_Unit"] = "°C"
            replace_text["$Design_Efficiency"] = round(3.517 / float(self.design_efficiency_str), 1)
            replace_text["$same_condition_effi"] = round(3.517 / self.same_conditon_effi, 1)
            replace_text["$deviation_per"] = "3.6"
            replace_text["$MostRunhrsPerformance"] = self.GetData.maxium_running_time_COP
            replace_text["$90TonPerformance"] = self.GetData.Ton90_COP
            replace_text["$Design_LCW"] = round(float(Design_LCW), 1)
            replace_text["$Design_ECDW"] = round(float(Design_ECDW), 1)

        del_text = list(imgs_dict.keys())
        if deter_effi < 0:
            del_text.extend(["$positive_deter*$positive_deter", "$negative_deter"])
        else:
            del_text.append(["$negative_deter*$negative_deter", "$positive_deter"])

        if self.effi_case == "case1":
            del_text.extend(["$case2*$case2", "$case3*$case3", "$case1", "$General"])
        elif self.effi_case == "case2":
            del_text.extend(["$case1*$case1", "$case3*$case3", "$case2", "$General"])
        else:
            del_text.extend(["$case1*$case1", "$case2*$case2", "$General*General", "$case3"])

        if os.access(self.GetData.fault_count_path, os.F_OK):
            del_text.append("There are no alarms during this period.")
        if self.ModelNum.startswith("19XRV"):
            replace_text["$is_installed_VFD"] = "Yes"
        else:
            replace_text["$is_installed_VFD"] = "No"

        # #把没有年数据的表和描述删除掉
        new_years = list(self.GetData.year_data.keys())
        dif_year = set(self.GetData.years) - set(new_years)
        for year in dif_year:
            del_text.append(f"${year}info*${year}info")
        for year in new_years:
            del_text.append(f"${year}info")

        # 填充表格
        year_data = self.GetData.year_data.copy()
        for year, data in year_data.items():
            del data["Energy/kWh"]
            if GetData_VFD_obj.T_unit == "C":
                data = data[["LCW", "Power", "COP_ref", "Ton", "ECDW", "Energy/kWh_str"]]
                ModifyDocx_VFD_obj.replace_cell(ModifyDocx_VFD_obj.doc_file.tables[self.GetData.years.index(year) + 2], [1], [0], ["Leaving Chilled water temperature, °C"])
                ModifyDocx_VFD_obj.replace_cell(ModifyDocx_VFD_obj.doc_file.tables[self.GetData.years.index(year) + 2], [5], [0], ["Entering Condenser water temperature, °C"])
                ModifyDocx_VFD_obj.replace_cell(ModifyDocx_VFD_obj.doc_file.tables[self.GetData.years.index(year) + 2], [3], [0], ["Chiller COP"])
            else:
                data = data[["LCW_F", "Power", "Efficiency_all_current", "Ton", "ECDW_F", "Energy/kWh_str"]]
            data["Power"] = data["Power"].apply(lambda x: int(x) if x != "-" else x)
            data["Ton"] = data["Ton"].apply(lambda x: int(x) if x != "-" else x)
            year_month_avg_data_list = [data[col].to_list() for col in data.columns]
            target_values = sum(year_month_avg_data_list, [])
            # target_values = [int(value) if isinstance(value, float) and value > 1 else value for value in target_values] #删除xx.0的.0
            ModifyDocx_VFD_obj.replace_cell(ModifyDocx_VFD_obj.doc_file.tables[self.GetData.years.index(year) + 2], list(range(1, 7)), list(range(1, 13)), target_values)

        """将imgs_dict的value路径的图片都增加一个边框，并另存为一个后缀为_border的相对应路径中"""
        for key, value_list in imgs_dict.items():
            imgs_dict[key] = []
            for value in value_list:
                self.DrawFigs.image_border(value, value[0:-4] + "_temp" + ".png", 'a', 30, color=(255, 255, 255))  #先以一个白色的画布为底色，将原图片贴在上面，白色画布尺寸为原图四周向外拓展30单位
                self.DrawFigs.image_border(value[0:-4] + "_temp" + ".png", value[0:-4] + "_border" + ".png", 'a', 3, color=(0, 0, 0))  #再以一个黑色的画布为底色，将上图贴在上面，黑色画布尺寸为上图四周向外拓展3单位
                imgs_dict[key].append(value[0:-4] + "_border" + ".png")
        self.ModifyDocx.change_imgs(imgs_dict)
        self.ModifyDocx.del_blank_pages()
        self.ModifyDocx.replace_text(replace_text, del_text)  # save doc在这里面
        # self.ModifyDocx.replace_placeholder(replace_text) #save doc在这里面


def get_setpoint_deviation(chillerSN):
    """
    从原始数据中计算出开机后冷冻水出水温度未达到设定点的数据比例
    """
    df = pd.read_csv("C:/02_SVN/04_ChillerReplacement/North_America_chiller_retrofit/" + chillerSN + ".csv")
    # usecols=["Percent_Line_Current", "eventdatetime", "Leaving_Chilled_Water", "Control_Point"])

    rename_dict_list = {"DateTime": ["eventdatetime"],
                        "PLC": ["AMPS_%", "Percent_Line_Current", "ch_runstatus_analog"],
                        "LCW": ["Leaving_Chilled_Water", "ch_lcw"],
                        "Control_Point": ["lcw_sp", "SetPoint", "ControlPoint", "Control Point", "controlpoint"]}
    rename_dict = {}
    for key, value_list in rename_dict_list.items():
        for value in value_list:
            if value in df.columns:
                rename_dict[value] = key

    df.rename(columns=rename_dict, inplace=True)

    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df["PLC"] = pd.to_numeric(df["PLC"])
    df["LCW"] = pd.to_numeric(df["LCW"])
    df["SetPoint"] = pd.to_numeric(df["Control_Point"])
    df.fillna(method="ffill", inplace=True)
    df["PLC_shift"] = df["PLC"].shift(1)
    on_list = df.loc[(df["PLC"] != 0) & (df["PLC_shift"] == 0), "DateTime"].to_list()  # 每个开机时间段的第一个时间点
    df.query("PLC > 0", inplace=True)
    for on in on_list:
        df_drop = df.loc[(df["DateTime"] >= on)]
        df_drop = df_drop.loc[df_drop["DateTime"] < on + datetime.timedelta(hours=1)]
        data = df.append(df_drop)
        df = data.drop_duplicates(subset=["DateTime"], keep=False)
    setpoint_deviation = round(len(df.query("LCW-SetPoint>1.8")) / len(df) * 100)
    return df[["DateTime", "SetPoint", "LCW", "PLC"]], setpoint_deviation


if __name__ == "__main__":
    projectname = "北美10台chiller换机计算"
    chillerSN_list = ["4504Q70011", "4704Q70012", "4604Q70013"]
    # chillerSN_list = ["4704Q70012"]
    chiller_info_csv = pd.read_excel(r"C:\02_SVN\QT_VFD_1118_vDataCollection\conf\chiller_info.xlsx", index_col="serial_number")
    chiller_info_csv.index.astype(str)
    chiller_info_csv.replace(np.nan, "", inplace=True)
    chillertype = '19XR'
    ton = float(666)
    COP = float(6)
    tariff = float(0)
    invest = float(0)
    fill = "no_fill"
    language = 0  # 0为EN，1为CN
    for chillerSN in chillerSN_list:
        print(chillerSN, chillerSN_list.index(chillerSN))
        df_stpt_devi, setpoint_deviation = get_setpoint_deviation(chillerSN)
        try:
            locationName = chiller_info_csv.loc[chillerSN, "location name"]
        except:
            locationName = ""
        try:
            customerName = chiller_info_csv.loc[chillerSN, "customer name"]
        except:
            customerName = ""
        try:
            locationCity = chiller_info_csv.loc[chillerSN, "City"]
        except:
            locationCity = ""
        try:
            postalcode = chiller_info_csv.loc[chillerSN, "postal code"]
        except:
            postalcode = ""
        try:
            siteaddress = chiller_info_csv.loc[chillerSN, "site address"]
        except:
            siteaddress = ""
        try:
            timezone = chiller_info_csv.loc[chillerSN, "timezone"]
        except:
            timezone = ""
        try:
            modelnumber = chiller_info_csv.loc[chillerSN, "Chiller Model Number"]
        except:
            modelnumber = ""
        try:
            design_efficiency = round(chiller_info_csv.loc[chillerSN, "Design efficiency"], 2)
        except:
            design_efficiency = "-"
        try:
            IPLV_efficiency = chiller_info_csv.loc[chillerSN, "IPLV_efficiency"]
        except:
            IPLV_efficiency = ""
        try:
            Design_Ton = round(chiller_info_csv.loc[chillerSN, "Design Ton"], 0)
        except:
            Design_Ton = "-"
        try:
            Design_LCW = str(chiller_info_csv.loc[chillerSN, "Design LCW"])
        except:
            Design_LCW = "-"
        try:
            Design_ECDW = str(chiller_info_csv.loc[chillerSN, "Design ECDW"])
        except:
            Design_ECDW = "-"

        if chillerSN[2:4].isdigit():  # str.isdigit()判断str中是否全部是数字
            if int(chillerSN[2:4]) < 23:
                year_str = "20" + chillerSN[2:4]
            elif int(chillerSN[2:4]) > 23:
                year_str = "19" + chillerSN[2:4]
            connect_date = year_str + "-01-01"
        else:
            year_str = ""
            connect_date = year_str
        """实例化GetData类，并调用需要的函数"""
        GetData_VFD_obj = GetData(chillertype, chillerSN, ton, COP, fill, tariff, invest, language)
        GetData_VFD_obj.set_path("..")
        GetData_VFD_obj.get_word_path("Chiller Replacement Report_V3", "Chiller Replacement")
        GetData_VFD_obj.get_data_path()
        GetData_VFD_obj.get_figs_path()
        GetData_VFD_obj.get_language()
        GetData_VFD_obj.get_VFD_analysis_data()
        GetData_VFD_obj.get_Total_COP()
        GetData_VFD_obj.get_dis_PLC_df()
        GetData_VFD_obj.get_dis_Ton_df(Design_Ton)
        GetData_VFD_obj.get_alarm_analysis()
        GetData_VFD_obj.get_maximun_data_ECDW()
        GetData_VFD_obj.get_specific_bin_ECDW_data()
        GetData_VFD_obj.get_load_bool()
        effi_case, same_conditon_effi, data_count = GetData_VFD_obj.get_effi_case(Design_LCW, Design_ECDW)
        GetData_VFD_obj.get_specific_year_data(years=[2022, 2023, 2024])

        """实例化DrawFigs类"""
        DrawFigs_obj = DrawFigs(GetData_VFD_obj)
        if (timezone.split("/")[0] == "America") or (timezone.split("/")[1] == "Kuwait"):  # 北美机器要求温度显示华氏度°F & 冷机性能显示：T/kW
            GetData_VFD_obj.T_unit = "F"
            # GetData_VFD_obj.df_dis 数据表中4个水温，3个COP需要转换
            """C --> F"""
            for T_col in ["LCW_min", "LCW_max", "LCW_mean",
                          "LCDW_min", "LCDW_max", "LCDW_mean",
                          "ECW_min", "ECW_max", "ECW_mean",
                          "ECDW_min", "ECDW_max", "ECDW_mean"]:
                GetData_VFD_obj.dis_PLC_df[T_col] = round(GetData_VFD_obj.dis_PLC_df[T_col] * 1.8 + 32, 1)
            GetData_VFD_obj.dis_PLC_df["efficiency_max"] = round(3.517 / GetData_VFD_obj.dis_PLC_df["COP_ref_min"], 2)
            GetData_VFD_obj.dis_PLC_df["efficiency_min"] = round(3.517 / GetData_VFD_obj.dis_PLC_df["COP_ref_max"], 2)
            GetData_VFD_obj.dis_PLC_df["efficiency_mean"] = round(3.517 / GetData_VFD_obj.dis_PLC_df["COP_ref_mean"], 2)
        else:
            GetData_VFD_obj.T_unit = "C"

        DrawFigs_obj.draw_line_plot(df_stpt_devi)
        DrawFigs_obj.draw_from_plot_config(GetData_VFD_obj.draw_analysis)

        dis_PLC_df = GetData_VFD_obj.dis_PLC_df.dropna(subset=["ECDW_min", "ECDW_max", "ECDW_mean"], how="all")
        DrawFigs_obj.draw_from_plot_config(dis_PLC_df)
        DrawFigs_obj.draw_performance_RLA_box(GetData_VFD_obj.dis_PLC_df)
        DrawFigs_obj.draw_performance_Ton_box(GetData_VFD_obj.dis_Ton_df)
        DrawFigs_obj.draw_sns_scatter(GetData_VFD_obj.data_merge)

        if not GetData_VFD_obj.alarm_data.empty:
            DrawFigs_obj.draw_alarm_analysis(GetData_VFD_obj.alarm_data)

        DrawFigs_obj.draw_year_data(GetData_VFD_obj.year_data)
        """实例化"""
        ModifyDocx_VFD_obj = ModifyDocx_VFD(GetData_VFD_obj, connect_date, projectname)
        OutputVFDReport = OutputReport(GetData_VFD_obj, DrawFigs_obj, ModifyDocx_VFD_obj, locationName, customerName, locationCity, postalcode,
                                       siteaddress, timezone, modelnumber, year_str, IPLV_efficiency, design_efficiency,
                                       setpoint_deviation, Design_Ton, effi_case, same_conditon_effi, data_count)
        OutputVFDReport.execute()

        import shutil
        from docx2pdf import convert

        """将报告复制到onedrive文件夹，并上传云端"""  # 先转换为pdf再复制
        source_report_path = os.path.abspath(GetData_VFD_obj.save_path)
        pdf_report_path = os.path.abspath(GetData_VFD_obj.save_path).split(".")[0] + ".pdf"
        convert(source_report_path, pdf_report_path)
        # target_report_path = "C:/Users/XUl8/OneDrive - Carrier Corporation/02_Project/06_SPT for VFD word report/result/Chiller_Replacement_word_EN/" + chillerSN + "_Chiller_Replacement_report.docx"
        # target_pdf_path = "C:/Users/XUl8/OneDrive - Carrier Corporation/02_Project/06_SPT for VFD word report/result/Chiller_Replacement_word_EN/" + chillerSN + "_Chiller_Replacement_report.pdf"
        # shutil.copyfile(source_report_path, target_report_path)
        # shutil.copyfile(pdf_report_path, target_pdf_path)
