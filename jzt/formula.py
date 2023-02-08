# -*-    coding:utf-8       -*-

import pandas as pd
import numpy as np
import re
from copy import deepcopy
import autoit
import time
import pyautogui
import pyperclip
import py_win_keyboard_layout as pwkl

englishlayout=0x04090409
englistlayout_oct=67699721
chineselayout=0x08040804
chineselayout_oct=134481924

#办公室笔记本
desktop_mouseclickposition=(600,200)

current_mouseclickposition=desktop_mouseclickposition

def ensure_englishlayout():
    """
    添加英文显示语言的方法:
    windows+i 进入设置 => 时间和语言 => 语言和区域 =>首选语言添加语言 =>搜索English(United States)，安装即可
    """
    layout = pwkl.get_foreground_window_keyboard_layout()
    if  englistlayout_oct != layout:
        pwkl.change_foreground_window_keyboard_layout(englistlayout_oct)
        layout =pwkl.get_foreground_window_keyboard_layout()
    assert englistlayout_oct== layout
    if englistlayout_oct== layout:
        return True
    else:
        return False

def read_formula_variable_file(filepath:str):
    """
    读取包含金字塔的图表策略的运行变量数据的文件
    获取数据的方法:加载图表策略，选定时间后，Shift+Q,保存在demo.txt文本中
    Parameters
    ----------
    filepath : str
        DESCRIPTION.

    Returns
    -------
    pandas的dataframe.

    """
        
    df = pd.read_csv(filepath, sep=";", index_col=None, names=['text'])
    df['id']=df.index//2
    df2=df.groupby('id')['text'].apply(lambda x:' '.join(list(x))).to_frame()
    
    rec=[]
    for row in df2.iterrows():
        allrecords={}
        print(row[1])
        
        ddd=row[-1].iloc[0]
        pattern=re.compile('\<(.*?)\>',re.S)
        strs = pattern.findall(ddd)
        assert len(strs)==2
        allrecords['品种']=strs[0]
        allrecords['策略']=strs[-1]
        
        for d in strs:
            ddd=ddd.replace('<'+d+'>','')
        ddd=ddd.replace('<'+d+'>','')
        ddd=ddd.strip()
        
        ddds = ddd.split(' ')
        
        newddds =deepcopy(ddds)
        records={}
        
        for i  in ddds:
            #if i in ['00:00:00','15:00:00']:
            if ':00' in i:
                newddds.remove(i)
            #break
            if ':' in i:
                arr=i.split(':')
                arr=[ai for ai in arr if ai]
                if len(arr)==2:
                    records[arr[0]]=arr[-1]
                    newddds.remove(i)
                    
        allrecords.update(records)
                   
        newddds=[ai for ai in newddds if ai]
        
        nn=[]
        for i in newddds:
            if ':'  in i:
                arr=i.split(':')
                arr=[ai for ai in arr if ai]
                assert len(arr)==1
                nn.append(arr[0])
            else:
                nn.append(i.strip())
        
        
        narr = np.array(nn)
        narr=narr.reshape((-1,2)).T
        dff =pd.Series(narr[1],index=narr[0])
        allrecords.update(dff.to_dict())
        rec.append(allrecords)
        
    want = pd.DataFrame(rec)
    return want
    
def calibrate_mouseclick_location(x=200,y=120):
    """校准点击位置
    note:需要管理员权限
    """
    handle =autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_move(x,y)
    return autoit.mouse_click("left",x=x,y=y,clicks=2)
    

def  grap_formula_runing_variable(filepath,speed=2):
    """
    从金字塔的图表策略的抓取运行变量数据
    获取数据的方法:加载图表策略，选定时间后，Shift+Q,保存在filepath文本中
    note:需要管理员权限
    Parameters
    ----------
    filepath : str
        DESCRIPTION.

    Returns
    -------
    无返回值

    """
    if ensure_englishlayout():
        print("输入法正常")
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    for i in range(10):
        autoit.send("{DOWN}")
        time.sleep(2*speed)
        
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    pyautogui.hotkey("ctrl","end")
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    pyautogui.hotkey("shift","q")
    time.sleep(0.5*speed)
    autoit.mouse_click("left",*current_mouseclickposition)
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    pyautogui.hotkey("ctrl","a")
    time.sleep(0.5*speed )
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    pyautogui.hotkey("ctrl","c")
    time.sleep(0.5*speed )
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("{esc}")
    time.sleep(0.5*speed)
    data=pyperclip.paste()
    print(data[:35])
    with open(filepath,mode='a',encoding="utf8") as f:
        f.write('\n')
        f.write(data)
    print("end")


