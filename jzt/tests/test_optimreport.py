# -*-    coding:utf-8       -*-
from jzt.optimreport import *
import pytest


def test_readJztOptimReportFile():
    fileName = r"..\data\Test_optimReport_Custom.txt"
    data = readJztOptimReportFile(fileName)
    print(data.head())
    print(data.index)
    print(data.columns)
    #assert data.shape[1]==3

def test_readJztOptimReportFile2():
    fileName = r"..\data\Test_optimReport_Custom.txt"
    data = readJztOptimReportFile2(fileName)
    print(data.head())
    print(data.index)
    print(data.columns)
    #assert data.shape[1]==3

def test_jztOptimReportTable():
    fileName = r"..\data\Test_optimReport_Normal.txt"
    obj = jztOptimReportTable(fileName)
    print(obj.showConfig())
    newconfig={
            "序号": 8,
            "计算参数": 13,
            "利润率": 13,
            "年回报": 13,
            "胜率": 11,
            "交易数": 10,
            "成功率": 13,
            "最大回撤": 15,
            "MAR比率": 11
        }
    obj.updateConfig(newconfig)
    data = obj.read(dropUseless=False)
    #assert data.shape[1]==9
    print(data.head())

def test_jztOptimReportTable2():
    fileName = r"..\data\Test_optimReport_Custom.txt"
    # 读取带有自定义表头的文件
    newconfig = {"最大连盈": 8}
    obj = jztOptimReportTable(fileName)
    #jzt = jztOptimReportTable(fileName, colWidthDict=colWidthdicts)
    print(obj.showConfig())
    obj.updateConfig(newconfig)
    data = obj.read(dropUseless=False)
    #assert data.shape[1]==9
    print(data.head())


#     