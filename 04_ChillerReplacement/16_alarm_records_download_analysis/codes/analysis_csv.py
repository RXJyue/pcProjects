# _*_ coding: utf-8 _*_
"""
Time:     1/26/2024 1:40 PM
Author:   XuLing
"""

"""此文件用于将从json文件转换为的csv文件，
1.description有值的留下；
2.删除rest=True的数据；
并保存至description_alarm_csv文件夹中"""

import os
import pandas as pd

if __name__ == "__main__":
    csv_path = os.path.join("..", "alarm_csv")
    chillerSN_list = ["4504Q70011", "4704Q70012", "4604Q70013"]
    for chillerSN in chillerSN_list:
        csv_save_path = os.path.join("..", "description_alarm_csv")
        df = pd.read_csv(os.path.join(csv_path, chillerSN + ".csv"))
        df.dropna(subset=["description"], inplace=True)
        if not df.empty:
            df.query("isreset == False", inplace=True)  # alarm里要剔除掉reset的数据
        if not df.empty:
            df.to_csv(os.path.join(csv_save_path, chillerSN + ".csv"))