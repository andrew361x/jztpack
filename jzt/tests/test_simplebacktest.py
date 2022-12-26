# -*-    coding:utf-8       -*-
from jzt.simplebacktest import *
import pytest


def test_jztSimpleBacktestTradedetailTable():
    fileName = r"..\data\Test_SimpleBTTradeDetail_Normal.txt"
    obj = jztSimpleBacktestTradedetailTable(fileName)
    print(obj.showConfig())
    data = obj.read()
    assert data.shape[1]==9
    print(data.head())

def test_readJztSimpleBacktestReportTradeDetail():
    fileName = r"..\data\Test_SimpleBTTradeDetail_Normal.txt"
    data = readJztSimpleBacktestReportTradeDetail(fileName)
    print(data.head())
    print(data.index)
    print(data.columns)
    assert data.shape[1]==3
    