import sys
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')
    # write()函数这样写，每调用一次就写到记录文件中，不需要等待程序运行结束。
    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass
import time
def tm():
    return time.strftime("%Y-%m-%d %H:%M:%S")+':'
sys.stdout = Logger('output.log', sys.stdout)
sys.stderr = Logger('output.log_file', sys.stderr)      # redirect std err, if necessary
import pandas as pd
import os
zb=0
def file_name_paths(path=r'D:\UP',
                    find=None ,
                    case_sensitive=False
                    ):
    path_collection=[]
    if case_sensitive:
        if find:
            for dirpath,dirnames,filenames in os.walk(path):
                    for file in filenames:
                            fullpath=os.path.join(dirpath,file)
                            if find in file & '~$' not in file:
                                path_collection.append(fullpath)
        else:
            for dirpath,dirnames,filenames in os.walk(path):
                    for file in filenames:
                            fullpath=os.path.join(dirpath,file)
                            if '~$' not in file:
                                path_collection.append(fullpath)
    else:
        if find:
            for dirpath,dirnames,filenames in os.walk(path):
                    for file in filenames:
                            fullpath=os.path.join(dirpath,file)
                            if find.upper() in file.upper() &  '~$' not in file.upper():
                                path_collection.append(fullpath)
        else:
            for dirpath,dirnames,filenames in os.walk(path):
                    for file in filenames:
                            fullpath=os.path.join(dirpath,file)
                            if '~$' not in file:
                                path_collection.append(fullpath)
    return path_collection

#导入小区数据
print(tm(),'导入小区数据')
f = file_name_paths(path='./输入表/')

for name in f:
    try:
        if 'LTE小区报表' in name :
            data_xqbb = pd.read_csv(name,encoding='gbk')
        if 'TDD闭锁小区' in name :
            data_bsxq = pd.ExcelFile(name)
            data_bsxq_use = data_bsxq.parse()
        if '荆州当前告警' in name :
            data_jzdqgj = pd.ExcelFile(name)
            data_jzdqgj_tdd = data_jzdqgj.parse(sheet_name = 'tdd')
            data_jzdqgj_fdd = data_jzdqgj.parse(sheet_name = 'fdd')
        if '高校小区' in name :
            data_gxxq = pd.ExcelFile(name)
            data_gxxq_use = data_gxxq.parse(sheet_name = 'Sheet1')
        if 'lll' in name :
            data_lll = pd.read_csv(name,encoding='gbk')
        if '零流量' in name :
            data_llltable = pd.ExcelFile(name)
            data_use = data_llltable.parse(sheet_name = '零流量小区')
        print(tm(),'{}导入成功'.format(name))
    except:
        print(tm(),'{}导入失败'.format(name))
        zb = 8
if zb==8:
    print(tm(),'导入数据失败，检查数据格式')
    assert 0
#判断是否为零流量
#匹配高校
print(tm(),'开始匹配高校')
data_gxxq_use.columns = ['小区CGI(*)_gxxq', '小区名称', '是否高校']
data_gxxq_use = data_gxxq_use[['小区名称', '是否高校']]
data_use=data_use[['站点名称', '小区名称', '是否零流量小区（0611）', '小区状态']]
data_use_gx = data_use.merge(data_gxxq_use,how='left',on='小区名称')
data_use_gx = data_use_gx.drop(data_use_gx.loc[data_use_gx['是否高校']=='是'].index)
data_use_gx = data_use_gx.drop(columns='是否高校')
#匹配零流量
print(tm(),'匹配lte小区表')
data_lll_use = data_lll[['小区中文名']]
data_lll_use['lll']='是'
data_lll_use.columns = ['小区名称','lll']
data_use_lll = data_use_gx.merge(data_lll_use,how='left',on='小区名称')
data_use_lll = data_use_lll.loc[data_use_lll['lll']=='是']
#匹配lte小区表
print(tm(),'匹配零流量')
data_xqbb.loc[(data_xqbb['激活状态']=='激活')&(data_xqbb['可用状态']!='正常'),'退服']='退服'
data_xqbb.loc[data_xqbb['激活状态']!='激活','去激活']='去激活'
data_xqbb_sue = data_xqbb[['小区名称','退服','去激活']]
data_use_g_q = data_use_lll.merge(data_xqbb_sue,how='left',on='小区名称')

#匹配闭锁小区
print(tm(),'匹配闭锁小区')
data_bsxq_use.loc[data_bsxq_use['administrativeState']!='UNLOCKED','去激活2']='去激活'
data_bsxq_use.loc[(data_bsxq_use['operationalState']!='ENABLED')&(data_bsxq_use['administrativeState']!='LOCKED'),'退服2']='退服'
data_bsxq_use2= data_bsxq_use[[data_bsxq_use.columns[6],'去激活2','退服2']]
data_bsxq_use2.columns = ['小区名称', '去激活2', '退服2']
data_use_bs = data_use_g_q.merge(data_bsxq_use2,how='left',on='小区名称')

#匹配告警 Problem Text
print(tm(),'匹配告警tdd')
data_jzdqgj_tdd_use = data_jzdqgj_tdd[[ '中文站点名','Problem Text']]
data_jzdqgj_tdd_use['x2'] = data_jzdqgj_tdd_use['Problem Text'].str.contains('X2')
data_jzdqgj_tdd_use2 = data_jzdqgj_tdd_use.loc[data_jzdqgj_tdd_use['x2']!=True]
data_jzdqgj_tdd_use2['告警']='告警'
data_jzdqgj_tdd_use2 = data_jzdqgj_tdd_use2[['中文站点名','告警']]
data_use_gj1 = data_use_bs.merge(data_jzdqgj_tdd_use2,how='left',left_on='站点名称',right_on='中文站点名')
print(tm(),'匹配告警fdd')
data_jzdqgj_fdd['告警2'] = '告警'
data_jzdqgj_fdd_use2 = data_jzdqgj_fdd[['告警源','告警2']]
data_use_gj2 = data_use_gj1.merge(data_jzdqgj_fdd_use2,how='left',left_on='站点名称',right_on='告警源')

#输出前整理
print(tm(),'输出前整理')
data_use_gj2['小区状态']='正常'
data_use_gj2.loc[data_use_gj2['去激活']=='去激活','小区状态']='去激活'
data_use_gj2.loc[data_use_gj2['去激活2']=='去激活','小区状态']='去激活'
data_use_gj2.loc[data_use_gj2['告警']=='告警','小区状态']='告警'
data_use_gj2.loc[data_use_gj2['告警2']=='告警','小区状态']='告警'
data_use_gj2.loc[data_use_gj2['退服']=='退服','小区状态']='退服'
data_use_gj2.loc[data_use_gj2['退服2']=='退服','小区状态']='退服'
data_use_gj2['是否零流量小区（0611）']=data_use_gj2['lll']
data_use_gj3 = data_use_gj2[['站点名称', '小区名称', '是否零流量小区（0611）', '小区状态']]

#导出数据
print(tm(),'开始导出数据')
data_use_gj3.to_csv('输出表/res{}.csv'.format(time.strftime("%Y-%m-%d_%H%M")),encoding='gbk',index=False)
print('导出数据成功')
time.sleep(5)
