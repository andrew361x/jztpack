# -*-    coding:utf-8       -*-
from jzt.probacktest import *
import pytest


def test_jztProBacktestTradedetailTable():
    fileName = r"..\data\Test_ProBTTradeDetail_Normal.txt"
    obj = jztProBacktestTradedetailTable(fileName)
    print(obj.showConfig())
    data = obj.read()
    assert data.shape[1]==25
    print(data.head())
    #data.to_excel("data.xlsx")

def test_jztProBactTestXlsxFile():
    assert 1
    