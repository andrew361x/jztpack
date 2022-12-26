# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd

# import json
# import  os
# import os.path

# def getcontractconfig(contractsymbols=None):
# """获取一系列合约列表的配置信息"""
# # contractCfgPath = os.path.abspath( os.path.join(os.getcwd(), "..",'files',"contractConfig.json") )
# # try:
# #     with open(contractCfgPath, encoding='utf-8') as f:
# #         cfg = json.load(f)
# #         margin = float(cfg[contractSymbol]['margin'])
# #         tradefee = float(cfg[contractSymbol]['commission'])
# #         LogInfo(f"获取{contractSymbol}的保证金:{margin} 和佣金{tradefee}")
# # except Exception as e:
# #     LogInfo(f"获取{contractSymbol}的保证金和佣金的数据 失败,因为 {e}")
# #     margin = 0.1    # 保证金 统一按照10%
# #     tradefee = 0.0  # 手续费,不收费

# margin = 0.1    # 保证金 统一按照10%
# tradefee = 0.0  # 手续费,不收费
# contractmultiple = 10  # 默认乘数为10
# isfixed = 0  # 不是固定的
# cfg = {}
# try:
# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres', echo=True)
# conn = engine.connect()
# cfg = pd.read_sql('select * from jztdata."contractConfig"; ', conn,index_col=['id']).copy().to_dict(orient="index")
# conn.close()
# except Exception as e:
# print(f"获取{contractsymbols}的保证金和佣金的数据 失败,因为 {e}")
# finally:
# deletekeys = cfg.keys()-contractsymbols  # 数据库有，而需求列表没有的，删除掉
# [cfg.pop(i) for i in deletekeys]


# addkeys = contractsymbols-cfg.keys()  # 需要列表有，数据库没有的，要添加
# print(f"数据库没有的品种列表: {addkeys},采用保证金0.1，手续费0，乘数10，isfixed固定")
# for i in addkeys:
# cfg[i] = {'commission': tradefee, 'contractmultiple': contractmultiple,
# 'margin': margin, 'isfixed': isfixed, 'name': i}
# return cfg
def getcontractconfig(contractsymbols=None):
    """获取一系列合约列表的配置信息"""
    # contractCfgPath = os.path.abspath( os.path.join(os.getcwd(), "..",'files',"contractConfig.json") )
    # try:
    #     with open(contractCfgPath, encoding='utf-8') as f:
    #         cfg = json.load(f)
    #         margin = float(cfg[contractSymbol]['margin'])
    #         tradefee = float(cfg[contractSymbol]['commission'])
    #         LogInfo(f"获取{contractSymbol}的保证金:{margin} 和佣金{tradefee}")
    # except Exception as e:
    #     LogInfo(f"获取{contractSymbol}的保证金和佣金的数据 失败,因为 {e}")
    #     margin = 0.1    # 保证金 统一按照10%
    #     tradefee = 0.0  # 手续费,不收费

    margin = 0.1  # 保证金 统一按照10%
    tradefee = 0.0  # 手续费,不收费
    contractmultiple = 10  # 默认乘数为10
    isfixed = 0  # 不是固定的
    cfg = {}
    try:
        engine = create_engine(
            'postgresql+psycopg2://postgres:0227@localhost:5432/postgres',
            echo=True)
        conn = engine.connect()
        cfg = pd.read_sql('select * from future; ',
                          conn,
                          index_col=['productid'
                                     ]).copy().to_dict(orient="index")
        conn.close()
    except Exception as e:
        print(f"获取{contractsymbols}的保证金和佣金的数据 失败,因为 {e}")
    finally:
        deletekeys = cfg.keys() - contractsymbols  # 数据库有，而需求列表没有的，删除掉
        [cfg.pop(i) for i in deletekeys]

        addkeys = contractsymbols - cfg.keys()  # 需要列表有，数据库没有的，要添加
        print(f"数据库没有的品种列表: {addkeys},采用保证金0.1，手续费0，乘数10，isfixed固定")
        for i in addkeys:
            cfg[i] = {
                'commission': tradefee,
                'contractmultiple': contractmultiple,
                'margin': margin,
                'isfixed': isfixed
            }
    return cfg