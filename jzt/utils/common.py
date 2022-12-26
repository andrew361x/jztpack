# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 09:21:59 2018

@author: LT004
"""
import os

import pandas as pd

import tkinter as tk
from tkinter import filedialog
import h5py
#import operator
#convertxls2xlsx 可以考虑 用pip install xls2xlsx这个库替代

def convertXls2Xlsx(fullpath):
    """通过调用win32com来将xls转化成xlsx,fullpath应使用全路径"""
    import win32com.client as win32
    excel = win32.DispatchEx("Excel.Application")

    #出现下面这两个问题的原因是,saveas时发现xlsx文件是存在的，想去覆盖它，却发现xlsx打开没有关掉，是可读的。无法覆盖################
    # 老是出现这个问题win32com.client  saveas com_error: (-2147417851, '服务器出现意外情况。', None, None)
    #com_error: (-2147352567, '发生意外。', (0, 'Microsoft Excel', '不能访问“lianyingv1_tf.xlsx”。', 'xlmain11.chm', 0, -2146827284), None)

    #excel = win32.gencache.EnsureDispatch("Excel.Application")
    # excel.DisplayAlerts = False #关掉覆盖时的对话框
    wb = excel.Workbooks.Open(fullpath)  # ,ReadOnly=True)
    # ConflictResolution:::xlLocalSessionChanges	2	总是接受本地用户所做的更改。xlOtherSessionChanges	3	总是拒绝本地用户所做的更改。xlUserResolution	1	弹出对话框请求用户解决冲突。
    # wb.SaveAs(fullpath.lower()+"x", FileFormat = 51,ConflictResolution=2)    #FileFormat = 51 is for .xlsx extension
    print("new path>>> ", fullpath.lower() + "x")
    try:
        if os.path.exists(fullpath.lower() + "x"):
            os.remove(fullpath.lower() + "x")
    except:
        pass
    wb.SaveAs(fullpath.lower() + "x", FileFormat=51)
    qWorkbook = wb.Close()
    # excel.DisplayAlerts = True                           #FileFormat = 56 is for .xls extension
    qExcel = excel.Application.Quit()
    return (qWorkbook is None) and (qExcel is None)


def getDirFolds(dirpath):
    """遍历该目录下的文件夹"""
    foldList = []
    for root, subdirs, files in os.walk(dirpath):
        for subdir in subdirs:
            foldName = os.path.join(root, subdir)
            foldList.append(foldName)
    return foldList


def getDirFiles(dirpath):
    """遍历该目录下的所有文件"""
    filefullnames = []
    for root, subdirs, files in os.walk(dirpath):
        for filepath in files:
            tmpfilename = os.path.join(root, filepath)
            filefullnames.append(tmpfilename)
    return filefullnames


###################################################################################################
#
#         使用func处理当前文件夹下的所有文件并生成所需要的dataframe原始数据
#
###################################################################################################


def readFiles(dirpath=None, func=None):
    """func 只有filename参数一个"""
    filefullnames = []  # 存储dirpath目录下的所有文件名

    mydata = pd.DataFrame()

    # 遍历该目录下的所有文件和文件夹
    filefullnames = getDirFiles(dirpath)

    # 逐个打开每个文件

    for fName in filefullnames:
        print("opening ", fName)
        newdata = func(fName)  # 默认导出的格式是dataframe
        mydata = mydata.append(newdata)
    print("finished!")
    # 由于有些天数未交易，结算单是一样的，所以要过滤掉CalculateNetPL_py3.py
    # 不管什么情况，也应该保证index是唯一不重复的
    mydata.drop_duplicates(inplace=True)
    return mydata


def askopenfilenames(initialdir):
    """使用 tkinter弹出选择多个文件的对话框"""
    root = tk.Tk()
    root.withdraw()  # 必须将窗口回收，不然就会有个窗口伫立在旁边，干都干不了
    return filedialog.askopenfilenames(initialdir=initialdir)


def getH5RootKeys(h5filename):
    """ 获取到h5文件的根目录的keys,使用dataframe.to_hdf保存的，根目录都是group，一个group对应一个dataframe"""
    f = h5py.File(h5filename, 'r')
    groupnames = list(f.keys())
    f.close()
    groupnames.sort()
    return groupnames


def shutdown(sec=None):
    smt = "shutdown /s /t " + str(sec)
    os.system(smt)


def convert_hdf5_to_csvfiles(h5filename, format='csv'):
    """目前支持一级目录,format支持csv和excel"""
    filemapping = {"csv": "csv", "excel": 'xlsx'}

    h5filename = os.path.abspath(h5filename)
    f = h5py.File(h5filename, 'r')
    groupnames = list(f.keys())
    print(groupnames)

    rootpath = os.path.splitext(os.path.abspath(h5filename))[0]
    if not os.path.exists(rootpath):
        print('creating rootpath...', rootpath)
        os.makedirs(rootpath)

    for path in groupnames:
        newpath = os.path.join(rootpath, path)
        print('creating grouppath...', newpath)
        os.mkdir(newpath)
        subgroupnames = f[path].keys()
        for subpath in subgroupnames:
            key = '/' + path + '/' + subpath
            savepath = os.path.join(rootpath, path,
                                    subpath + '.' + filemapping[format])
            print(f'reading hdf5file...,key ={key}, savepath: {savepath}')
            df = pd.read_hdf(h5filename, key=key)
            try:
                df.__getattribute__('to_' + format)(savepath)
            except:
                print("保存出现异常!!!")
    f.close()
