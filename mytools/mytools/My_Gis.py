# encoding='utf-8'
import geopandas as gpd
from shapely.ops import unary_union
from shapely.geometry import Polygon,Point,LineString,MultiPolygon
from shapely import wkt
import pandas as pd
import numpy as np
import math
from geographiclib.geodesic import Geodesic
'''
度，如要转换成米，需要乘以(地球半径6371000*PI/180)
如果要用米转为为度 则反过来 *180/(6371000*PI)
'''
tab = "MapInfo File"  #".tab"
geojson ="GeoJSON"  #".geojson"
shp = "ESRI Shapefile"
class MyTools_gis(object):
    # def __init__(self):

    def quadrat_cut_geometry(self,geometry, quadrat_width, min_num=3, buffer_amount=1e-9):
        """
        将一个多边形或多个多边形分割成具有指定大小的子多边形
        参数
        ----------
        geometry : shapely.geometry.Polygon 或者 shapely.geometry.MultiPolygon
            将一个多边形或多个多边形分割成具有指定大小的子多边形。参数
        quadrat_width : 数字
            用于分割几何图形的样方的线性宽度(即几何图形所在的单位)。
        min_num : 整数（不修改）
            最小的线性样条线数(例如，最小数字-3表示4个正方形的样条网格，暂时不修改)
        缓冲量:numerid
            缓冲网格的四分格线由四分格宽度乘以缓冲量
            返回
        -------
        multipoly : shapely.geometry.MultiPolygon
        """
        # 在最小和最大x和y界限之间创建n个均匀间隔的点
        west, south, east, north = geometry.bounds
        x_num = math.ceil((east - west) / quadrat_width) + 1
        y_num = math.ceil((north - south) / quadrat_width) + 1
        x_points = np.linspace(west, east, num=max(x_num, min_num))
        y_points = np.linspace(south, north, num=max(y_num, min_num))

        # 在每一个均匀间隔的点上创建一个矩形网格
        vertical_lines = [LineString([(x, y_points[0]), (x, y_points[-1])]) for x in x_points]
        horizont_lines = [LineString([(x_points[0], y), (x_points[-1], y)]) for y in y_points]
        lines = vertical_lines + horizont_lines

        # 缓冲每条线到距离的四边形宽度除以10亿，取它们的并，然后将几何图形切成这些四边形的碎片
        buffer_size = quadrat_width * buffer_amount
        lines_buffered = [line.buffer(buffer_size) for line in lines]
        quadrats = unary_union(lines_buffered)
        multipoly = geometry.difference(quadrats)
        return multipoly
    def box_make_kmluse(self,lon_n=114.198312,lat_n=30.630697,radius=70,lod=15000):
        res = Geodesic.WGS84.Direct(lat_n, lon_n, 45, radius)
        lon_1= res['lon2']
        lat_1= res['lat2']
        res1 = Geodesic.WGS84.Direct(lat_n, lon_n, 225, radius)
        lon_2= res1['lon2']
        lat_2= res1['lat2']
        return ([(lon_2, lat_2), (lon_2, lat_1), (lon_1, lat_1),(lon_1, lat_2),(lon_2, lat_2)])

    def read_geocsv(self,df,geometry='geometry'):
        df[geometry] = df[geometry].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'},geometry=geometry)
        return gdf
    def __fwjuli(lonlat=['lon','lat'],juli = 70):
        lon,lat = lonlat
        list_lonlat = []
        p_1=Geodesic.WGS84.Direct(lat, lon, 45, juli)
        p_2=Geodesic.WGS84.Direct(lat, lon, 225, juli)
        max_lon = p_1['lon2']
        max_lat = p_1['lat2']
        min_lon = p_2['lon2']
        min_lat = p_2['lat2']
        tu = Polygon([(min_lon,min_lat),(max_lon,min_lat),(max_lon,max_lat),(min_lon,max_lat),(min_lon,min_lat)])
        return tu
    def buffer(self,
                    df,
                    buff_float= 600 ,
                    geometry='geometry'
                    ):    
        df=df.to_crs('+proj=utm +zone=50 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        df[geometry]=df[geometry].buffer(buff_float)
        df=df.to_crs({'init': 'epsg:4326'})
        return df
    def buffer_df(self,
                        df,
                        buff_col='距离',
                        geometry='geometry'
                        ):    
        df=df.to_crs('+proj=utm +zone=50 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        df[geometry]=df[[geometry,buff_col]].apply(lambda x:x[0].buffer(x[1]),axis=1)
        df=df.to_crs({'init': 'epsg:4326'})
        return df
    def add_buffer(self,
                    df,
                    lon='CellLongitude',
                    lat='CellLatitude',
                    buff_float= 600 ,
                    geometry='geometry'
                    ):    
        df[geometry]=df[[lon,lat]].apply(lambda x:Point((x[0],x[1])),axis=1)
        df=gpd.GeoDataFrame(df,crs={'init': 'epsg:4326'},geometry=geometry)
        df=df.to_crs('+proj=utm +zone=50 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        df[geometry]=df[geometry].buffer(buff_float)
        df=df.to_crs({'init': 'epsg:4326'})
        return df
    def add_buffer_df(self,
                        df,
                        lon='CellLongitude',
                        lat='CellLatitude',
                        buff_col='距离',
                        geometry='geometry'
                        ):    
        df[geometry]=df[[lon,lat]].apply(lambda x:Point((x[0],x[1])),axis=1)
        df=gpd.GeoDataFrame(df,crs={'init': 'epsg:4326'},geometry=geometry)
        df=df.to_crs('+proj=utm +zone=50 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        df[geometry]=df[[geometry,buff_col]].apply(lambda x:x[0].buffer(x[1]),axis=1)
        df=df.to_crs({'init': 'epsg:4326'})
        return df
    def changjing_distance(self,
                            df,
                            changjing,
                            zhishi,
                            use_type='覆盖半径', # 站间距 或者 覆盖半径
                            beishu=1
                            ):
        '''添加的列为‘distance
        use_type 填写 站间距 或者 覆盖半径
        举例： df = changjing_distance(df,'场景','制式',use_type='覆盖半径'beishu=1)
        ’'''
        if use_type=='覆盖半径':
            try:
                F900 = {0:'300',1:'430',2:'430',3:'400',4:'1200',5:'2200'}
                TDD = {0:'250',1:'400',2:'400',3:'350',4:'800',5:'1000'}
                df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj] 
                         for cj , pd in zip(df[changjing],df[zhishi])]
            except:
                try:
                    F900 = {'主城区':'300','一般城区':'430','市郊':'430','县城':'400','乡镇':'1200','农村':'2200'}
                    TDD = {'主城区':'250','一般城区':'400','市郊':'400','县城':'350','乡镇':'800','农村':'1000'}
                    df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj]
                             for cj , pd in zip(df[changjing],df[zhishi])]
                except:
                    F900 = {'核心城区':'300','一般城区':'430','市郊':'430','县城':'400','乡镇':'1200','农村':'2200'}
                    TDD = {'核心城区':'250','一般城区':'400','市郊':'400','县城':'350','乡镇':'800','农村':'1000'}
                    df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj]
                             for cj , pd in zip(df[changjing],df[zhishi])]
        elif use_type=='站间距':
            try:
                F900 = {0:'450',1:'650',2:'650',3:'600',4:'1800',5:'3300'}
                TDD = {0:'400',1:'600',2:'600',3:'550',4:'1200',5:'1500'}
                df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj] 
                         for cj , pd in zip(df[changjing],df[zhishi])]
            except:
                try:
                    F900 = {'主城区':'450','一般城区':'650','市郊':'650','县城':'600','乡镇':'1800','农村':'3300'}
                    TDD = {'主城区':'400','一般城区':'600','市郊':'600','县城':'550','乡镇':'1200','农村':'1500'}
                    df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj]
                             for cj , pd in zip(df[changjing],df[zhishi])]
                except:
                    F900 = {'核心城区':'450','一般城区':'650','市郊':'650','县城':'600','乡镇':'1800','农村':'3300'}
                    TDD = {'核心城区':'400','一般城区':'600','市郊':'600','县城':'550','乡镇':'1200','农村':'1500'}
                    df['distance']= [F900[cj] if pd == 'FDD900' else TDD[cj]
                             for cj , pd in zip(df[changjing],df[zhishi])]
        else:
            raise 'use_type选择的值错误，可选为 覆盖半径 和 站间距'
        df['distance'] = pd.to_numeric(df['distance'])
        df['distance'] = df['distance'] * float(beishu)
        return df

    

    def __draw_sector_min_max(self,
                  lon=114.198312,
                  lat=30.630697,
                  azimuth=0,
                  radius_min=50,
                  radius_max=100,
                  shape_dict={
                      'beam': 120,
                      'per_degree': 10
                  },
                  **kwargs):
        """制作扇区形状，无高度

        """
        beam, per_degree = ( shape_dict['beam'],shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))

        points = []
        for azi in azimuth_list:
            res_min = Geodesic.WGS84.Direct(lat, lon, azi, radius_min)
            points.append((res_min['lon2'], res_min['lat2']))
        for azi in reversed(azimuth_list):
            res_max = Geodesic.WGS84.Direct(lat, lon, azi, radius_max)
            points.append((res_max['lon2'], res_max['lat2']))
        points.append(points[0])

        return Polygon(points)

    def __draw_sector_min_max_hasz(self,
                          lon=114.198312,
                          lat=30.630697,
                          height=5,
                          azimuth=0,
                          radius_min=50,
                          radius_max=100,
                          shape_dict={
                              'beam': 120,
                              'per_degree': 10
                          },
                          **kwargs):
        """制作扇区形状，3d  has_z就是3d

        """
        beam, per_degree = ( shape_dict['beam'],shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))
        points = []
        for azi in azimuth_list:
            res_min = Geodesic.WGS84.Direct(lat, lon, azi, radius_min)
            points.append((res_min['lon2'], res_min['lat2'], height))
        for azi in reversed(azimuth_list):
            res_max = Geodesic.WGS84.Direct(lat, lon, azi, radius)
            points.append((res_max['lon2'], res_max['lat2'], height))
        points.append(points[0])
        return Polygon(points)
    def add_sectors_min_max(self,df,
                        coords=['d_lon','d_lat','d_height','d_azimuth','d_radius_min','d_radius_max'],
                        has_z=True,
                        sec_col='geometry',
                        shape_dict={'beam': 120,'per_degree': 10},
                        **kwargs):
        """根据经纬度挂高方向角距离所在列，为df增加CRS和 geometry 列
            默认has_z=True,需要填写高度和距离，不要高度has_z=False
            shape_dict={'beam': 30,'per_degree': 10},
        """

        lon, lat,  height,azimuth,radius_min,radius_max = coords
        df = df.copy()
        if has_z: 
            df.loc[:, sec_col] = [
                self.__draw_sector_min_max_hasz(*x, shape_dict=shape_dict)
                for x in zip(df[lon], df[lat], df[height],df[azimuth], df[radius_min],df[radius_max])
            ]
        else:
            df.loc[:, sec_col] = [
                self.__draw_sector_min_max(*x,  shape_dict=shape_dict)
                for x in zip(df[lon], df[lat],df[azimuth], df[radius_min],df[radius_max])
            ]
        df = gpd.GeoDataFrame(df, crs={"init": "epsg:4326"}, geometry=sec_col)
        return df
    def maps(self,
            name='湖北地市',
            cd='g'
            ):
        if (name == '湖北地市') or (name == '湖北地图') or (name == '湖北'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/湖北省地市-边界-边界/全省地市边界/全省地市边界.shp'.format(g=cd),encoding = 'utf-8')
            city_tu = city_tu.to_crs({'init': 'epsg:4326'})
        elif (name=='湖北区县') or (name=='湖北县城') or (name=='县城') or (name=='区县'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/武汉新-县城图层/县界.TAB'.format(g=cd),encoding = 'gbk')
        elif (name=='地市区县'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/县城和地市归属图层pickle/县界.shp'.format(g=cd),encoding = 'utf-8')
        elif (name=='武汉') or (name=='武汉地图'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/武汉分公司图层20190109/武汉市区分公司区域图层201804版/武汉市区分公司区域图层201804版/武汉市区分公司区域图层201804版.TAB'.format(g=cd),encoding = 'gbk')
            city_tu = city_tu.to_crs({'init': 'epsg:4326'})
        elif (name=='场景') or (name=='changjing'):
            coverage='{g}:/1-规划/图层/全省区域规划图层20180510/全省区域规划图层20180510/全省区域规划图层20180510.TAB'.format(g=cd)
            city_tu = gpd.read_file(coverage,encoding = 'gbk')
        else:
            city_tu='名字错误：目前支持的有(湖北地市,湖北区县,武汉,场景))'
        return city_tu

    def add_points(self,
                    df,
                    lon='lon',
                    lat='lat',
                    pnt_col='geometry'
                    ):
        '''add_points(df,lon='lon',lat='lat',pnt_col='geometry'):'''
        df = df.copy()
        df[pnt_col] = [Point(x) for x in zip(df[lon], df[lat])]
        df = gpd.GeoDataFrame(df, crs={"init": "epsg:4326"}, geometry='geometry') 
        return df

    def nearest_site_one(self,data,
                 id_name_column='id',
                 lon='lon',
                 lat='lat',
                 num_min_results = 3,
                 Including_itself = False
                 ):
        '''nearest_site方法用于：查询一批位置点的最近的第N个站点，以及它的距离。
        data：一个数据表格
        id_name_column：字段-每个数据的id或者名字
        lon，lat：经纬度的字段
        num_min_results：如果查询最近的一个站点则设置为1，则为最近站点，如果为2则为第二个最近站点
        Including_itself:选True：包括自己; 选False:不包括自己（通常设置为False）
            在num_min_results=1选True的时候，最近站点为自身，距离都为0。
        例子：
        nearest_site(data,
                 id_name_column='id',lon='lon',lat='lat',
                 num_min_results = 3,Including_itself = False)
        '''
        if isinstance(num_min_results,str) | isinstance(num_min_results,float):
            print('错误：输入的num_min_results不能为字符或者小数，请输入大于0的整数')
            assert 0
        elif num_min_results<1:
            print('错误：输入的num_min_results不合理，请输入大于0的整数')
            assert 0

        data_use = data.copy()
        data_use['geometry'] = [Point(x) for x in zip(data_use[lon], data_use[lat])]
        data_zhan_pot = gpd.GeoDataFrame(data_use, crs={"init": "epsg:4326"}, geometry='geometry')
        data_zhan_pot = data_zhan_pot.reset_index(drop=True).reset_index()
        data_zhan_pot_name = data_zhan_pot[['index',id_name_column,lon,lat]]
        data_sindex = data_zhan_pot.sindex

        if Including_itself:
            data_zhan_pot['minimum_index'] = data_zhan_pot['geometry'].apply(
                lambda x: list(data_sindex.nearest(x.bounds,num_results=num_min_results))[num_min_results-1])
        else:
            data_zhan_pot['minimum_index'] = data_zhan_pot['geometry'].apply(
                lambda x: list(data_sindex.nearest(x.bounds,num_results=num_min_results+1))[num_min_results])
        data_zhan_pot = data_zhan_pot.drop(['geometry'],axis=1)
        df = data_zhan_pot.merge(
            data_zhan_pot_name,how = 'left',left_on = 'minimum_index',right_on='index',suffixes=('','_y'))
        lon1, lat1, lon2, lat2 = map(np.radians, [df[lon], df[lat], df[lon+'_y'], df[lat+'_y']])
        dis_t = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
        df['distance']= 2*np.arcsin(np.sqrt(dis_t))*6371*1000
        res = df.drop(['index_y'],axis=1)
        return res
	
	
    def min_one(self,
				data_x,
				data_y,
				lon_x='经度',lat_x='纬度',
				lon_y='经度y',lat_y='纬度y'):
        '''
        求距离A数据(df格式)中每一条数据最近的一个数据（来自B数据）
        其中两组数据的经纬度不要一样
        示例：res = min_one(data,zhan,'经度','纬度','衔接经度','衔接纬度')
        
        data_x:需要计算距离的A数据（df格式）
        data_y:计算距离所需要使用的B数据（df格式）
        lon_x：lat_x：data_x表中的经纬度列名
        lon_y：lat_y：data_y表中的经纬度列名
        '''
		#生成点gdf
        data_x_p = self.add_points(data_x,lon_x,lat_x)
        data_y_p = self.add_points(data_y,lon_y,lat_y)
        
        #匹配距离最近的数据
        data_y_p_index = data_y_p.sindex
        data_x_p['minimum_index'] = data_x_p['geometry'].apply(lambda x: list(data_y_p_index.nearest(x.bounds,num_results=1))[0])
        data_x_p = data_x_p.drop(columns='geometry')
        data_y_p = data_y_p.drop(columns='geometry')
        res = data_x_p.merge(data_y_p,how='left',left_on='minimum_index',right_index = True)
		
        #添加距离
        res1 = self.distancea_df(res,lon_x,lat_x,lon_y,lat_y)
        return res1
	
    def points_coverage_merge(self,
                                df,
                                lon='RRU经度',
                                lat='RRU纬度',
                                coverage='G:/1-规划/图层/全省区域规划图层20200110/全省区域规划图层20200110.TAB',
                                df_merge_coverage_columns=['区域类型'],
                                merge_only_right_mark='农村'
                                ):
        '''示例是给df打标场景
            df:DataFrame -- 数据表
            lon:str -- df.lon
            lat:str -- df.lat
            coverage:图层 or gpd-- 图层文件的地址，支持tab、shp、geojson
            df_merge_coverage_columns：list -- 图层中的列，可接受一个列表
            merge_only_right_mark：str -- 没有圈到的数据填充值或者标记
            注意：··如果df_merge_coverage_columns的参数大于1个那么merge_only_right_mark将不生效
        '''
        if isinstance(coverage,str):
            if 'index' in list(df.columns):
                print('df列中不能包含index列')
                assert 0
            else:
                data_use = df.reset_index(drop=True).reset_index()
                guihua = gpd.read_file(coverage)
                if guihua.crs=={"init": "epsg:4326"}:
                    pass
                else:
                    guihua = guihua.to_crs({"init": "epsg:4326"})
                data_p = self.add_points(data_use,lon,lat)
                res = gpd.sjoin(guihua,data_p)
                list_columns = df_merge_coverage_columns[:]
                list_columns.append('index')
                res_use = res[list_columns]
                res_use_ok = data_use.merge(res_use,how='left',on='index')
                if len(df_merge_coverage_columns)>1:
                    pass
                else:
                    res_use_ok.loc[res_use_ok[df_merge_coverage_columns[0]].isna(),df_merge_coverage_columns[0]]=merge_only_right_mark
                    if '规划图层' in coverage:
                        res_use_ok[df_merge_coverage_columns[0]] = res_use_ok[df_merge_coverage_columns[0]].replace({'3A景区':'农村','4A景区':'农村','5A景区':'农村','景区':'农村','热点':'乡镇'})
                res_use_ok_df = res_use_ok.drop_duplicates('index').drop(columns='index')
                return res_use_ok_df
        elif isinstance(coverage,gpd.GeoDataFrame):
            if 'index' in list(df.columns):
                print('df列中不能包含index列')
                assert 0
            else:
                data_use = df.reset_index(drop=True).reset_index()
                guihua = coverage.copy()
                if guihua.crs=={"init": "epsg:4326"}:
                    pass
                else:
                    guihua = guihua.to_crs({"init": "epsg:4326"})
                data_p = self.add_points(data_use,lon,lat)
                res = gpd.sjoin(guihua,data_p)
                list_columns = df_merge_coverage_columns[:]
                list_columns.append('index')
                res_use = res[list_columns]
                res_use_ok = data_use.merge(res_use,how='left',on='index')
                if len(df_merge_coverage_columns)>1:
                    pass
                else:
                    res_use_ok.loc[res_use_ok[df_merge_coverage_columns[0]].isna(),df_merge_coverage_columns[0]]=merge_only_right_mark
                res_use_ok_df = res_use_ok.drop_duplicates('index').drop(columns='index')
                if '区域类型' in list(guihua.columns):
                        res_use_ok_df['区域类型'] = res_use_ok_df['区域类型'].replace({'3A景区':'农村','4A景区':'农村','5A景区':'农村','景区':'农村','热点':'乡镇'})
                return res_use_ok_df

    def nearest_site(self,data,
                 id_name_column='id',
                 lon='lon',
                 lat='lat',
                 num_min_results = 3,
                 Including_itself = False,
                 juli_n = 5000
                 ):
        '''nearest_site方法用于：
        1、查询一批位置点的最近的一个点的那个点，以及它的距离。
        2、查询一批位置点的最近的n个点，以及它们的平均距离。（相当于平均站间距）
        data：一个数据表格
        id_name_column：字段-每个数据的id或者名字
        lon，lat：经纬度的字段
        num_min_results：如果查询最近的一个站点则设置为1，如果查询多个最近站点并求平均数设置>1
        Including_itself:选True：包括自己; 选False:不包括自己（通常设置为False）
            在num_min_results=1选True的时候，最近站点为自身，距离都为0。
            在num_min_results>1选True的时候最，近的一个站点距离为0，结果为两个站点的平均值。
        例子：
        nearest_site(data,
                 id_name_column='id',lon='lon',lat='lat',
                 num_min_results = 3,Including_itself = False)
        '''
        if isinstance(num_min_results,str) | isinstance(num_min_results,float):
            print('错误：输入的num_min_results不能为字符或者小数，请输入大于0的整数')
            assert 0
        elif num_min_results<1:
            print('错误：输入的num_min_results不合理，请输入大于0的整数')
            assert 0

        data_use = data.copy()
        data_use['geometry'] = [Point(x) for x in zip(data_use[lon], data_use[lat])]
        data_zhan_pot = gpd.GeoDataFrame(data_use, crs={"init": "epsg:4326"}, geometry='geometry')
        data_zhan_pot = data_zhan_pot.reset_index(drop=True).reset_index()
        data_zhan_pot_name = data_zhan_pot[['index',id_name_column,lon,lat]]
        data_sindex = data_zhan_pot.sindex

        if num_min_results==1:
            if Including_itself:
                data_zhan_pot['minimum_index'] = data_zhan_pot['geometry'].apply(
                    lambda x: list(data_sindex.nearest(x.bounds,num_results=1))[0])
            else:
                data_zhan_pot['minimum_index'] = data_zhan_pot['geometry'].apply(
                    lambda x: list(data_sindex.nearest(x.bounds,num_results=2))[1])
            data_zhan_pot = data_zhan_pot.drop(['geometry'],axis=1)
            df = data_zhan_pot.merge(
                data_zhan_pot_name,how = 'left',left_on = 'minimum_index',right_on='index',suffixes=('','_y'))
            lon1, lat1, lon2, lat2 = map(np.radians, [df[lon], df[lat], df[lon+'_y'], df[lat+'_y']])
            dis_t = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
            df['distance']= 2*np.arcsin(np.sqrt(dis_t))*6371*1000
            res = df.drop(['index_y'],axis=1)
        elif num_min_results>1:
            if Including_itself:
                three_minimum_point= data_zhan_pot['geometry'].apply(
                    lambda x: list(data_sindex.nearest(x.bounds,num_results=num_min_results)))
            else:
                three_minimum_point= data_zhan_pot['geometry'].apply(
                    lambda x: list(data_sindex.nearest(x.bounds,num_results=num_min_results+1))[1:num_min_results+1])
            data_zhan_pot = data_zhan_pot.drop(['geometry'],axis=1)
            three_minimum_point_df = pd.DataFrame(
                [x for x in three_minimum_point],columns = 
                [ 'minimum_index_'+str(y+1) for y,z in enumerate(three_minimum_point[0])])
            data_zhan_pot_minimum3 = pd.concat([data_zhan_pot,three_minimum_point_df],axis=1)
            distance_dict = dict()

            for columns_index , name in enumerate(three_minimum_point_df.columns):
                df = data_zhan_pot_minimum3.merge(
                    data_zhan_pot,how='left',left_on = name,right_on = 'index',suffixes=('','_y'))
                lon1, lat1, lon2, lat2 = map(np.radians, [df[lon], df[lat], df[lon+'_y'], df[lat+'_y']])
                dis_t = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
                name_data= 2*np.arcsin(np.sqrt(dis_t))*6371*1000
                distance_dict['distance_'+str(columns_index+1)] = name_data
            distance_dict_df = pd.DataFrame(distance_dict)
            if juli_n:
                distance_dict_df[distance_dict_df>juli_n] = 0
            distance_dict_df['mean'] = distance_dict_df.mean(axis=1)
            res = pd.concat([data_zhan_pot_minimum3,distance_dict_df],axis=1)
        res.reset_index(drop=True,inplace=True)
        return res

    


    def distancea_df(self,
                        df,
                        lon_1, 
                        lat_1, 
                        lon_2, 
                        lat_2,
                        columns_name='距离'
                        ):
        lon1, lat1, lon2, lat2 = map(np.radians, [df[lon_1], df[lat_1], df[lon_2], df[lat_2]])
        a = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
        df[columns_name] = 2*np.arcsin(np.sqrt(a))*6371*1000
        return df

    def add_area(self,
                    gdf,
                    column = '面积'
                    ):
        '''把gdf新增一列‘面积‘单位是平方米
        临时转换成
        gdf = gdf.to_crs({'init': 'epsg:32650'}) #投影坐标系WGS 84 / UTM zone 50N的ID是32650
        计算面积后转回原来的坐标系
        '''
        crs_t=gdf.crs
        gdf = gdf.to_crs({'init': 'epsg:32650'})
        gdf[column]=gdf.area
        gdf = gdf.to_crs(crs_t)
        return gdf
        
    def str_to_Polygoen(self,a):
        '''支持将113.23，30.234324 ; 113.32432,23.23432;113.2342,23.3432;
        转换成Polygon支持的格式
        使用：
		示例：
		df['居民区边界图层2'] = df['居民区边界图层'].apply(lambda x:x[:-1] if (x.endswith(';')or x.endswith) else x)
		df['geometry'] = df['居民区边界图层2'].apply(lambda x:mytools.gisn.str_to_Polygoen(x))
        '''
        list=[[float(b) for b in x.split(',')] for x in a.split(';')]
        return Polygon(list)
    
    
    #---------找lod的四个角
    def lod_lon_lat(self,lon=114.198312,lat=30.630697,radius=7000):
        """
        寻找经纬度45°和225°，距离“radius”的点并返回经纬度
        __lod_lon_lat(lon=114.198312,lat=30.630697,radius=7000)
        返回样式[114.24996532912053, 30.675333957040422, 114.1467060788554, 30.586039237766027]
        """
        points1 = []
        res = Geodesic.WGS84.Direct(lat, lon, 45, radius)
        points1.append(res['lon2'])
        points1.append(res['lat2'])
        res = Geodesic.WGS84.Direct(lat, lon, 225, radius)
        points1.append(res['lon2'])
        points1.append(res['lat2'])
        return points1

    #---------找lod的四个角
    def add_lod(self,df,lon='114.198312',lat='30.630697',radius=7000,sec_col = 'lod'):
        """
        寻找经纬度45°和225°，距离“radius”的点返回df,新增一列'lod'
        add_lod(df,lon='lon',lat='lat',radius=7000)
        """
        df.loc[:, sec_col] = [self.lod_lon_lat(x,y, radius=7000)for x,y in (df[lon], df[lat])]
        return df

    def __draw_sector_jl(self,
                  lon=114.198312,
                  lat=30.630697,
                  azimuth=0,
                  radius=100,
                  shape_dict={
                      'beam': 30,
                      'per_degree': 5
                  },
                  **kwargs):
        """制作扇区形状，无高度

        """
        beam, per_degree = ( shape_dict['beam'],shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))

        points = [(lon, lat)]
        for azi in azimuth_list:
            res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
            points.append((res['lon2'], res['lat2']))
        points.append(points[0])
        return Polygon(points)

    def __draw_sector_jl_hasz(self,
                          lon=114.198312,
                          lat=30.630697,
                          height=5,
                          azimuth=0,
                          radius=100,
                          shape_dict={
                              'beam': 30,
                              'per_degree': 5
                          },
                          **kwargs):
        """制作扇区形状，3d  has_z就是3d

        """
        beam, per_degree = ( shape_dict['beam'],shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))
        points = [(lon, lat, height)]
        for azi in azimuth_list:
            res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
            points.append((res['lon2'], res['lat2'], height))
        points.append(points[0])
        return Polygon(points)
    def add_sectors_df(self,df,
                        coords=['d_lon','d_lat','d_height','d_azimuth','d_radius'],
                        has_z=True,
                        sec_col='geometry',
                        shape_dict={'beam': 120,'per_degree': 10},
                        **kwargs):
        """根据经纬度挂高方向角距离所在列，为df增加CRS和 geometry 列
            默认has_z=True,需要填写高度和距离，不要高度has_z=False
            shape_dict={'beam': 30,'per_degree': 10},
        """
        lon, lat,  height,azimuth,radius = coords
        df = df.copy()
        if has_z: 
            df.loc[:, sec_col] = [
                self.__draw_sector_jl_hasz(*x, shape_dict=shape_dict)
                for x in zip(df[lon], df[lat], df[height],df[azimuth], df[radius])
            ]
        else:
            df.loc[:, sec_col] = [
                self.__draw_sector_jl(*x,  shape_dict=shape_dict)
                for x in zip(df[lon], df[lat],df[azimuth], df[radius])
            ]
        df = gpd.GeoDataFrame(df, crs={"init": "epsg:4326"}, geometry=sec_col)
        return df

    def __draw_sector(self,
                      lon=114.198312,
                      lat=30.630697,
                      azimuth=0,
                      shape_dict={
                          'radius': 100,
                          'beam': 30,
                          'per_degree': 10
                      },
                      **kwargs):
        """制作扇区形状，可以2d也可以3d  has_z就是3d
    
        """
        radius, beam, per_degree = (shape_dict['radius'], shape_dict['beam'],
                                    shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))

        points = [(lon, lat)]
        for azi in azimuth_list:
            res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
            points.append((res['lon2'], res['lat2']))
        points.append(points[0])
        return Polygon(points)
    def __draw_sector_hasz(self,
                      lon=114.198312,
                      lat=30.630697,
                      height=5,
                      azimuth=0,
                      shape_dict={
                          'radius': 100,
                          'beam': 30,
                          'per_degree': 10
                      },
                      **kwargs):
        """制作扇区形状，可以2d也可以3d  has_z就是3d
    
        """
        radius, beam, per_degree = (shape_dict['radius'], shape_dict['beam'],
                                    shape_dict['per_degree'])
        azimuth_list = list(
            range(
                int(azimuth - beam / 2),
                int(azimuth + beam / 2) + 1, per_degree))

        points = [(lon, lat, height)]
        for azi in azimuth_list:
            res = Geodesic.WGS84.Direct(lat, lon, azi, radius)
            points.append((res['lon2'], res['lat2'], height))
        points.append(points[0])
        return Polygon(points)

    def add_sectors(self,
                    df,
                    coords=['','','',''],
                    has_z=True,
                    sec_col='geometry',
                    shape_dict={
                        'radius': 100,
                        'beam': 30,
                        'per_degree': 10
                    },
                    **kwargs):
        """根据经纬度挂高方向角所在列，为df增加CRS和 geometry 列
        shape_dict={
                          'radius': 100,
                          'beam': 30,
                          'per_degree': 10
                      },
        Returns:
            [type] -- [description]
        """
        if coords == ['','','','']:
            coords = [self.lon, self.lat, self.height, self.azimuth]
        lon, lat, *oth = coords
        df = df.copy()
        height = oth[0]
        azimuth = oth[1]
        if has_z:
            df.loc[:, sec_col] = [
                self.__draw_sector_hasz(*x, shape_dict=shape_dict, has_z=has_z)
                for x in zip(df[lon], df[lat], df[height], df[azimuth])
            ]
        else:
            df.loc[:, sec_col] = [
                self.__draw_sector(*x, shape_dict=shape_dict, has_z=has_z)
                for x in zip(df[lon], df[lat], df[azimuth])
            ]
        df = gpd.GeoDataFrame(df, crs={"init": "epsg:4326"}, geometry=sec_col)
        return df

