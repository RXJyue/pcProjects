# VFD Health Check & Diagnostic Tool (app ver.)

<a title="Python Version" target="_blank" href="https://www.python.org/downloads/release/python-3119/"><img src="https://img.shields.io/badge/Python-3.11-brightgreen?style=flat-square"></a>
<a title="tkinter" target="_blank" href="https://tkdocs.com/"><img src="https://img.shields.io/badge/Tkinter-%23b8ebf3?style=flat&logo=python"></a>
<a title="matplotlib" target="_blank" href="https://matplotlib.org/stable/"><img src="https://img.shields.io/badge/Matplotlib-%23b8ebf3?style=flat&logo=python"></a>
<a title="within" target="_blank"><img src="https://img.shields.io/badge/INTERNAL%20USE-red"></a>

| 项目总结    | 描述        |
|---------|-----------|
| 开始日期    | 1/1/2024  |
| 上次更新    | 4/29/2024 |
| 当前状态    | 更新中       |
| 软件开发人员  | 靳越        |

<p>
<a href="README.md">English</a> &nbsp;|&nbsp; <a href="././screenshots/prep.png">Demo</a>
</p>


## 💡 简介
VFD Health Check & Diagnostic Tool是一个基于Python的桌面应用程序，用于变频器的智能诊断，并为用户提供简约易用的UI。  
该工具使用Tkinter作为GUI框架。  

主要功能设计：    
- 数据传输与可视化
- 数据分析与智能诊断



## 🗺️ 背景

当下有越来越多的数据应用得到关注，同时基于转型升级的大背景提出该项目。值得注意的是，数据应用不仅包含获取数据，也包括将数据转换为有效的信息。  

该工具当前仅用于变频器（VFD）数据的分析和可视化。包括但不限于：  
* 变频器生命周期管理
* 变频器检修
* 变频器故障排除
* 变频器调试
* 其他潜在应用场景...


## ✨ 特性
<h4>4/8更新</h4>
* 可编辑的坐标轴
* 变量的offset与scale设置
* 缩放
* 读写操作

![page1](././screenshots/prep.png)
![page2](././screenshots/summary.png)
****

<details>
<summary>更新</summary>
<h4>3/4更新</h4>
* 概念构建
* GUI设计和布局
* 功能部件
* 多通道设置

<img alt="#1" src="././screenshots/firstreview.png" width="700" height="400" />
</details>


## 📋 目录
基于`GlobalVars`, 用户可以实现自定义组件，包括`menus`, `canvas`, `tabs`以及它们的状态。    
对于大型复杂的应用程序来说，将其拆分成多个软件包和模块更便于管理代码。    
![struct](././screenshots/contents.png)

### Components
![compo](././screenshots/components.png)  
Components包含了整个界面，和出现在界面中的元素。  
子目录是由`ttk.Notebook`实现的分页页面，以便自定义单个页面布局。  


除了tab以外，也可以对原始tk组件进行重写并应用。 例如在`widgets.py`中:  
![labelframe](././screenshots/label_frame.png)  
自定义组件时可以指定任意组件的特性，例如`text_color`, `font`等并应用到全局。 


### Functions
![func](././screenshots/functions.png)  
Functions是对部件的实际控制。


### Reports
TBA


### app.py
该部分建造了`GlobalVar`模块, 用于存储全局变量。  
`GlobalVar`有两个函数：  
* set_value: 存储变量值
* get_value: 获取变量值

**运行该文件来启动应用。**


## ▶️ 使用方法
> 以 **tab_data_prepare**页面为例。   
![prep](././screenshots/data_prepare.png) 

这个页面包含了四个分区，每个区域使用一个`LabelFrame`作为容器来添加自定义的组件。

对于每个`LabelFrame`来说，组件的位置必须被指定。  
值得注意的是Tkinter提供了三种不同的<a href="https://www.pythonguis.com/faq/pack-place-and-grid-in-tkinter/">布局管理</a>: `pack`, `grid` and `place`.

所有组件可以实例化以启用，开发者可根据自己的应用场景选择搭配。

## 🏗️ 相关文档
* <a href="https://wiki.python.org/moin/GuiProgramming">Python图形用户界面开发</a>
* <a href="https://matplotlib.org/stable/users/explain/figure/backends.html">Matplotlib中的图形底层代码</a>
* <a href="https://tcl.tk/man/tcl8.6/TkCmd/contents.htm">Tk指令</a>
* <a href="https://pillow.readthedocs.io/en/stable/reference/ImageTk.html">PIL中的ImageTK模块</a>