def grap_formula_runing_variable_batch(filepath,formula=None,product="IF00",cyclelist=["4","5","6"],speed=2):
    """依次批量抓取同一个品种的不同周期的数据
    4:30min,5:60min,6:day
    note:需要管理员权限
    """
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(product)
    autoit.send("{enter}")  #回车键
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("demo")
    autoit.send("{enter}")  #回车键
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(formula)
    autoit.send("{enter}")  #回车键
    
    for cycle in cyclelist:
        print(cycle) 
        autoit.win_activate("金字塔决策交易系统")
        autoit.mouse_click("left",*current_mouseclickposition)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send(product)
        time.sleep(0.5*speed)
        autoit.send("{enter}")  #回车键
        time.sleep(0.5*speed)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send(cycle)  
        time.sleep(0.5*speed)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send("{enter}")  #回车键
        time.sleep(0.5*speed)
        grap_formula_runing_variable(filepath,speed=speed)
        time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(chineselayout)



def grap_formula_runing_variable_batch2(filepath,subfunction=None,product="IF00",cyclelist=["4","5","6"],speed=2):
    """依次批量抓取同一个品种的不同周期的数据
    4:30min,5:60min,6:day
    note:需要管理员权限
    """
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(product)
    autoit.send("{enter}")  #回车键
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    #autoit.send("demo")
    #autoit.send("{enter}")  #回车键
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    pyautogui.hotkey("alt","F8")
    autoit.send(subfunction)
    autoit.send("{enter}")  #回车键
    
    for cycle in cyclelist:
        print(cycle) 
        autoit.win_activate("金字塔决策交易系统")
        autoit.mouse_click("left",*current_mouseclickposition)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send(product)
        time.sleep(0.5*speed)
        autoit.send("{enter}")  #回车键
        time.sleep(0.5*speed)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send(cycle)  
        time.sleep(0.5*speed)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send("{enter}")  #回车键
        time.sleep(0.5*speed)
        grap_formula_runing_variable(filepath,speed=speed)
        time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(chineselayout)


def request_historydata(product="IF00",cycle="6",speed=2):
    """
    不断请求历史数据
    """
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(product)
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("{enter}")  #回车键
    time.sleep(1*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(cycle)
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("{enter}")  #回车键

    for i in range(100):
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        pyautogui.hotkey("ctrl","home")
        time.sleep(0.5*speed)
        for j in range(5):
            pwkl.change_foreground_window_keyboard_layout(englishlayout)
            autoit.send("{LEFT}")
            time.sleep(1*speed)
            pyautogui.hotkey("left")

        for j in range(5):
            pwkl.change_foreground_window_keyboard_layout(englishlayout)
            autoit.send("{DOWN}")
            time.sleep(1*speed)
            pyautogui.hotkey("down")
        


def grap_formula_runing_variable_ZhuK(filepath,product="IF00",cycle="6",speed=2):
    """依次批量抓取同一个品种的不同周期的数据
    4:30min,5:60min,6:day
    note:需要管理员权限
    """
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(product)
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("{enter}")  #回车键
    time.sleep(1*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send(cycle)
    time.sleep(0.5*speed)
    pwkl.change_foreground_window_keyboard_layout(englishlayout)
    autoit.send("{enter}")  #回车键

    if ensure_englishlayout():
        print("输入法正常")
    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    for i in range(2000):
        autoit.send("{DOWN}")
        time.sleep(0.0001*speed)
        pyautogui.hotkey("ctrl","home")
    print("拉取数据结束")

    autoit.win_activate("金字塔决策交易系统")
    autoit.mouse_click("left",*current_mouseclickposition)
    pyautogui.hotkey("ctrl","home")
    time.sleep(0.5*speed)

    currentdate=''

    for i  in range(1000000000):

        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        pyautogui.hotkey("shift","q")
        time.sleep(1*speed)
        autoit.mouse_click("left",*current_mouseclickposition)
        time.sleep(1*speed)
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        pyautogui.hotkey("ctrl","a")
        time.sleep(0.5*speed )
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        pyautogui.hotkey("ctrl","c")
        time.sleep(0.5*speed )
        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        autoit.send("{esc}")
        time.sleep(0.5*speed)
        data=pyperclip.paste()
        
        pattern=re.compile('\<(.*?)\>',re.S)
        strs = pattern.findall(data)
        productstr = strs[0]
        datenum =data.find('时间:')
        datestr = data[datenum+3:datenum+3+17]

        if currentdate != datestr:
            currentdate =datestr
            with open(filepath,mode='a',encoding="utf8") as f:
                f.write('\n')
                f.write(data)
        else:
            break
        
        print(productstr,currentdate)

        pwkl.change_foreground_window_keyboard_layout(englishlayout)
        pyautogui.hotkey("right")
        time.sleep(0.5*speed)
