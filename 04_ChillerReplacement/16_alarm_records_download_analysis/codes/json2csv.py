# _*_ coding: utf-8 _*_
"""
Time:     1/23/2024 4:08 PM
Author:   XuLing
"""
"""此代码用于将已下载好的假json格式的alarm records转换为csv格式"""
import os
import json
import pandas as pd

def have_csv(chillerSN, csv_save_path):
    for dirpath, dirnames, filenames in os.walk(csv_save_path):
        if str(chillerSN) + ".csv" in filenames:
            return True
        else:
            continue
    return False

def findfiles(path, result):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            result = findfiles(cur_path, result)
        else:
            result.append(cur_path)
    return result

def json2csv_bc(json_path, csv_path):
    """  #用于json文件非一行一个dict的情况
    :param json_path: 存放对应chillerSN的json文件的路径. eg: '..\\alarm_json\\1913Q22565'
    :param csv_path: 保存csv文件的路径. eg: '..\\alarm_csv\\1913Q22565.csv'
    :return:
    """
    year_list = []
    file_paths = findfiles(json_path, [])
    for file_path in file_paths: #打开某一个json文件，并对其处理
        with open(file_path, 'r', encoding='utf8') as file:
            df_list = []
            for line in file:
                line_list = line.split("}{")  # 再以背靠背的大括号来把每一条记录分成一个str
                output_list = []
                for line in line_list:
                    if "{" not in line:  # 再给每一条记录缺失的前后大括号给补上
                        line = "{" + line
                    if "}" not in line:
                        line = line + "}"
                    dict_line = json.loads(line)  # str转换为dict
                    output_list.append(dict_line)
                df = pd.DataFrame.from_records(output_list)
                df_list.append(df)
            df_output = pd.concat(df_list)
            year_list.append(df_output)
    year_df = pd.concat(year_list)
    year_df.to_csv(csv_path)


def json2csv(json_path, csv_path):
    file_paths = findfiles(json_path, [])
    alarm_list = []
    for file_path in file_paths:
        df_alarm = pd.read_json(file_path, lines=True)
        alarm_list.append(df_alarm)
    df_output = pd.concat(alarm_list)
    df_output.to_csv(csv_path)

if __name__ == "__main__":
    json_path = os.path.join("..", "alarm_json")
    csv_save_path = os.path.join("..", "alarm_csv")
    chillerSN_list = ["4504Q70011", "4704Q70012", "4604Q70013"]
    for chillerSN in chillerSN_list:
        json_path_SN = os.path.join(json_path, chillerSN)
        csv_save_path_SN = os.path.join(csv_save_path, chillerSN + ".csv")
        if not os.path.exists(csv_save_path): #构建一个路径来保存csv文件
            os.mkdir(os.path.join("..", "alarm_csv"))
        # if not have_csv(chillerSN, csv_save_path): #如果csv_save_path文件夹中没有对应的chiller文件
        json2csv(json_path_SN, csv_save_path_SN)