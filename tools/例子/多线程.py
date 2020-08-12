# from multiprocessing import Pool
import pandas as pd
data = pd.read_csv('d:/duoxiancheng.csv',encoding='gbk')
# def yunxing(df):
#     print(df.shape)
#     df['aa']= df['摸底指标']+df['保障指标']
#     return  df

# if __name__ == '__main__':
#     with Pool(3) as p:
#         print(p.map(yunxing, [df[1] for df in data.groupby('区县') ]))


# from multiprocessing import Process

# def yunxiung(name):
#     print('hello', name)

# if __name__ == '__main__':
#     p = Process(target=yunxiung, args=('bob',))
#     p.start()
#     p.join()

# from multiprocessing import Process
# import os

# def info(title):
#     print(title)
#     print('你好:', __name__)
#     print('你好 process:', os.getppid())
#     print('你好 id:', os.getpid())

# def f(name):
#     info('程序 f')
#     print('hello', name)

# if __name__ == '__main__':
#     info('主消息 line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()


# from tqdm import tqdm
# import time
# import geopandas as gpd
# from shapely.geometry import (LinearRing, LineString, MultiLineString,
#                               MultiPoint, MultiPolygon, Point, Polygon)
# from multiprocessing import Pool
# import os
# import re
# import mgrs
# import multiprocessing
#设置变量通用名


# def yunxing(df):

#     return df
# def kaishi():
#     #创建一个空gpd
#     res_conant = pd.DataFrame()
#     for name_1 , data_t_1 in tqdm(data.groupby('区县'),ncols=70,desc = city ):
#         nn = nn +1 
#         res_t = gpd.overlay(data_t_1,city_tu_diff,how='intersection')
#         res_conant = res_conant.append(res_t)


# if __name__ == '__main__' :
#     p = multiprocessing.Pool(processes = 5)
#     p.apply_async(yunxing,args =('十堰',))
#     p.apply_async(yunxing,args =('咸宁',))

#     p.close()
#     p.join()

# from multiprocessing import Process, Lock

# def f(l, i):
#     l.acquire()
#     try:
#         print('hello world', i)
#     finally:
#         l.release()
#     return i

# if __name__ == '__main__':
#     lock = Lock()
#     a = []
#     for num in range(10):
#         a.append(Process(target=f, args=(lock, num)).start())
#     print(a)
        
from multiprocessing import Pool
import multiprocessing
import time

def f(x,name):
    x = x.dissolve(by='fenlei')
    tu_new_t = gpd.overlay(tu_new_t,x,how='difference')
    return tu_new_t

if __name__ == '__main__':
    data_z = gpd.GeoDataFrame()
    p = multiprocessing.Pool(processes = 10)
    
    for data_t in myYield(shuixi1_use_area_use):
        result = p.apply_async(f, (data_t,)) # evaluate "f(10)" asynchronously in a single process
        aa =  result.get()       
        data_z = data_z.append(aa)