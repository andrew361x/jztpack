#-*-  coding:utf8   -*-
from .utils  import ExcelImg,convertXls2Xlsx
from .formula import *
from .simplebacktest import *
from .optimreport import *
from .probacktest    import *
from .probacktest_multistrategy  import *
# 金字塔策略周期映射表
jztdatatype = {
    1: "1分钟",
    2: "5分钟",
    3: "15分钟",
    4: "30分钟",
    5: "60分钟",
    6: "日线",
    7: "周线",
    8: "月线",
    9: "年线"
}

name ='jzt'
version='0.0.2'