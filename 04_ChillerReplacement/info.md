# chiller replacement report 处理流程

CREATE DATE | 2024.9.3
LAST UPDATE | 2024.9.9

author: xuling

## 1.下载

### 1.1 写入需要下载的chiller（batch_calculate_input_chillers_template），从abound 下载最近3年数据(使用BatchMain.py)

### 1.2 从abound 下载最近3年alarm info(使用16_alarm_records_download_analysis)，配置环境并更改以下文件中的chillersn_list：

##### 1. Alarm_download 2. Json2csv 3.Analysis_csv

### 1.3 从abound 查找此台机器的chiller info 信息并写入 chiller_info.csv，删掉重复chiller信息

##### （\\172.24.236.209\share\QT_VFD_1118_vDataCollection\conf）

##### Design efficiency：Design Efficieny (kw/T)

##### Design Ton：Chiller Capacity (Ton)

##### Design LCW： Design Chiller Setpoint (摄氏度)

##### Design ECDW：Design Entering Condenser Water（摄氏度）

## 2.数据预处理

### 2.1 使用上述1.1的工具“开始计算功能”，从batch_preprocessed_data目录下找到预处理好的数据

##### （\\172.24.236.209\share\QT_VFD_1118_vDataCollection\batch_preprocessed_data）

### 2.2 将上述2.1的csv文件放入North_Ameriaca_chiller_retrofit中

### 2.3 把1.2的文件放入16_alarm_records_download_analysis\alarm_csv中

## 3. 数据计算

### 3.1 用2.2的结果运行并更改ChillerRetrofit.py中需要计算的chiller, 计算chiller replacement的结果

### 3.2 运行 "换机报告的数据准备.py"，处理3.1的结果

## 4. 报告生成

### 4.1 运行 Report_Replace_word_en.py 生成报告
