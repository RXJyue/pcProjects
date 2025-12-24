# _*_ coding: utf-8 _*_
"""
Time:     1/26/2024 10:48 AM
Author:   XuLing
"""
"""此代码用于从azure数据库中下载alarm数据，只下载23/24年，因为23/24年alarm才有fault description"""
import os
import time
from azure.storage.blob import ContainerClient
# from func_timeout import func_set_timeout

container_url = "https://csdatalakeprod.blob.core.windows.net/smartchillerprodgen2/AlertAlarm"
sastoken = "sp=rlep&st=2023-12-29T06:53:52Z&se=2024-12-31T14:53:52Z&spr=https&sv=2022-11-02&sr=c&sig=IXZXDXT9U8cPaij9FtEzuYg4Mv8sG4LpECYjCJSs0IQ%3D"
local_path = os.path.join("..", "alarm_json")
download_year = ["2022", "2023", "2024"]

def get_download_path(chiller, download_year):
    path_list = []
    for year in download_year:
        path_list.append(os.path.join(chiller, year + ".json"))
    return path_list

# @func_set_timeout(600)
def download_blob(blob):
    try:
        container_client = ContainerClient.from_container_url(container_url + '?' + sastoken)
        blob_client = container_client.get_blob_client(blob)
        print("-------begin " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), blob)
        with open(os.path.join(local_path, blob), "wb") as my_blob: #注意，open函数自动创建空文件功能只能在已有文件夹的前提下
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
        print("-------success download " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), blob)
    except:
        print("-------fail download " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), blob)

if __name__ =="__main__":
    chillerSN_list = ["4504Q70011", "4704Q70012", "4604Q70013"]
    for chillerSN in chillerSN_list:
        path_list = get_download_path(chillerSN, download_year)
        for path in path_list:
            if not os.path.isdir(os.path.join(local_path, chillerSN)):
                os.makedirs(os.path.join(local_path, chillerSN))
            download_blob(path) #下载指定文件