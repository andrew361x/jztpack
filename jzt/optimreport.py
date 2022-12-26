# -*-    coding:utf-8       -*-

import os
import os.path
import shutil
from collections import OrderedDict
from datetime import datetime

import numpy as np
import pandas as pd
from openpyxl import load_workbook

from .utils.ExcelImg import     jztProReportPicture
from .utils.common   import convertXls2Xlsx
from operator import itemgetter

getShortLength = itemgetter(0)
getLongLength = itemgetter(1)
#getShortLength = lambda x:int(x[0])
#getLongLength = lambda x:int(x[1])

def readJztOptimReportFile(filename,
                           generatorShortLong=True,
                           removeShortGtLong=True,
                           dropUseless=True,
                           sortByParm=True):
    """读取金字塔优化报告,更高效，支持自定义字段"""
    fileObj = open(filename)
    # delim_whitespace是个新特性，很好用
    data = pd.read_csv(fileObj,
                       delim_whitespace=True,
                       header=0,
                       index_col=(0, ))
    data.columns = data.columns.str.strip("(%)")

    # 金字塔的中的无穷小无穷大需要替换成numpy的inf
    data.replace('-1.#J%', -np.inf, inplace=True)
    data.replace('1.#J%', np.inf, inplace=True)

    #先删除交易数为0的参数，没有交易就没有价值
    data = data[data['交易数'] > 0]

    data["计算参数"] = [i.strip('()') for i in data["计算参数"]]
    data["利润率"] = data["利润率"].str.strip("%").astype(float) / 100.
    data["胜率"] = data["胜率"].str.strip("%").astype(float) / 100.

    if dropUseless:
        data.drop([u'年回报', u'成功率', u'最大回撤', u'MAR比率'], axis=1, inplace=True)
    else:
        data["年回报"] = data["年回报"].str.strip("%").astype(float) / 100.
        data["成功率"] = data["成功率"].str.strip("%").astype(float) / 100.
        data["最大回撤"] = data["最大回撤"].str.strip("%").astype(float) / 100.

    if generatorShortLong:
        data["tmp"] = [i.split(',', 2)[:2] for i in data["计算参数"]]
        data["Short"] = data["tmp"].map(getShortLength)
        data["Long"] = data["tmp"].map(getLongLength)
        data.drop('tmp', axis=1, inplace=True)

    if removeShortGtLong:
        data = data[data["Short"] < data["Long"]]

    if sortByParm:
        data.sort_values("计算参数", inplace=True)

    return data


def readJztOptimReportFile2(filename,
                            generatorShortLong=True,
                            removeShortGtLong=True,
                            dropUseless=True,
                            sortByParm=True):
    """读取金字塔优化报告,更高效，支持自定义字段"""
    fileObj = open(filename)
    # delim_whitespace是个新特性，很好用
    data = pd.read_csv(fileObj,
                       delim_whitespace=True,
                       header=0,
                       index_col=(0, ))
    data.columns = data.columns.str.strip("(%)")

    # 金字塔的中的无穷小无穷大需要替换成numpy的inf
    data.replace('-1.#J%', -np.inf, inplace=True)
    data.replace('1.#J%', np.inf, inplace=True)

    #先删除交易数为0的参数，没有交易就没有价值
    data = data[data['交易数'] > 0]

    data["计算参数"] = [i.strip('()') for i in data["计算参数"]]
    data["利润率"] = [float(str(i).replace("%", "")) / 100. for i in data["利润率"]]
    data["胜率"] = [float(str(i).replace("%", "")) / 100. for i in data["胜率"]]

    if dropUseless:
        data.drop([u'年回报', u'成功率', u'最大回撤', u'MAR比率'], axis=1, inplace=True)
    else:
        data["年回报"] = [
            float(str(i).replace("%", "")) / 100. for i in data["年回报"]
        ]
        data["成功率"] = [
            float(str(i).replace("%", "")) / 100. for i in data["成功率"]
        ]
        data["最大回撤"] = [
            float(str(i).replace("%", "")) / 100. for i in data["最大回撤"]
        ]

    if generatorShortLong:
        #data["tmp"] = data["计算参数"].str.split(",", 2)[:2]
        data["tmp"] = [i.split(',', 2)[:2] for i in data["计算参数"]]
        data["Short"] = [int(x[0]) for x in data["tmp"]]
        data["Long"] = [int(x[1]) for x in data["tmp"]]
        data.drop('tmp', axis=1, inplace=True)
    if removeShortGtLong:
        data = data[data["Short"] < data["Long"]]

    if sortByParm:
        data.sort_values("计算参数", inplace=True)

    return data


class jztOptimReportTable:
    """封装金字塔优化报告数据的接口"""
    def __init__(self, fileName=None, colWidthDict=None):
        """初始化 变量"""
        self._fileName = fileName
        self._widthDict = OrderedDict({
            "序号": 10,
            "计算参数": 13,
            "利润率": 13,
            "年回报": 13,
            "胜率": 11,
            "交易数": 10,
            "成功率": 13,
            "最大回撤": 15,
            "MAR比率": 11
        })

        if not colWidthDict is None:
            self._widthDict.update(colWidthDict)

    def showConfig(self):
        print(self._widthDict)

    def updateConfig(self, config):
        self._widthDict.update(config)

    def read(self,
             generatorShortLong=True,
             removeShortGtLong=True,
             dropUseless=True):
        """ 读取金字塔优化报告表格
        默认表头:序号      计算参数         利润率(%)    年回报(%)    胜率(%)    交易数    成功率(%)    最大回撤(%)    MAR比率
        默认宽度:序号:10,计算参数:17,利润率(%):13,年回报(%):13,胜率(%):11,交易数:10,成功率(%):13,最大回撤(%):15,MAR比率:11
        """
        _names = list(self._widthDict.keys())
        _widths = list(self._widthDict.values())
        fh = open(self._fileName)
        data = pd.read_fwf(fh,
                           widths=_widths,
                           names=_names,
                           encoding="GB2312",
                           skiprows=(0, ))
        data["序号"] = [int(i) for i in data["序号"]]
        data["计算参数"] = [i.strip().strip('()') for i in data["计算参数"]]
        data["利润率"] = [float(i.replace("%", "")) / 100. for i in data["利润率"]]
        data["年回报"] = [float(i.replace("%", "")) / 100. for i in data["年回报"]]
        data["胜率"] = [float(i.replace("%", "")) / 100. for i in data["胜率"]]
        data["交易数"] = [int(i) for i in data["交易数"]]
        data["成功率"] = [float(i.replace("%", "")) / 100. for i in data["成功率"]]
        data["最大回撤"] = [float(i.replace("%", "")) / 100. for i in data["最大回撤"]]
        data["MAR比率"] = [float(i) / 100. for i in data["MAR比率"]]

        if dropUseless:
            data.drop([u'年回报', u'成功率', u'最大回撤', u'MAR比率'],
                      axis=1,
                      inplace=True)

        if generatorShortLong:
            #data["tmp"] = data["计算参数"].str.split(",", 2)[:2]
            data["tmp"] = [i.split(',', 2)[:2] for i in data["计算参数"]]
            data["Short"] = data["tmp"].map(lambda x: int(x[0]))
            data["Long"] = data["tmp"].map(lambda x: int(x[1]))
            data.drop('tmp', axis=1, inplace=True)

        if removeShortGtLong:
            data = data[data["Short"] < data["Long"]]
        return data