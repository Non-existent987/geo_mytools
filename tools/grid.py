import pandas as pd
import geopandas as gpd
# import os
# import re
# import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Pool
import mytools
from shapely.geometry import Polygon,Point
from geographiclib.geodesic import Geodesic

def ppp(changjing_polygon):
    min_lon,min_lat,max_lon,max_lat=changjing_polygon
    tu = Polygon([(min_lon,min_lat),(max_lon,min_lat),(max_lon,max_lat),(min_lon,max_lat),(min_lon,min_lat)])
    return tu

def __fwjuli(lonlat=['lon','lat'],juli = 70):
    lon,lat = lonlat
    list_lonlat = []
    p_1=Geodesic.WGS84.Direct(lat, lon, 45, juli)
    p_2=Geodesic.WGS84.Direct(lat, lon, 225, juli)
    max_lon = p_1['lon2']
    max_lat = p_1['lat2']
    min_lon = p_2['lon2']
    min_lat = p_2['lat2']
    tu2 = [(min_lon,min_lat),(max_lon,min_lat),(max_lon,max_lat),(min_lon,max_lat),(min_lon,min_lat)]
    tu = Polygon([(min_lon,min_lat),(max_lon,min_lat),(max_lon,max_lat),(min_lon,max_lat),(min_lon,min_lat)])
    return tu
def read_ttt(coverage='G:/1-规划/图层/全省区域规划图层20180510/全省区域规划图层20180510/全省区域规划图层20180510.TAB'):
    changjing = gpd.read_file(coverage,encoding = 'gbk')
    changjing_use = changjing.loc[(changjing['区域类型'].isin (['主城区','一般城区','县城'])) | (changjing['地市名称']=='武汉')]
    changjing_use = changjing_use.reset_index(drop=True)
    changjing_polygon = changjing_use.total_bounds
    changjing_polygon = ppp(changjing_polygon)
    return changjing_use,changjing_polygon




def go(name):
    kong_data = pd.DataFrame()
    kong_name = ''
    print(name,'读取数据开始')
    data_t = pd.read_csv(name,header=None,encoding='gbk')
    print(name,'读取数据完成')
    data_t.columns = ['id','lat','lon']
    data_t_p = mytools.gisn.add_points(data_t,'lon','lat')
    data_t_p_polygon = data_t_p.total_bounds
    data_t_p_polygon = ppp(data_t_p_polygon)
    changjing_use,changjing_polygon = read_ttt()
    a = data_t_p_polygon.intersection(changjing_polygon)
    if a:
        print(name,'开始相交')
        data_sjoin = gpd.sjoin(data_t_p,changjing_use)
        print(name,'完成相交')
        return data_sjoin
    else:
        return kong_data



if __name__ == '__main__' :
    p = multiprocessing.Pool(processes = 6)
    names = list()
    data_res2 = pd.DataFrame()
    f = mytools.othern.file_name_paths(path='G:/1-规划/图层/栅格/亿阳算法的全省100米栅格/',find=None,case_sensitive=False)
    for name_2 in f:
        print(name_2,'开始')
        data_linshi_t = p.apply_async(go,args =(name_2,))
        aaaa = data_linshi_t.get()
        print(aaaa.shape)
        data_res2.append(aaaa)
        print(name_2,'结束')
    # print([x for x in names])
    # data_res2.to_csv('d:/grid_2020.csv')
    p.close()
    p.join()
    data_res2.to_csv('d:/gogogo.csv')
