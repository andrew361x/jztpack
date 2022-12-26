# -*-    coding:utf-8       -*-

import pandas as pd
from collections import OrderedDict
from datetime import datetime

import numpy as np
# for   readJztSimpleBacktestReportTradeDetail
from PyQt5.QtCore import QFile, QIODevice, QTextStream


class jztSimpleBacktestTradedetailTable:
    """封装金字塔简单回测报告交易明细表格的接口"""

    def __init__(self, fileName=None, colWidthDict=None):
        """初始化 变量"""
        self._fileName = fileName
        self._widthDict = OrderedDict({
            "时间": 23,
            "名称": 10,
            "类型": 8,
            "交易价": 17,
            "交易量": 10,
            "收益": 14,
            "幅度": 23,
            "资产": 16,
            "最大回撤": 10
        })  # 因为配置中有中文，但是并没有按照两个计算，把每个字符当一个英文字符统计

        if not colWidthDict is None:
            self._widthDict.update(colWidthDict)

    def showConfig(self):
        print(self._widthDict)

    def updateConfig(self, config):
        self._widthDict.update(config)

    def read(self):
        """ 读取金字塔简单回测报告交易明细表格
        默认表头:时间                   名称           类型        交易价/成本价    交易量    收益          幅度%(不计平仓费用)    资产            最大回撤%
        默认宽度:"时间":23,"名称":15,"类型":12,"交易价":17,"交易量":10,"收益":14,"幅度":23,"资产":16,"最大回撤":10
        """
        _names = list(self._widthDict.keys())
        _widths = list(self._widthDict.values())
        fh = open(self._fileName)
        data = pd.read_fwf(fh, 
                           widths=_widths, 
                           names=_names,
                           encoding="GB2312",
                           skiprows=(0,))
        DTFORMAT = r"%Y/%m/%d %H:%M:%S"
        data["时间"] = [datetime.strptime(i, DTFORMAT) for i in data["时间"]]
        data["名称"] = [str(i.strip()) for i in data["名称"]]
        data["类型"] = [str(i) for i in data["类型"]]
        data["交易价"] = [float(i.split("/")[0]) for i in data["交易价"]]
        data["交易量"] = [int(i) for i in data["交易量"]]
        data["收益"] = [float(str(i).replace(",", "")) for i in data["收益"]]
        data["幅度"] = [float(i)/100. for i in data["幅度"]]
        data["资产"] = [float(str(i).replace(",", "")) for i in data["资产"]]
        data["最大回撤"] = [float(i) for i in data["最大回撤"]]

        return data


# %%----------------------------------------------------------------------------------------------
# 时间                   名称        类型        交易价/成本价    交易量    收益         幅度%(不计平仓费用)    资产            最大回撤%
# 2010/04/16 14:00:00    塑料连续    开多        11810            1                                                            0.00
# 2010/04/16 18:00:00    塑料连续    平多        11865/11810      1         275.00       0.47                   1,000,275.00   0.03
#  ---------------------------------------------------------------------------------------------

def readJztSimpleBacktestReportTradeDetail(fileName):
    """
    读取 时间  名称 类型  交易价  交易量 这五列数据,且只能读取这几列,早期版本功能有限
    """
    fh = QFile(fileName)
    if not fh.open(QIODevice.ReadOnly | QIODevice.Text):
        print("打开文件失败")
        return

    intext = QTextStream(fh)
    LineNo = 0  # 文本行号
    tmpNo = 0  # 交易量所在的列号
    strList = []  # 用一个QStringList保存所有字符串
    columns = []  # 这个list用来保存字符串

    while not intext.atEnd():
        line = intext.readLine()
        #print("everyLine: "+line)
        if LineNo == 0:
            tmpNo = line.index("交易量")
        # /截断交易量后面的字符串，然后把单行数据分割成list，这个字符串是带\的
        columnstmp = line[:tmpNo].split()
        # print("columnstmp:")
        print(columnstmp)
        columns.clear()

        for i in range(len(columnstmp)):

            if i == 0:  # 第一列是时间有分隔符但是不能分
                aa = columnstmp[i]
            else:
                aa = columnstmp[i].split('/')[0]
            # print("aa")
            # print(aa)
            strList.append(aa)

        LineNo += 1

    strList.insert(0, "日期")

    npdata = np.array(strList)
    npdata.shape = (-1, 5)
    data = pd.DataFrame(npdata[1:], columns=npdata[0])

    data['datetime'] = pd.to_datetime(data['日期']+' '+data['时间'])
    data.set_index('datetime', inplace=True)
    data.drop(['日期', '时间'], axis=1, inplace=True)

    data['名称'] = [str(i) for i in data['名称']]
    data['类型'] = [str(i) for i in data['类型']]
    data['交易价'] = [float(i) for i in data['交易价']]

    return data
