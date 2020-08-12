import pandas as pd
from tqdm import tqdm
import time
import geopandas as gpd
import app.netools as an
nt = an.NetTools()
import app.mydef as md
mt = md.MyTools()
from shapely.geometry import (LinearRing, LineString, MultiLineString,
                              MultiPoint, MultiPolygon, Point, Polygon)
from multiprocessing import Pool
import os
import re
import mgrs
import multiprocessing
#设置变量通用名
print('设置变量通用名')
id = '小区CGI(*)'
lon = 'RRU经度'
lat = 'RRU纬度'
changjing = '覆盖类别'
zhishi = ' 工作频段'
fw = '方位角'
def gongcan():
    #导入数据
    print('导入数据')
    gongcan = pd.read_csv(open('g:/1-规划/工参/工参数据/ltejizhan20191107.csv',encoding = 'gbk'))
    gongcan['Z'] = gongcan['Z'].fillna('无')
    gongcan = gongcan.loc[~gongcan['Z'].str.contains('W-')]
    
    #过滤工参数据
    print('过滤工参数据')
    gongcan_loc = gongcan.loc[(gongcan[lon]>0) &  (gongcan[lat]>0) & (gongcan[fw]>0)]
    gongcan_loc[changjing] = gongcan_loc[changjing].apply(lambda x: np.NaN if str(x).isspace() else x)
    gongcan_loc.loc[gongcan_loc[changjing].isnull(),changjing]=2
    #添加覆盖距离
    print('添加覆盖距离')
    gongcan_loc_juli = mt.changjing_distance(gongcan_loc,changjing,zhishi)
    gongcan_loc_juli_columns = gongcan_loc_juli[[id,lon,lat,fw,'juli','所属地区']]
    gongcan_loc_juli_columns['cgi'] = gongcan_loc_juli_columns['小区CGI(*)']
    gongcan_loc_juli_columns['juli'] = pd.to_numeric(gongcan_loc_juli_columns['juli'])
    gongcan_loc_juli_columns['juli_2'] = gongcan_loc_juli_columns['juli'] + gongcan_loc_juli_columns['juli']
    return gongcan_loc_juli_columns
def ditu():
    city_tu = gpd.read_file('g:/1-规划/图层/湖北省地市-边界-边界/',encoding = 'gbk')
    city_tu = city_tu.to_crs({'init': 'epsg:4326'})
    city_tu = city_tu.replace('市', '', regex=True)
    city_tu['city'] = city_tu['kkk'] 
    return city_tu

def code2mgrs(city = 'dishi'):
    gongcan_loc_juli_columns = gongcan()
    city_tu = ditu()
    print(gongcan_loc_juli_columns.shape,'gongcan的行列数')
    print(city_tu.shape,'地图的行列数')
    gongcan_loc_juli_columns_1 = gongcan_loc_juli_columns.loc[gongcan_loc_juli_columns['所属地区']==city]
    city_tu_shiyong = city_tu.loc[city_tu['kkk']==city]
    #做扇区
    print(city,'做扇区')
    gongcan_s = mt.add_sectors_jl(gongcan_loc_juli_columns_1,coords=[lon, lat, 'd_height', fw, 'juli'], has_z=False, sec_col='geometry', shape_dict={'beam': 120, 'per_degree': 10})
    print(city,'扇区完成，扇区的行列数',gongcan_s.shape,gongcan_s.head(1))
    #将扇形一个地市合并成一个图
    print(city,'将扇形一个地市合并成一个图')
    gongcan_city = gongcan_s.dissolve(by = '所属地区')
    print(city,'将扇形一个地市合并成一个图-ok',gongcan_city.area,gongcan_city.head(1))
    #求与地市地图没有交集部分-覆盖空洞
    print(city,'求与地市地图没有交集部分')
    city_tu_diff = gpd.overlay(city_tu_shiyong,gongcan_city,how='difference')
    print(city,'求与地市地图没有交集部分-ok',city_tu_diff.area,city_tu_diff.head(1))
    #做弧扇区
    print(city,'做弧扇区')
    gongcan_s = mt.add_sectors_min_max(gongcan_loc_juli_columns_1, coords=[lon, lat, 'd_height', fw, 'juli', 'juli_2'], has_z=False)
    print(city,'做弧扇区-ok',gongcan_s.shape,gongcan_s.head(1))
    gongcan_s_area = mt.add_area(gongcan_s,column='扇形面积')
    print(city,'添加面积完成')
    
    print(city,'建立一个空的gpd')
    #按照cgi分组
    print(gongcan_s_area.columns)
    data_t_groupby = gongcan_s_area.groupby(by = 'cgi')
    nn = 0 
    print(city,'开始循环',gongcan_s_area.shape)
    #创建一个空gpd
    res_conant = gpd.GeoDataFrame()
    for name_1 , data_t_1 in tqdm(data_t_groupby,ncols=70,desc = city ):
        nn = nn +1 
        res_t = gpd.overlay(data_t_1,city_tu_diff,how='intersection')
        res_conant = res_conant.append(res_t)
        # if nn%2 == 0:
        #     print(city,nn)
        #     print(city,'执行了',nn)

    print('循环结束')
    res_conant_res = mt.add_area(res_conant, column='空洞面积')
    res_conant_res.to_csv(city+'.csv',encoding = 'gbk',index = False)
    print(city,'完成')

if __name__ == '__main__' :
    p = multiprocessing.Pool(processes = 4)
    p.apply_async(code2mgrs,args =('十堰',))
    p.apply_async(code2mgrs,args =('咸宁',))
    p.apply_async(code2mgrs,args =('天门',))
    p.apply_async(code2mgrs,args =('孝感',))
    p.apply_async(code2mgrs,args =('宜昌',))
    p.apply_async(code2mgrs,args =('恩施',))
    p.apply_async(code2mgrs,args =('武汉',))
    p.apply_async(code2mgrs,args =('江汉',))
    p.apply_async(code2mgrs,args =('潜江',))
    p.apply_async(code2mgrs,args =('荆州',))
    p.apply_async(code2mgrs,args =('荆门',))
    p.apply_async(code2mgrs,args =('襄阳',))
    p.apply_async(code2mgrs,args =('鄂州',))
    p.apply_async(code2mgrs,args =('随州',))
    p.apply_async(code2mgrs,args =('黄冈',))
    p.apply_async(code2mgrs,args =('黄石',))

    p.close()
    p.join()