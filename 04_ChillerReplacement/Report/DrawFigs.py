# _*_ coding: utf-8 _*_
"""
Time:     6/8/2023 10:31 AM
Author:   XuLing
"""
import os
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
sns.set(style="whitegrid", font='Times New Roman', font_scale=1.4)

import matplotlib
matplotlib.rcParams["font.size"] = 18
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
plt.switch_backend('Agg')

class DrawFigs:
    def __init__(self, GetData):
        self.GetData = GetData
        self.draw_fig_path = self.GetData.parent_path + "/conf/plot_config_for_report.xlsx"

    def Sort_Order(self, data, col):
        order_list = data[col].unique().tolist()
        order_list = [i for i in order_list if i == i]
        if '_range' in col:
            order_list.sort(key=lambda x: float(x.split('~')[0]))
            return order_list
        else:
            return list(np.sort(order_list))

    def draw_from_plot_config(self, data):
        plot_config = pd.read_excel(self.draw_fig_path)
        for index, row in plot_config.iterrows():
            try:
                if ((index != 0) and (plot_config.loc[index - 1, "plot"])) or index == 0: #遍历到（index-1）行的plot为False或index=0行（即认为index行开始画图）
                    fig, ax = plt.subplots(figsize=(int(row["figsize"].split(",")[0]), int(row["figsize"].split(",")[1])))
                    ax.set_title(row["title"]).set_fontsize(row["title_fontsize"])
                    ax.set_ylabel(row["y_label"]).set_fontsize(row["y_label_fontsize"])
                    if row["plot_type"] == "bar" and row["LR"] == "L":
                        exec('ax.%s(%s,%s,%s,%s="%s", %s="%s")' % (row["plot_type"], list(data.index + row["x_shift"]),
                            data[row["y"]].to_list(), row["width"], "label", row["legend_label"], "color",
                            row["color"]))
                        if row["text"] == True:
                            for a, b in zip(list(data.index + row["x_shift"]), data[row["y"]].to_list()):
                                plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
                    if row["plot_type"] == "plot" and row["LR"] == "L":
                        exec('ax.%s(%s,%s,%s="%s",marker="o", markersize=8, markerfacecolor="red", %s="%s")' % (
                            row["plot_type"], list(data.index), data[row["y"]].to_list(), "label",
                            row["legend_label"], "color", row["color"]))
                        if row["text"] == True:
                            for a, b in zip(list(data.index), data[row["y"]].to_list()):
                                plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
                    if row["plot_type"] == "scatter" and row["LR"] == "L":
                        exec('ax.%s(data["%s"],data["%s"],%s="%s", %s="%s")' % (row["plot_type"], row["x"], row["y"], "label", row["legend_label"], "color", row["color"]))
                        plt.xlim([data[row["x"]].min(), data[row["x"]].max()])
                    if isinstance(row["legend_anchor"], str):
                        ax.legend(loc=row["legend_loc"], bbox_to_anchor=(float(row["legend_anchor"].split(",")[0]), float(row["legend_anchor"].split(",")[1])))
                    else:
                        ax.legend(loc=row["legend_loc"])
                    ax.set_axisbelow(True)
                    ax.grid(zorder=2.5)
                    if row["x_ticks_label"] == "月份" or row["x_ticks_label"] == "PLC_label" or row["x_ticks_label"] == "Month":
                        ax.set_xticks(list(data.index))
                        ax.set_xticklabels(data[row["x_ticks_label"]].to_list(), rotation=30)
                    ax.set_xlabel(row["x_label"])
                    ax.xaxis.label.set_fontsize(row["x_label_fontsize"])
                    if row["axhline"] == row["axhline"]:
                        plt.axhline(y=row["axhline"], c="r", ls="--")
                    if (index < len(plot_config)-1 and plot_config.loc[index + 1, "LR"] == "R") or (index < len(plot_config)-2 and plot_config.loc[index + 2, "LR"] == "R"):
                        ax1 = ax.twinx()
                        ax1.grid()
                        ax1.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
                        ax1.set_ylim(0, 1)
                        # ax1.legend(loc=row["legend_loc"])
                    if row["plot_type"] == "bar" and row["LR"] == "R":
                        exec('ax1.%s(%s,%s,%s,%s="%s", %s="%s")' % (
                            row["plot_type"], list(data.index + row["x_shift"]),
                            data[row["y"]].to_list(), row["width"], "label", row["legend_label"], "color",
                            row["color"]))
                    if row["plot_type"] == "plot" and row["LR"] == "R":
                        exec('ax1.%s(%s,%s,%s="%s", marker="o", markersize=8, markerfacecolor="red", %s="%s")' % (
                            row["plot_type"], list(data.index), data[row["y"]].to_list(), "label",
                            row["legend_label"], "color", row["color"]))
                    if index < len(plot_config)-1 and plot_config.loc[index + 1, "LR"] == "R":
                        row_ax1 = plot_config.iloc[index + 1]
                        ax1.set_ylabel(row_ax1["y_label"]).set_fontsize(row_ax1["y_label_fontsize"])
                    elif index < len(plot_config)-2 and plot_config.loc[index + 2, "LR"] == "R":
                        row_ax1 = plot_config.iloc[index + 2]
                        ax1.set_ylabel(row_ax1["y_label"]).set_fontsize(row_ax1["y_label_fontsize"])
                else:
                    if row["plot_type"] == "bar" and row["LR"] == "L":
                        exec('ax.%s(%s,%s,%s,%s="%s", %s="%s")' % (
                            row["plot_type"], list(data.index + row["x_shift"]),
                            data[row["y"]].to_list(), row["width"], "label", row["legend_label"], "color",
                            row["color"]))
                        if isinstance(row["legend_anchor"], str):
                            ax.legend(loc=row["legend_loc"], bbox_to_anchor=(
                            float(row["legend_anchor"].split(",")[0]), float(row["legend_anchor"].split(",")[1])))
                        else:
                            ax.legend(loc=row["legend_loc"])
                        if row["text"] == True:
                            for a, b in zip(list(data.index + row["x_shift"]), data[row["y"]].to_list()):
                                plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
                    if row["plot_type"] == "plot" and row["LR"] == "L":
                        exec('ax.%s(%s,%s,%s="%s",marker="o",markersize=8, markerfacecolor="red", %s="%s")' % (
                            row["plot_type"], list(data.index), data[row["y"]].to_list(), "label",
                            row["legend_label"], "color", row["color"]))

                        if isinstance(row["legend_anchor"], str):
                            ax.legend(loc=row["legend_loc"], bbox_to_anchor=(
                                float(row["legend_anchor"].split(",")[0]), float(row["legend_anchor"].split(",")[1])))
                        else:
                            ax.legend(loc=row["legend_loc"])
                        if row["text"] == True:
                            for a, b in zip(list(data.index), data[row["y"]].to_list()):
                                plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
                    if row["plot_type"] == "scatter" and row["LR"] == "L":
                        exec('ax.%s(data["%s"],data["%s"],%s="%s", %s="%s")' % (
                        row["plot_type"], row["x"], row["y"], "label", row["legend_label"], "color", row["color"]))
                        ax.legend(loc=row["legend_loc"])
                    if row["plot_type"] == "bar" and row["LR"] == "R":
                        exec('ax1.%s(%s,%s,%s,%s="%s", %s="%s")' % (
                            row["plot_type"], list(data.index + row["x_shift"]),
                            data[row["y"]].to_list(), row["width"], "label", row["legend_label"], "color",
                            row["color"]))
                        ax1.legend(loc=row["legend_loc"])
                    if row["plot_type"] == "plot" and row["LR"] == "R":
                        exec('ax1.%s(%s,%s,%s="%s",marker="o",markersize=8, markerfacecolor="red", %s="%s")' % (
                            row["plot_type"], list(data.index), data[row["y"]].to_list(), "label",
                            row["legend_label"], "color", row["color"]))
                        ax1.legend(loc=row["legend_loc"])
                if row["plot"] == True:
                    if row["save_path"] in ["EfficiencyPLCRunhrs.png", "COPPLCRunhrs.png"]:
                        ax.grid(visible=None)
                        ax1.grid(axis="both")
                        ax.set_zorder(2)
                        ax1.set_zorder(1)
                        ax.patch.set_visible(False)
                    plt.savefig(self.GetData.path + '/analysis/' + self.GetData.SN + row["save_path"])
                    plt.close()
            except:
                plt.close()
                continue

    def draw_sns_scatter(self, data):
        sns.set(style="whitegrid", font='Times New Roman', font_scale=1.4)
        """横坐标为时间，纵坐标为COP，变频改造前后的COP散点图"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_title(self.GetData.lan["COP_B_A"]).set_fontsize(18)
        sns.scatterplot(self.GetData.data_merge.DateTime, self.GetData.data_merge.COP_all_compare, label=self.GetData.lan["COP_A"])
        sns.scatterplot(self.GetData.data_merge.DateTime, self.GetData.data_merge.COP_all_current, label=self.GetData.lan["COP_B"])
        plt.xlim(self.GetData.data_merge.DateTime.min(), self.GetData.data_merge.DateTime.max())
        ax.set_xlabel(self.GetData.lan["Time"])
        ax.xaxis.label.set_fontsize(18)
        ax.set_ylabel('Chiller COP').set_fontsize(18)
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.legend()
        plt.savefig(self.GetData.COP_path)
        plt.close()

        """横坐标为时间，纵坐标为chiller efficiency，变频改造前后的efficiency散点图"""
        for title, save_path in {"Chiller efficiency before and after retrofit": self.GetData.Efficiency_path,
                                 "Chiller efficiency before and after replacement": self.GetData.Efficiency_Replace_path}.items():
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.set_title(title).set_fontsize(18)
            sns.scatterplot(self.GetData.data_merge.DateTime, self.GetData.data_merge.Efficiency_all_compare,
                            label="Efficiency after")
            sns.scatterplot(self.GetData.data_merge.DateTime, self.GetData.data_merge.Efficiency_all_current,
                            label="Efficiency before")
            plt.xlim(self.GetData.data_merge.DateTime.min(), self.GetData.data_merge.DateTime.max())
            ax.set_xlabel(self.GetData.lan["Time"])
            ax.xaxis.label.set_fontsize(18)
            ax.set_ylabel('Chiller efficiency/(kW/T)').set_fontsize(18)
            plt.xticks(rotation=20)
            plt.tight_layout()
            plt.legend(loc="left upper")
            plt.savefig(save_path)
            plt.close()

        if not "Energy Saving%" in self.GetData.data_merge.columns:
            if "节能百分比" in self.GetData.data_merge.columns:
                self.GetData.data_merge["Energy Saving%"] = self.GetData.data_merge["节能百分比"] * 100
            else:
                self.GetData.data_merge["Energy Saving%"] = self.GetData.data_merge[self.GetData.lan["S%"]]*100

        """横坐标为PLC，纵坐标为ECDW，并且hue为Energy saving%的散点图"""
        for title, save_path in {"VFD retrofit saving potential": self.GetData.SaveRate_path,
                                 "Chiller replacement saving potential": self.GetData.SaveRate_Replace_path}.items():
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.set_title(title).set_fontsize(18)
            sns.scatterplot(100*self.GetData.data_merge.PLC, self.GetData.data_merge.ECDW, hue=data["Energy Saving%"],
                            hue_order=self.Sort_Order(self.GetData.data_merge, "Energy Saving%"), palette='rainbow')
            ax.set_xlabel("%RLA")
            ax.xaxis.label.set_fontsize(18)
            ax.set_ylabel('Chiller efficiency kW/T').set_fontsize(18)
            plt.tight_layout()
            plt.legend()
            plt.savefig(self.GetData.effi_PLC_ECDW_path)
            plt.close()

            #上图再画一个纵坐标为F的
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.set_title(title).set_fontsize(18)
            sns.scatterplot(100*self.GetData.data_merge.PLC, round((self.GetData.data_merge.ECDW) * 1.8 + 32, 1), hue=data["Energy Saving%"],
                            hue_order=self.Sort_Order(self.GetData.data_merge, "Energy Saving%"), palette="rainbow")
            ax.set_xlabel("%RLA")
            ax.xaxis.label.set_fontsize(18)
            ax.set_ylabel('Entering condenser water temperature/°F').set_fontsize(18)
            plt.tight_layout()
            plt.legend()
            plt.savefig(save_path[:-4] + "_F" + save_path[-4:])
            plt.close()

        """横坐标是PLC，纵坐标是Chiller efficiency， ECDW以5为bin找到数据量最多的bin，画出所有点"""
        data["year"] = data.DateTime.dt.year
        data["ECDW_F"] = 1.8 * data["ECDW"] + 32
        #先画英制
        #先找出ECDW哪个区间点最多
        bins = list(range(0, 100, 5))
        s = pd.cut(data['ECDW_F'], bins).value_counts()
        self.maxium_data_ECDW = s.index[0]
        for bin_max, save_path in {s.index[0]: self.GetData.effi_PLC_ECDW_path, s.index[1]: self.GetData.effi_PLC_ECDW1_path}.items():
            data_ECDW = data[data["ECDW_F"].between(bin_max.left, bin_max.right)]
            data_ECDW["PLC"] = 100 * data_ECDW["PLC"]
            data_ECDW["Efficiency_all_current"] = 3.517 / data_ECDW["COP_all_current"]
            fig, ax = plt.subplots(figsize=(15, 8))
            ax.set_title("%Full Load Design Ton vs chiller efficiency in range " + str(bin_max.left) + "-" + str(bin_max.right) + " ( ECDWT/°F)").set_fontsize(18)
            for year in data_ECDW.year.unique():
                sns.scatterplot(data=data_ECDW[data_ECDW["year"] == year], x="PLC", y="Efficiency_all_current", s=100)
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height]) # 将ax坐标轴往左压缩，留下放legend的空间
            legend_labels = [str(yea) + " year" for yea in data_ECDW.year.unique()]
            plt.legend(labels=legend_labels, bbox_to_anchor=(1.03, 0.8), loc=3, borderaxespad=0, prop={'size': 12})  #legend在画布外显示
            ax.set_xlabel("%Full Load Design Ton")
            ax.set_ylabel("Chiller efficiency(kW/T)").set_fontsize(18)
            ax.xaxis.label.set_fontsize(18)
            plt.savefig(save_path)
            plt.close()

        #再画公制
        # 先找出ECDW哪个区间点最多
        bins = list(range(0, 100, 5))
        s = pd.cut(data['ECDW'], bins).value_counts()
        for bin_max, save_path in {s.index[0]: self.GetData.COP_PLC_ECDW_path, s.index[1]: self.GetData.COP_PLC_ECDW1_path}.items():
            data_ECDW = data[data["ECDW"].between(bin_max.left, bin_max.right)]
            data_ECDW["PLC"] = 100*data_ECDW["PLC"]
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.set_title("%Full Load Design Ton vs COP in range " + str(bin_max.left) + "-" + str(
                bin_max.right) + " ( ECDWT/°C)").set_fontsize(18)
            for year in data_ECDW.year.unique():
                sns.scatterplot(data=data_ECDW[data_ECDW["year"] == year], x="PLC", y="COP_all_current", s=100)
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
            legend_labels = [str(yea) + " year" for yea in data_ECDW.year.unique()]
            plt.legend(labels=legend_labels, bbox_to_anchor=(1.01, 0.8), loc=3, borderaxespad=0, prop={'size': 12})  # legend在画布外显示
            ax.set_xlabel("%Full Load Design Ton")
            ax.set_ylabel("COP").set_fontsize(18)
            ax.xaxis.label.set_fontsize(18)
            plt.savefig(save_path)
            plt.close()

    def draw_alarm_analysis(self, data): #for chiller replacement
        data_plot = pd.DataFrame({"Count": data.values, "Fault": data.index.to_list()})
        f, ax = plt.subplots(figsize=(14, 7))
        plt.subplots_adjust(left=0.5, right=0.95, top=0.95, bottom=0.15)
        plt.title("Fault category", fontsize=18)
        sns.set_color_codes("pastel")
        sns.barplot(x="Count", y="Fault", data=data_plot, label="2022", color=[0.0824, 0.1725, 0.451], orient="h")
        sns.set_color_codes("muted")
        plt.xlabel("count of fault occurrence", fontdict={"size": 18, "color": "black"})
        plt.yticks(fontsize=15)
        plt.savefig(self.GetData.fault_count_path)
        plt.close()

    def draw_line_plot(self, data): #for chiller replacement
        """画一个横坐标为时间，纵坐标为leaving chilled water和control point，注意fill between，公制和英制各画一次分别保存"""
        data.query("PLC>0", inplace=True)
        data["LCW_C"] = data["LCW"]
        data["LCW_F"] = data["LCW"] * 1.8 + 32

        data["Control Point_C"] = data["SetPoint"]
        data["Control Point_F"] = data["SetPoint"] * 1.8 + 32

        for unit in ["C", "F"]:
            f, ax = plt.subplots(figsize=(14, 9))
            plt.title("Leaving Chilled Water Temperature Profile(°%s) vs time" % unit, fontsize=18)
            ax.plot(data["DateTime"], data["Control Point_%s" % unit], color="blue", label="Control Point")
            ax.fill_between(data["DateTime"], 0, data["Control Point_%s" % unit], facecolor='blue', alpha=0.3)
            ax.plot(data["DateTime"], data["LCW_%s" % unit], color="red", label="Leaving Chilled Water Temperature")
            ax.fill_between(data["DateTime"], data["Control Point_%s" % unit], data["LCW_%s" % unit], facecolor='red', alpha=0.3)
            plt.xlabel("Time", fontdict={"size": 18, "color": "black"})
            plt.ylim(0, )
            plt.ylabel("Temperature(°%s)" % unit)
            handles, labels = ax.get_legend_handles_labels()  # 获取legend
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
            plt.legend(handles=handles, bbox_to_anchor=(1.01, 0.89), loc=3, borderaxespad=0, prop={'size': 12})  # 双纵坐标时legend显示在一起，并在画布外显示
            plt.xticks(rotation=20)
            plt.yticks(fontsize=15)
            #设计图中x轴的间距
            data_x_axis = data.copy()
            data_x_axis.dropna(subset=["Control Point_%s" % unit, "LCW_%s" % unit], how="all", inplace=True)
            multi_xlabel =  ((data_x_axis.DateTime.max() - data_x_axis.DateTime.min()).days)/9
            ax.xaxis.set_major_locator(MultipleLocator(multi_xlabel))
            plt.savefig(self.GetData.LCW_STPT_path[0:-4] + "_" + unit + "." + self.GetData.LCW_STPT_path.split(".")[-1])
            plt.close()

    def draw_performance_RLA_box(self, data): #for chiller replacement
        self.GetData.data["cut_PLC"] = pd.cut(self.GetData.data['PLC'], bins=[0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.2],
                                 labels=["<30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", ">90"])
        box_data_list_F = []
        box_data_list_C = []

        for label in ["30-40", "40-50", "50-60", "60-70", "70-80", "80-90", ">90"]:
            box_data_F = self.GetData.data[self.GetData.data["cut_PLC"] == label]["Efficiency_all_current"]
            box_data_C = self.GetData.data[self.GetData.data["cut_PLC"] == label]["COP_all_current"]
            box_data_list_F.append(box_data_F)
            box_data_list_C.append(box_data_C)

        for unit, performance in {"F": ["kW/RT", "efficiency_mean", box_data_list_F], "C": ["COP", "COP_ref_mean", box_data_list_C]}.items():
            figure, ax = plt.subplots(figsize=(18, 7)) #ToDo,此处出现主纵坐标和次纵坐标的横坐标岔开一个的bug，临时解决方案是将主纵坐标最左边增加一个值
            ax.set_title("Chiller {} vs %RLA".format(performance[0])).set_fontsize(18)
            ax.set_ylabel("Running Hours%")
            ax.bar(data["cut_PLC"], 100 * data["RunhrsRate"], label="Running Hours%")
            handles_left, labels_left = ax.get_legend_handles_labels()
            ax.grid(visible=True)
            for a, b in zip(list(data["cut_PLC"])[1:], list(100 * round(data["RunhrsRate"], 2))[1:]):
                plt.text(a, b, int(b), ha='center', va='bottom', fontsize=15)
            ax.set_xticklabels(data["cut_PLC"].to_list(), rotation=20)
            ax.set_xlabel("%RLA")
            ax_right = ax.twinx()
            ax_right.grid(visible=False)
            ax_right.set_ylabel("Chiller %s" % performance[0])
            ax_right.boxplot(performance[2],
                             showbox=True,  # 显示箱子与否
                             widths=(0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3),  # 箱子宽度设置
                             boxprops={'color': 'white', 'linewidth': 1, 'linestyle': '-', "alpha": 0.001},  # 箱子样式设置
                             showfliers=False,  # 不显示离群值
                             # showmeans=True, #平均值以点的形式显示
                             showcaps=True,  # 显示箱须，箱线图顶端和末端的两条线
                             capprops={'color': 'black', 'linewidth': 2, 'linestyle': '-'},  # 箱须格式
                             whiskerprops={'color': 'red', 'linewidth': 1},
                             medianprops={"color": "white", "linewidth": 0},  # 设置中位数的样式
                             )
            ax_right.boxplot(performance[2],
                             showbox=True,  # 显示箱子与否
                             widths=(0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001),  # 箱子宽度设置
                             boxprops={'color': 'red', 'linewidth': 1, 'linestyle': '-'},  # 箱子样式设置
                             showfliers=False,  # 不显示离群值
                             # showmeans=True, #平均值以点的形式显示
                             showcaps=True,  # 显示箱须，箱线图顶端和末端的两条线
                             capprops={'color': 'black', 'linewidth': 2, 'linestyle': '-'},  # 箱须格式
                             whiskerprops={'color': 'red', 'linewidth': 1},
                             medianprops=dict(linewidth=0))
            ax_right.plot(data.index, data[performance[1]], marker=".", color="blue", markersize=10,
                          label="Chiller %s Average" % performance[0])
            for a, b in zip(list(data.index), data[performance[1]].to_list()):
                plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
            handles_right, labels_right = ax_right.get_legend_handles_labels() #获取左右纵坐标的legend
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width*0.8, box.height])  #将ax坐标轴往左压缩，留下放legend的空间
            plt.legend(handles=[handles_left[0], handles_right[0]], bbox_to_anchor=(1.07, 0.89), loc=3, borderaxespad=0,
                       prop={'size': 12}) #双纵坐标时legend显示在一起，并在画布外显示
            ax_right.set_xticklabels(["30-40", "40-50", "50-60", "60-70", "70-80", "80-90", ">90"], rotation=30)
            plt.savefig(self.GetData.box_performance_RLA_path[0:-4] + "_" + unit + "." + self.GetData.box_performance_RLA_path.split(".")[-1])
            plt.close()

    def draw_performance_Ton_box(self, dis_Ton_df): #for chiller replacement
        """TODO：此处有一个bug：箱线图和柱状图横坐标对不上，怀疑是pandas和python版本导致，后续更新版本后可以再测试"""
        #临时解决方案为给主纵坐标最左边增加一个值
        dis_Ton_df.loc[-1] = [0] * len(dis_Ton_df.columns)
        dis_Ton_df.sort_index(inplace=True)
        dis_Ton_df.reset_index(inplace=True, drop=True)
        dis_Ton_df.loc[0, ["RunhrsRate", "Efficiency_all_current_mean"]] = [0, 0]
        box_data_F = {}
        box_data_C = {}
        for label in list(dis_Ton_df["cut_Ton"][1:]):
            box_data_F[label] = list(self.GetData.data[self.GetData.data["cut_Ton"] == label]["Efficiency_all_current"])
            box_data_C[label] = list(self.GetData.data[self.GetData.data["cut_Ton"] == label]["COP_all_current"])
        for unit, performance in {"F": ["kW/RT", "Efficiency_all_current_mean", box_data_F], "C": ["COP", "COP_ref_mean", box_data_C]}.items():
            figure, ax = plt.subplots(figsize=(14, 9))
            ax.set_title("Chiller {} vs Cooling Load(RT)".format(performance[0])).set_fontsize(18)
            ax.set_ylabel("Running Hours%")
            ax.bar(dis_Ton_df.index, 100 * dis_Ton_df["RunhrsRate"], label="Running Hours%")
            ax.grid(visible=True)
            # ax.set_xticklabels([0] + dis_Ton_df["cut_Ton"].to_list())
            ax.set_xlabel("Cooling Load(RT)")
            handles_left, labels_left = ax.get_legend_handles_labels()
            for a, b in zip(list(dis_Ton_df.index)[1:], list(100 * (round(dis_Ton_df["RunhrsRate"], 2)))[1:]):
                plt.text(a, b, int(b), ha='center', va='bottom', fontsize=15)

            ax_right = ax.twinx()
            ax_right.set_ylabel("Chiller %s" % performance[0])
            ax_right.grid(visible=False)
            plt.boxplot(list(performance[2].values()), labels=list(performance[2].keys()),
                        showbox=True,  # 显示箱子与否
                        widths=tuple([0.3]*len(list(performance[2].values()))),  # 箱子宽度设置
                        boxprops={'color': 'white', 'linewidth': 1, 'linestyle': '-', "alpha": 0.001},  # 箱子样式设置
                        showfliers=False,  # 不显示离群值
                        # showmeans=True, #平均值以点的形式显示
                        showcaps=True,  # 显示箱须，箱线图顶端和末端的两条线
                        capprops={'color': 'black', 'linewidth': 2, 'linestyle': '-'},  # 箱须格式
                        whiskerprops={'color': 'red', 'linewidth': 1},
                        medianprops={"color": "white", "linewidth": 0},  # 设置中位数的样式
                        )
            plt.boxplot(list(performance[2].values()), labels=list(performance[2].keys()),
                        showbox=True,  # 显示箱子与否
                        widths=tuple([0.001]*len(list(performance[2].values()))),  # 箱子宽度设置
                        boxprops={'color': 'red', 'linewidth': 1, 'linestyle': '-'},  # 箱子样式设置
                        showfliers=False,  # 不显示离群值
                        # showmeans=True, #平均值以点的形式显示
                        showcaps=True,  # 显示箱须，箱线图顶端和末端的两条线
                        capprops={'color': 'black', 'linewidth': 2, 'linestyle': '-'},  # 箱须格式
                        whiskerprops={'color': 'red', 'linewidth': 1},
                        medianprops=dict(linewidth=0))
            ax_right.plot(dis_Ton_df.index[1:], dis_Ton_df[performance[1]].to_list()[1:], marker=".", color="blue", markersize=10,
                    label="Chiller %s Average" % performance[0])
            for a, b in zip(list(dis_Ton_df.index), dis_Ton_df[performance[1]].to_list()):
                plt.text(a, b, round(b, 2), ha='center', va='bottom', fontsize=15)
            handles_right, labels_right = ax_right.get_legend_handles_labels() #获取左右纵坐标的legend
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
            plt.legend(handles=[handles_left[0], handles_right[0]], bbox_to_anchor=(1.07, 0.89), loc=3, borderaxespad=0,
                       prop={'size': 12})  # 双纵坐标时legend显示在一起，并在画布外显示
            ax.set_xticklabels(list(dis_Ton_df["cut_Ton"])[1:], rotation=30)
            plt.savefig(self.GetData.box_performance_Ton_path[0:-4] + "_" + unit + "." + self.GetData.box_performance_Ton_path.split(".")[-1])
            plt.close()



    def draw_year_data(self, data_dict): #for chiller replacement
        for year, value in data_dict.items():
            data = value.replace("-", 0)
            #横坐标为月份，主纵坐标为冷冻水和冷却水温度（折线），次纵坐标为冷吨, 英制与公制分别画一张图
            for key, value in {"C": ["LCW", "ECDW"], "F": ["LCW_F", "ECDW_F"]}.items():
                figure, ax = plt.subplots(figsize=(15, 7))
                ax.grid(visible=True)
                ax.set_title(f"Temperature(°{key}) vs Cooling load, RT - {year}").set_fontsize(18)
                ax.set_ylabel(f"Temperature(°{key})")
                ax.plot(data.index, data[value[0]].to_list(), label=f"Average Leaving Chilled water temperature °{key}")
                ax.plot(data.index, data[value[1]].to_list(), label=f"Average Entering Condenser water temperature °{key}")
                for a, b in zip(list(data.index), data[value[0]].to_list()):
                    plt.text(a, b, b, ha='center', va='bottom', fontsize=13)
                for a, b in zip(list(data.index), data[value[1]].to_list()):
                    plt.text(a, b, b, ha='center', va='bottom', fontsize=13)
                ax.set_xticks(list(data.index))
                handles_left, labels_left = ax.get_legend_handles_labels()  # 获取legend
                ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=30)
                ax_right = ax.twinx()
                ax_right.grid(visible=False)
                ax_right.set_ylabel("Cooling Load, RT")
                ax_right.set_ylim(0, 3*data["Ton"].max())
                ax_right.bar(data.index, data["Ton"].to_list(), label="Average Cooling load, RT")

                for a, b in zip(list(data.index), data["Ton"].to_list()):
                    plt.text(a, b, int(b), ha='center', va='bottom', fontsize=13)
                handles_right, labels_right = ax_right.get_legend_handles_labels() #获取左右纵坐标的legend
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
                plt.legend(handles=[handles_left[0], handles_left[1], handles_right[0]], bbox_to_anchor=(1.07, 0.89), loc=3, borderaxespad=0, prop={'size': 12})
                plt.savefig((".").join(self.GetData.year_month_avg_T_Ton_path.split(".")[0:-1]) + "_" + str(year) + key + ".png")

            #横坐标为月份，主纵坐标为chiller effiency（折线），次纵坐标为chiller energy consumption，kWh, 英制与公制分别画一张图
            for key, value in {"C": ["COP_ref", "COP", "LCW", "ECDW"], "F": ["Efficiency_all_current", "efficiency, kW/RT", "LCW_F", "ECDW_F"]}.items():
                figure, ax = plt.subplots(figsize=(14, 7))
                ax.grid(visible=True)
                ax.set_title(f"Chiller {value[1]} vs Chiller energy consumption,kWh- {year}").set_fontsize(18)
                ax.set_ylabel(f"Chiller {value[1]}")
                ax.plot(data.index, data[value[0]].to_list(), label=f"Average Chiller {value[1]}")
                for a, b in zip(list(data.index), data[value[0]].to_list()):
                    plt.text(a, b, b, ha='center', va='bottom', fontsize=13)
                handles_left, labels_left = ax.get_legend_handles_labels()  # 获取legend
                ax.set_xticks(list(data.index))
                ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=30)
                ax_right = ax.twinx()
                ax_right.grid(visible=False)
                ax_right.set_ylabel("Chiller energy consumption, kWh")
                ax_right.set_ylim(0, 1.5 * data["Energy/kWh"].max())
                ax_right.bar(data.index, data["Energy/kWh"].to_list(), label="Chiller energy consumption, kWh")
                for a, b in zip(list(data.index), data["Energy/kWh"].to_list()):
                    plt.text(a, b, format(int(b), ","), ha='center', va='bottom', fontsize=13)
                handles_right, labels_right = ax_right.get_legend_handles_labels() #获取左右纵坐标的legend
                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
                plt.legend(handles=[handles_left[0], handles_right[0]], bbox_to_anchor=(1.1, 0.89), loc=3, borderaxespad=0,
                           prop={'size': 12})
                plt.savefig((".").join(self.GetData.year_month_avg_effi_energy_path.split(".")[0:-1]) + "_" + str(year) + key + ".png")

            #横坐标是月份，主纵坐标是Cooling load,RT, 次纵坐标为Chiller power consumption,kW
            figure, ax = plt.subplots(figsize=(14, 7))
            ax.grid(visible=True)
            ax.set_title("Cooling load, RT vs Chiller power consumption,kW - {}".format(year)).set_fontsize(18)
            ax.set_ylabel("Cooling load, RT")
            ax.plot(data.index, data["Ton"].to_list(), label="Average Cooling load, RT")
            ax.set_ylim(0, )
            for a, b in zip(list(data.index), data["Ton"].to_list()):
                plt.text(a, b, int(b), ha='center', va='bottom', fontsize=13)
            handles_left, labels_left = ax.get_legend_handles_labels()  # 获取legend
            ax.set_xticks(list(data.index))
            ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                               rotation=30)
            ax_right = ax.twinx()
            ax_right.grid(visible=False)
            ax_right.set_ylabel("Chiller power consumption, kW")
            ax_right.set_ylim(0, 1.5*data["Power"].max())
            ax_right.bar(data.index, data["Power"].to_list(), label="Chiller power consumption, kW")
            for a, b in zip(list(data.index), data["Power"].to_list()):
                plt.text(a, b, int(b), ha='center', va='bottom', fontsize=13)
            handles_right, labels_right = ax_right.get_legend_handles_labels() #获取左右纵坐标的legend
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])  # 将ax坐标轴往左压缩，留下放legend的空间
            plt.legend(handles=[handles_left[0], handles_right[0]], bbox_to_anchor=(1.07, 0.89), loc=3, borderaxespad=0,
                       prop={'size': 12})
            plt.savefig((".").join(self.GetData.year_month_avg_Ton_power_path.split(".")[0:-1]) + "_" + str(year) + ".png")

    def image_border(self, src, dst, loc='a', width=3, color=(0, 0, 0)):
        '''
        src: (str) 需要加边框的图片路径
        dst: (str) 加边框的图片保存路径
        loc: (str) 边框添加的位置, 默认是'a'(
            四周: 'a' or 'all'
            上: 't' or 'top'
            右: 'r' or 'rigth'
            下: 'b' or 'bottom'
            左: 'l' or 'left'
        )
        width: (int) 边框宽度 (默认是3)
        color: (int or 3-tuple) 边框颜色 (默认是0, 表示黑色; 也可以设置为三元组表示RGB颜色)
        '''
        # 读取图片
        img_ori = Image.open(src)
        w = img_ori.size[0]
        h = img_ori.size[1]
        # 添加边框
        if loc in ['a', 'all']:
            w += 2 * width
            h += 2 * width
            img_new = Image.new('RGB', (w, h), color)
            img_new.paste(img_ori, (width, width))
        elif loc in ['t', 'top']:
            h += width
            img_new = Image.new('RGB', (w, h), color)
            img_new.paste(img_ori, (0, width, w, h))
        elif loc in ['r', 'right']:
            w += width
            img_new = Image.new('RGB', (w, h), color)
            img_new.paste(img_ori, (0, 0, w - width, h))
        elif loc in ['b', 'bottom']:
            h += width
            img_new = Image.new('RGB', (w, h), color)
            img_new.paste(img_ori, (0, 0, w, h - width))
        elif loc in ['l', 'left']:
            w += width
            img_new = Image.new('RGB', (w, h), color)
            img_new.paste(img_ori, (width, 0, w, h))
        else:
            pass
        # 保存图片
        img_new.save(dst)


if __name__ == "__main__":
    projectname = "北美家用"
    chillertype = '19XR'
    chillerSN = '1107Q73751'
    connect_date = "2020-06-13"
    ton = float(666)
    COP = float(6)
    tariff = float(0)
    invest = float(0)
    fill = "no_fill"
    language = 0  # 0为EN，1为CN

    from Report.GetData import GetData
    GetData_obj = GetData(chillertype, chillerSN, ton, COP,fill, tariff, invest, language)

    GetData_obj.set_path("..")
    GetData_obj.get_word_path("VFD Retrofit Template", "VFD")
    GetData_obj.get_data_path()
    GetData_obj.get_language()

    dis_data = GetData_obj.dis_PLC_df()
    DrawFigs_obj = DrawFigs(GetData_obj)
    DrawFigs_obj.draw_from_plot_config(dis_data)