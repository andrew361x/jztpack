# -*-    coding:utf-8       -*-
from jzt.formula import *
import pytest

def test_read_formula_variable_file():
    filepath =r"..\data\formula_runing_variable_data.txt"
    data = read_formula_variable_file(filepath)
    print(data.head())
    assert data.shape!=(0,0)
