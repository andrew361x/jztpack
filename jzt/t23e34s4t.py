# -*-    coding:utf-8       -*-
import pandas as pd
from collections import OrderedDict
from datetime import datetime

import numpy as np
# for   readJztSimpleBacktestReportTradeDetail
from PyQt5.QtCore import QFile, QIODevice, QTextStream

# if __name__ == "__main__":

#     fileName = "Test_optimReport_Normal.txt"

#     data2 = readJztOptimReportFile(fileName)

#     # 读取默认表头的文件
#     fileName = "Test_optimReport_Normal.txt"

#     jzt = jztOptimReportTable(fileName=fileName)
#     jzt.showConfig()
#     config = {
#         "序号": 8,
#         "计算参数": 13,
#         "利润率": 13,
#         "年回报": 13,
#         "胜率": 11,
#         "交易数": 10,
#         "成功率": 13,
#         "最大回撤": 15,
#         "MAR比率": 6
#     }
#     jzt.updateConfig(config)
#     data = jzt.read()
#     print(data.head())

#     fileName = "Test_optimReport_Custom.txt"

#     data3 = readJztOptimReportFile(fileName)

#     # 读取带有自定义表头的文件
#     fileName = "Test_optimReport_Custom.txt"
#     colWidthdicts = {"最大连盈": 8}

#     jzt = jztOptimReportTable(fileName, colWidthDict=colWidthdicts)
#     config = {
#         "序号": 10,
#         "计算参数": 17,
#         "利润率": 13,
#         "年回报": 13,
#         "胜率": 11,
#         "交易数": 10,
#         "成功率": 13,
#         "最大回撤": 15,
#         "MAR比率": 11
#     }
#     jzt.updateConfig(config)
#     jzt.showConfig()
#     data = jzt.read()
#     data["最大连盈"] = [int(i) for i in data["最大连盈"]]
#     print(data.head())

#     fileName = "Test_SimpleBTTradeDetail_Normal.txt"

#     data4 = readJztOptimReportFile(fileName)

#     # 读取默认表头的文件
#     fileName = "Test_SimpleBTTradeDetail_Normal.txt"

#     jzt = jztSimpleBacktestTradedetailTable(fileName=fileName)
#     jzt.showConfig()
#     #config = {"序号":8,"计算参数":13,"利润率":13,"年回报":13,"胜率":11,"交易数":10,"成功率":13,"最大回撤":15,"MAR比率":6}
