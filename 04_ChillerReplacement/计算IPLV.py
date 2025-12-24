# _*_ coding: utf-8 _*_
"""
Time:     1/8/2024 1:18 PM
Author:   XuLing
"""


"""计算IPLV, 先通过ChillerRetrofit中函数：rule_cop2计算出ton，再根据ton使用函数：Ecat_COP计算出不同负荷的额定COP，再通过标准中的公式计算IPLV"""
import pandas as pd
from ChillerRetrofit import Ecat_COP

"""把值写进excel表中"""
chiller_info_path = r"C:\02_Project\13_SPT_Tag\V24_01_18Tag\conf\chiller_info.csv"
df = pd.read_csv(chiller_info_path)

dict = {'1913Q22565': 653.802253062401, '2301Q65746': 325.16524642632436, '2511Q20862': 330.34215404791723, '2608Q18009': 334.6735696123318, '2619Q27626': 316.58240906275006, '4004Q69950': 316.69506229082117, '4415Q24810': 765.5345531065716, '4998J59038': 862.2918042341641, '5111Q21335': 741.1359986763518, '5200Q64908': 561.5118251428145}

input_data = pd.DataFrame({"PLR": [100, 75, 50, 25],
                           "ECDW": [30, 24.5, 19, 19],
                           "LCW": [7, 7, 7, 7],
                           }) #来自标准
for chillerSN in list(dict.keys()):
    print(chillerSN)
    Ton = dict[chillerSN]
    data_output, ton_output = Ecat_COP(input_data, new_col='psm_cop', chtp='19XRV', tonnage=Ton, PLR='PLR', LT='LCW', ECT='ECDW')
    IPLV_COP = round(0.01*data_output["psm_cop"][0] + 0.42*data_output["psm_cop"][1] + 0.45*data_output["psm_cop"][2] + 0.12*data_output["psm_cop"][3], 1)#公式来自标准
    df.loc[df["serial_number"] == chillerSN, "IPLV_COP"] = IPLV_COP
    df.loc[df["serial_number"] == chillerSN, "IPLV_efficiency"] = round(3.517/IPLV_COP, 2)
df.to_csv(chiller_info_path)





