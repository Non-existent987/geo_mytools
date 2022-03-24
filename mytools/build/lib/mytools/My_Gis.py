#!/usr/bin/env python
# coding: utf-8
import geopandas as gpd

from shapely.ops import unary_union, triangulate
from shapely.geometry import Polygon,Point,LineString,MultiPolygon, MultiPoint
from shapely import wkt
import pandas as pd
import numpy as np
import math,os,simplekml
import shapefile
import shutil
from geographiclib.geodesic import Geodesic
import kml2geojson as k2g
# from osgeo import osr
from itertools import chain
from mytools.My_Other import MyTools_other

'''
————————————————
LineString：线段
LinearRing：线环
MultiLineString


r"is_empty::对于一个空的几何图形，该值就为True"
r"is_simple::如果几何体自身不交叉，该值就为True(仅对线串--LineStrings和线环--LineRings有意义)")
r"is_valid::如果几何体是有效的，该值就为True")
test3.is_ring::如果几何体是有效的，该值就为True")
geopandas:一些属性
exterior是外边框返回‘geometry’线条格式
interiors是内边框返回‘geometry’线条格式

geo.exterior.coords #外边
[interior.coords[:-1] for interior in geo.interiors]#内边

GeoSeries.buffer(distance, resolution=16) #缓冲区
GeoSeries.boundary  #表示每个几何的集合理论边界的低维对象
GeoSeries.centroid  #几何的质心
GeoSeries.convex_hull   #建立最小多边形
GeoSeries.envelope      #建立表示包含每个对象的点或最小矩形多边形（边平行于坐标轴）的几何图形
GeoSeries.unary_union   #返回包含所有几何的并集的几何
GeoSeries.simplify      #返回GeoSeries包含每个对象的简化表示的a
GeoSeries.rotate        #旋转GeoSeries的坐标
GeoSeries.scale         #沿着每个（x，y，z）维度缩放GeoSeries的几何
GeoSeries.skew          #通过沿x和y维度的角度剪切/倾斜GeoSeries的几何
GeoSeries.translate     #移动GeoSeries的坐标

geo1 = Polygon([(0,0),(0,1),(1,1),(1,0)])
geo2 = Polygon([(1,0),(2,0),(2,1),(1,1)])
geo3 = Polygon([(0,0),(2,0),(2,1),(1,1)])
geo4 = Polygon([(3,3),(5,3),(5,4),(4,4)])
geo_s1 = MultiPolygon([geo1,geo2])
geo_s2 = MultiPolygon([geo1,geo3])
geo_s3 = MultiPolygon([geo1,geo4])
geo_s1 # geo1,geo2
geo_s2 #geo1,geo3
geo_s3 #geo1,geo4
geo1.intersects(geo1) #相交，一个点都算
geo1.intersection(geo1).area > 0.00001 #相交，取出相交的部分
geo44 = shapely.geometry.polygon.orient(geo4, sign=2.0)
geo4 = Polygon([(3,3),(5,4),(5,3),(5,3),(4,4)])
p1 = pyproj.Proj(init="epsg:4326") # 定义数据地理坐标系 WGS84
p2 = pyproj.Proj(init="epsg:3857") # 定义转换投影坐标系
x, y = pyproj.transform(p1, p2, lon, lat) # lon 和lat 可以是元组
geo1.intersection(geo2).area
geo1.overlaps(geo3) #相交需要有内部相交，且不包含
geo3.relate(geo2) #9 宫格
geo1.touches(geo1) #相交，且内部不想交
geo1.symmetric_difference(geo3) #去掉交集
geo1.union(geo3) # 合并图层,如果相交就融合，边相邻也是
[o.wkt for o in shapely.ops.nearest_points(geo1, geo4)] #计算两个多边形的最近点，可能不是现有的顶点

gdf.boundary 凸包
gpd.sjoin交集
gpd.overlay()交集面积
gdf.dissolve(by = '所属地区') 合并


from shapely.wkt import dumps, loads
loads('POLYGON ((837375.9352482457 3388127.612888217, 837410.1272730283 3387033.069187988, 837373.8431845196 3387025.271652122, 
          837375.9352482457 3388127.612888217))')
————————————————
度，如要转换成米，需要乘以,地球半径(6371000*PI/180)
如果要用米转为为度 则反过来 *180/(6371000*PI)

tab = "MapInfo File"  #".tab"
geojson ="GeoJSON"  #".geojson"
shp = "ESRI Shapefile"

'''

class MyTools_gis(object):
    # def __init__(self):

    def to_kml(self,
                df_zb,
                out_dir = 'd:/图层/栅格.kml',
                use_id='id',
                colour = 'colour',
                group_name = None,
                geometry='geometry',
                view = 5000):
        '''
        将geopandas数据导出kml文件，并设置颜色
        df_zb::geoDatafrem
        out_dir::输出的文件目录
        geometry::geoDatafrem的图形列名
        use_id::kml每个图形的名字
        group_name::按照该列分割文件
        colour::颜色支持类型：红色，白色，黄色，蓝色，绿色
        view::视野，配合box使用

        举例子：
        to_kml(df_zb, 'd:/图层2/','st_astext',group_name = '区域')
        '''
        de_col = df_zb.columns
        de_col = de_col.drop(geometry)
        df_zb['geometry'] = df_zb[geometry]
        df_zb = gpd.GeoDataFrame(df_zb,crs='epsg:4326',geometry='geometry')

        #添加标注列
        df_zb['description']=''
        for inde_1, name_1 in enumerate(de_col):
            df_zb['linshi']=de_col[inde_1]+' : '+df_zb[de_col[inde_1]].astype('str')+'\n'
            df_zb['description'] = df_zb['description']+df_zb['linshi']
            df_zb.drop(columns='linshi')
        df_zb = df_zb.drop(columns='linshi')
        data_sectors= df_zb.copy()
        data_sectors[['lon_t','lat_t']] = self.polygon_centroid(data_sectors)
        #添加lod的polygon
        data_sectors['lod_dis']= view
        data_sectors['lon1'] = data_sectors['lon_t'] + data_sectors['lod_dis']*np.sin(45* np.pi/180)*180/( np.pi * 6371229 * np.cos(data_sectors['lat_t'] * np.pi/180))
        data_sectors['lat1'] = data_sectors['lat_t'] + data_sectors['lod_dis']*np.cos(45* np.pi/180) / ( np.pi * 6371229 / 180)
        data_sectors['lon2'] = data_sectors['lon_t'] + data_sectors['lod_dis']*np.sin(225* np.pi/180)*180/( np.pi * 6371229 * np.cos(data_sectors['lat_t'] * np.pi/180))
        data_sectors['lat2'] = data_sectors['lat_t'] + data_sectors['lod_dis']*np.cos(225* np.pi/180) / ( np.pi * 6371229 / 180)
        data_sectors['list_data']=[([lon_1, lat_1,lon_2, lat_2]) 
         for lon_1, lat_1,lon_2, lat_2 in zip(data_sectors['lon1'],data_sectors['lat1'],data_sectors['lon2'],data_sectors['lat2'])]
        #最终使用的列
        if group_name:
            df_use = data_sectors.reindex(columns=['lon_t','lat_t',use_id,group_name,colour,'list_data','description','geometry'])   
        else:
            df_use = data_sectors.reindex(columns=['lon_t','lat_t',use_id,colour,'list_data','description','geometry'])   
        dict_color = {'红色':'ff0000ff','蓝色':'ffff0000','黄色':'ff00ffff','绿色':'ff008000','白色':'ffffffff'}
        def make_kml(data_t,name='红色栅格',cc='ff0000ff',xiankuan=0,minlodpixels=5):
            style = simplekml.Style()
            style.linestyle.color = simplekml.Color.changealphaint(250, cc)  # 最终线条上色
            style.linestyle.width = xiankuan
            style.polystyle.color = simplekml.Color.changealphaint(150, cc )  # 最终形状上色
            lod1 = simplekml.Lod(minlodpixels=minlodpixels, maxlodpixels=-1,minfadeextent=None, maxfadeextent=None)
            grid_red = kml.newfolder(name=name)
            for grid,list_data ,description_str,geo in zip(data_t[use_id],data_t['list_data'],data_t['description'],data_t['geometry']):
                pol_r = grid_red.newpolygon(name=grid,outerboundaryis=list(geo.exterior.coords),innerboundaryis=[po.coords for po in list(geo.interiors)])
                pol_r.description = description_str
                pol_r.altitudemode = simplekml.AltitudeMode.clamptoground
                lon_dd,lat_dd,lon1_dd,lat1_dd = list_data
                latlonaltbox = simplekml.LatLonAltBox(east =lon_dd ,north=lat_dd ,south=lat1_dd ,west=lon1_dd,
                                                      minaltitude=None, maxaltitude=None, altitudemode=None)
                pol_r.region.latlonaltbox = latlonaltbox
                pol_r.region.lod = lod1
                pol_r.style=style
        MyTools_other().new_folder(os.path.split(out_dir)[0])

        if group_name:
            for name,data_t in df_use.groupby(group_name):
                kml = simplekml.Kml()
                for name_c,data_c in data_t.groupby(colour):
                    cc = dict_color[name_c]
                    make_kml(data_c,name_c,cc)
                kml.save(f'{os.path.splitext(out_dir)[0]}_{name}.kml')
        else:
            kml = simplekml.Kml()
            for name_c,data_c in df_use.groupby(colour):
                cc = dict_color[name_c]
                make_kml(data_c,name_c,cc)
            kml.save(out_dir)




    def add_qiushen_grid(self,
                            df,
                            lon='lon_aggregation',
                            lat='lat_aggregation',
                            distance=50,
                            geometry='geometry'):
        '''
        功能：将点生成栅格，王秋体系
        df::DataFrame
        lon::经度列名
        lat::纬度列名
        distance::栅格大小
        '''

        df['geometry'] = df.apply(lambda x: Polygon(self._add_grid_aggregation(x[lon],x[lat],distance)),axis=1)
        df = gpd.GeoDataFrame(df, crs="epsg:4326",geometry='geometry')
        return df
    def _add_grid_aggregation(self,
                            lon,
                            lat,
                            distance):
        x1=lon+(distance*0.00001*1.0408)/2
        y1=lat+(distance*0.00001*0.9045)/2
        x2=lon-(distance*0.00001*1.0408)/2
        y2=lat-(distance*0.00001*0.9045)/2
        return ([(x1, y1), (x1, y2), (x2, y2),(x2, y1),(x1, y1)])

    def add_qiushen_lonlat(self,
                        df,
                        lon='lon',
                        lat='lat',
                        grid_size=50,
                        amend_lon=1.0408,
                        amend_lat=0.9045):
        '''
        功能：将df中的经纬度汇聚到一个点上，王秋体系
        df::DataFrame
        lon::经度列名
        lat::纬度列名
        grid_size::距离，栅格的大小，配合add_grid_aggregation（生成栅格）使用
        amend_lon 和 amend_lat为经纬度偏移距离，坐标系和googel地球对比。
        '''
        grid_size = grid_size # 米
        lon_juli=grid_size*amend_lon
        lat_juli=grid_size*amend_lat
        df['lon_aggregation']=((df[lon]/lon_juli).round(5)*lon_juli)
        df['lat_aggregation']=((df[lat]/lat_juli).round(5)*lat_juli)
        df['ID_aggregation'] = df["lon_aggregation"].astype(str) + df["lat_aggregation"].astype(str)
        return df

    def delaunay_triangles(self,
                            df,
                            id_use='栅格ID',
                            lon='lon',
                            lat='lat'):
        '''
        功能：将表格中的经纬度生成delaunay三角形，每个三角形关联id编号
        df::DataFrame
        id_use::表中的id列名
        lon::经度列名
        lat::纬度列名
        return gdf 可以直接导出为图层
        '''
        df['lonlat'] = df[lon].map(str) + df[lat].map(str)
        triangles = triangulate(MultiPoint([[lon,lat] for lon,lat in zip(df[lon],df[lat])]),tolerance=0.00001)
        gdf = gpd.GeoDataFrame(pd.DataFrame([[index,t] for index,t in enumerate(triangles)],columns=['id','geometry']),crs="epsg:4326",geometry='geometry')
        gdf[['site1','site2','site3']] = gdf['geometry'].apply(lambda c:pd.Series([str(x)+str(y) for x,y in [xy for xy in {c_t for c_t in c.exterior.coords}]]))
        for i in range(1,4):
            gdf = gdf.merge(df[[id_use,'lonlat']].rename(columns={id_use:f'{id_use}_{i}','lonlat':f'site{i}'}),how='left',on=f'site{i}')
        return gdf

    def to_shp(self,
                gdf_data,
                out_path='d:/polygon.shp',
                encoding='gbk',
                geometry_name='geometry',
                use_crs = "epsg:4326"):
        '''
        功能：将geopandas导入的gdf导出为shp格式文件，
        目前支持
        polygon,MultiPolygon,BaseMultipartGeometry
        Point,MultiPoint,
        LineString,LinearRing,MultiLineString
        不支持 GeometryCollection
        主要解决geopandas导出shp文件中文乱码问题
        '''
        #将‘geometry’列放到最后
        gdf_data = gdf_data.reindex(columns=(gdf_data.columns.drop(geometry_name).insert(gdf_data.shape[1],geometry_name)))
        gdf_data = gpd.GeoDataFrame(gdf_data,crs=use_crs,geometry=geometry_name)
        w = shapefile.Writer(out_path,encoding='gbk')
        #列名传给shp的属性列名
        [w.field(x) for x in gdf_data.drop(columns=geometry_name).columns]
        #循环每一行数据判断类型整理成对应的列表写入w
        for row in gdf_data.iterrows():
            geo = row[1]['geometry']
            if geo.type == 'MultiPolygon':#判断是否为MultiPolygon是就循环下
                exterior_z = []
                for data in geo:
                    data_a = data.exterior
                    exterior_z.append([[list(x) for x in list(data_a.coords)]])
                    for data_i in data.interiors:
                        exterior_z.append([[list(x) for x in list(data_i.coords)]])
                exterior = list(chain(*exterior_z))
                w.poly(exterior)
            elif geo.type == 'Polygon':
                def to_co(ring):
                    return [[list(x) for x in list(ring.coords)]]
                exterior = list(chain.from_iterable(map(to_co,[geo.exterior, *geo.interiors])))
                w.poly(exterior)
            elif geo.type == 'Point':
                exterior = [geo.x, geo.y]
                w.point(geo.x, geo.y)
            elif geo.type == 'MultiPoint':
                exterior = list(map(lambda x:[x.x,x.y],geo))
                w.multipoint(exterior)
            elif geo.type == 'LineString':
                exterior = [[list(x) for x in list(geo.coords)]]
                w.line(exterior)
            elif geo.type == 'LinearRing':
                exterior = [[list(x) for x in list(geo.coords[:-1])]]
                w.line(exterior)
            elif geo.type == 'MultiLineString':
                exterior = [[list(x) for x in list(x.coords)] for x in geo]
                w.linem(exterior)
            else:
                print('错误一行')
            w.record(*[x for x in row[1][:-1]]) # 输出每一行的内容除了geometry
        w.close()
        # proj = osr.SpatialReference()
        crs_num = int(use_crs.split(':')[1])
        # proj.ImportFromEPSG(crs_num)
        # #或 proj.ImportFromProj4(proj4str)等其他的来源
        # wkt = proj.ExportToWkt()
        #写出prj文件
        crs_dict = {
                    4326:'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
                    32651:'PROJCS["WGS_1984_UTM_zone_51N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["false_easting",500000.0],PARAMETER["false_northing",0.0],PARAMETER["central_meridian",123.0],PARAMETER["scale_factor",0.9996],PARAMETER["latitude_of_origin",0.0],UNIT["Meter",1.0]]'
                    }
        f = open(out_path.replace(".shp",".prj"), 'w')
        f.write(crs_dict[crs_num])
        f.close()

    def covering_radius_5G(self,
                        df,
                        cj='区域类型',
                        zs='制式',
                        distance='distance',
                        model='default'
                       ):
        '''
        主要在计算不同场景不同工作频段对应的覆盖半径距离,自用
        df = covering_radius(df,'区域类型','工作频段')
        '''
        if model=='default':
            F700 = {'主城区':350,'一般城区':450,'市郊':450,'县城':600,'乡镇':650,'农村':2500}
            F260 = {'主城区':250,'一般城区':300,'市郊':300,'县城':350,'乡镇':550,'农村':1200}
        elif model=='min':
            F700 = {'主城区':210,'一般城区':270,'市郊':270,'县城':360,'乡镇':390,'农村':1500}
            F260 = {'主城区':150,'一般城区':180,'市郊':180,'县城':210,'乡镇':330,'农村':720}
        elif model=='max':
            F700 = {'主城区':500,'一般城区':700,'市郊':700,'县城':800,'乡镇':900,'农村':4000}
            F260 = {'主城区':350,'一般城区':450,'市郊':450,'县城':550,'乡镇':800,'农村':1800}
        def matching(a,b):
            if b in ['700MHz']:
                return F700[a]
            elif b in ['2.6GHz']:
                return F260[a]
            elif b == '4.9GHz':
                return F260[a]
            else:
                print(f"{b}::格式错误：有效的格式为['700MHz','2.6GHz','4.9GHz']")
                return F260[a]
        df[distance] = df.apply(lambda x:matching(str(x[cj]),str(x[zs])),axis=1)
        return df
    def covering_radius(self,
                        df,
                        cj='区域类型',
                        zs='制式',
                        distance='distance',
                        model='default'
                       ):
        '''
        主要在计算不同场景不同工作频段对应的覆盖半径距离,自用
        df = covering_radius(df,'区域类型','工作频段')
        '''
        if model=='default':
            FDD_900 = {'主城区':300, '一般城区':450, '县城':400, '乡镇':1200, '农村':2200}
            FDD_1800 = {'主城区':250, '一般城区':400, '县城':350, '乡镇':800, '农村':1000}
            TDD_D = {'主城区':200, '一般城区':350, '县城':300, '乡镇':450, '农村':600}
            TDD_other = {'主城区':150, '一般城区':250, '县城':200, '乡镇':350, '农村':400}
            shifen = {'主城区':100, '一般城区':100, '县城':100, '乡镇':100, '农村':100}
        elif model=='min':
            FDD_900 = {'主城区':180, '一般城区':270, '县城':240, '乡镇':720, '农村':1320}
            FDD_1800 = {'主城区':150, '一般城区':240, '县城':210, '乡镇':480, '农村':600}
            TDD_D = {'主城区':120, '一般城区':210, '县城':180, '乡镇':270, '农村':360}
            TDD_other = {'主城区':90, '一般城区':150, '县城':120, '乡镇':210, '农村':240}
            shifen = {'主城区':100, '一般城区':100, '县城':100, '乡镇':100, '农村':100}
        elif model=='max':
            FDD_900 = {'主城区':450, '一般城区':650, '县城':600, '乡镇':1800, '农村':3300}
            FDD_1800 = {'主城区':400, '一般城区':600, '县城':550, '乡镇':1200, '农村':1500}
            TDD_D = {'主城区':300, '一般城区':500, '县城':450, '乡镇':700, '农村':900}
            TDD_other = {'主城区':200, '一般城区':400, '县城':350, '乡镇':500, '农村':600}
            shifen = {'主城区':100, '一般城区':100, '县城':100, '乡镇':100, '农村':100}

        def matching(a,b):
            if b in ['F','FDD1800','F1','F2','F3','F4','S']:
                return FDD_1800[a]
            elif b in ['A', 'D', 'D1', 'D2', 'D3','D4', 'D5', 'D6', 'D7','D8','D9']:
                return TDD_D[a]
            elif b in ['FDD900','G']:
                return FDD_900[a]
            elif b in '零购、低成本、普服':
                return TDD_other[a]
            elif b in '微站':
                return TDD_other[a]
            elif b in '零购900、低成本900、普服900 ':
                return TDD_D[a]
            elif b in '室分室内微站E E1 E2 E3':
                return shifen[a]
            else:
                print(f"{b}::格式错误：有效的格式为['F','FDD1800','A', 'D', 'E','FDD900','零购、低成本、普服','零购900、低成本900、普服900']")
                return FDD_1800[a]
        df[distance] = df.apply(lambda x:matching(str(x[cj]),str(x[zs])),axis=1)
        return df

    def add_azimuth_angle(self,
                            df,
                            lon='lon',
                            lat='lat', 
                            lon2='lon2',
                            lat2='lat2',
                            columns_name='方位角差异'):
        '''
        作用：计算另个经纬度点之间的方位角夹角
        接收参数
        df:带有两个经纬度参数的表格，分别为lon,lat,lon2,lat2
        columns_name:是新家的列名自定义
        '''
        radLonA, radLatA, radLonB, radLatB = map(np.radians, [df[lon], df[lat], df[lon2], df[lat2]])
        x = np.cos(radLatA) * np.sin(radLatB) - np.sin(radLatA) * np.cos(radLatB) * np.cos(radLonB - radLonA)
        brng = np.degrees(np.arctan2((np.sin(radLonB - radLonA) * np.cos(radLatB)), x))
        df[columns_name] =(brng + 360) % 360
        return df
    def dissolve(self,
                gdf,
                columns_name='区县',
                by=['伍家岗区','猇亭区'],
                new_name='宜昌开发区'):
        '''
        作用：合并在一个gdf表中的两个多边形，根据他的某一个字段信息
        接收参数
        gdf：带geometry的geopandas表
        columns_name:选择要合并的列名
        by:在columns_name的列中 值等于by中的两个字段的geometry进行合并
        new_name:合并后的columns_name值命名为new_name
        '''
        gdf['combine_x'] = 'hb' 
        qx1 , qx2 = by
        if gdf.loc[gdf[columns_name].isin([qx1,qx2])].shape[0] ==2:
            gdf_t = gdf.loc[gdf[columns_name].isin([qx1 , qx2 ])].dissolve(by = 'combine_x').reset_index()
            gdf_t[columns_name] = new_name
            gdf = gdf_t.append(gdf.loc[~gdf[columns_name].isin([qx1 , qx2 ])])
            gdf = gdf.drop(columns='combine_x')
            print('合并成功')
            return gdf
        else:
            print('两个名字不能同时找到图层')

    def polygon_centroid(self, gdf):
        '''
        作用：计算出多边形的质心
        gdf[['lon','lat']] = mytools.gisn.polygon_centroid(gdf)
        '''
        return gdf.apply(lambda x:pd.Series(x['geometry'].centroid.coords[:][0]),axis=1)
    def read_kml(self,file_name):
        '''
        作用：读取kml文件中的gis属性和id
        '''
        k2g.convert(file_name, './temp')
        try:
            gdf = gpd.read_file(os.path.splitext('./temp/'+os.path.split(file_name)[-1])[0]+'.geojson',encoding='gbk')
        except:
            gdf = gpd.read_file(os.path.splitext('./temp/'+os.path.split(file_name)[-1])[0]+'.geojson',encoding='utf-8')
        shutil.rmtree( './temp')
        return gdf
    def quadrat_cut_geometry(self,
                            geometry,
                            quadrat_width,
                            min_num=3,
                            buffer_amount=1e-9):
        """
        将一个多边形或多个多边形分割成具有指定大小的子多边形
        参数
        ----------
        geometry : shapely.geometry.Polygon 或者 shapely.geometry.MultiPolygon
            将一个多边形或多个多边形分割成具有指定大小的子多边形。参数
        quadrat_width : 数字z
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
    def box_make_to_polygon(self,
                        lon_n=114.198312,
                        lat_n=30.630697,
                        radius=70):
        '''
            点生成类似buffer的正方形
            radius：100米的栅格使用70.5，10米的栅格使用35
            df['geometry'] = df.apply(lambda x: mytools.gisn.box_make_to_polygon(x['lon'],x['lat'],2.1),axis=1)
        '''
        res = Geodesic.WGS84.Direct(lat_n, lon_n, 45, radius)
        lon_1= res['lon2']
        lat_1= res['lat2']
        res1 = Geodesic.WGS84.Direct(lat_n, lon_n, 225, radius)
        lon_2= res1['lon2']
        lat_2= res1['lat2']
        return Polygon([(lon_2, lat_2), (lon_2, lat_1), (lon_1, lat_1),(lon_1, lat_2),(lon_2, lat_2)])
    
    def box_make_kmluse(self,
                        lon_n=114.198312,
                        lat_n=30.630697,
                        radius=70):
        '''
            点生成以点为中心的经纬度列表
        '''
        res = Geodesic.WGS84.Direct(lat_n, lon_n, 45, radius)
        lon_1= res['lon2']
        lat_1= res['lat2']
        res1 = Geodesic.WGS84.Direct(lat_n, lon_n, 225, radius)
        lon_2= res1['lon2']
        lat_2= res1['lat2']
        return ([(lon_2, lat_2), (lon_2, lat_1), (lon_1, lat_1),(lon_1, lat_2),(lon_2, lat_2)])

    def df_to_gdf(self,df,geometry='geometry'):
        '''
        作用：将带有geometry列的df转换成gdf
        '''
        df[geometry] = df[geometry].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df, crs="epsg:4326",geometry=geometry)
        return gdf

    def buffer(self,
                    df,
                    buff_float= 600 ,
                    geometry='geometry'):    
        '''
        作用：将一个gdf数据的geometry图形进行扩大buffer
        '''
        df=df.to_crs(epsg=32650)
        df[geometry]=df[geometry].buffer(buff_float)
        df=df.to_crs(epsg=4326)
        return df

    def buffer_df(self,
                    df,
                    buff_col='距离',
                    geometry='geometry'
                    ):
        '''
        作用：将一个gdf数据的geometry图形进行扩大buffer，接受数据列为距离
        '''
        df=df.to_crs(epsg=32650)
        df[geometry]=df[[geometry,buff_col]].apply(lambda x:x[0].buffer(x[1]),axis=1)
        df=df.to_crs(epsg=4326)
        return df
    def add_buffer(self,
                    df,
                    lon='CellLongitude',
                    lat='CellLatitude',
                    buff_float= 600 ,
                    geometry='geometry'
                    ):   
        '''
        作用：将一个经纬度数据进行扩大buffer
        '''          
        df[geometry]=df[[lon,lat]].apply(lambda x:Point((x[0],x[1])),axis=1)
        df=gpd.GeoDataFrame(df,crs="epsg:4326",geometry=geometry)
        df=df.to_crs(epsg=32650)
        df[geometry]=df[geometry].buffer(buff_float)
        df=df.to_crs(epsg=4326)
        return df
    def add_buffer_df(self,
                        df,
                        lon='CellLongitude',
                        lat='CellLatitude',
                        buff_col='距离',
                        geometry='geometry'
                        ):
        '''
        作用：将一个经纬度数据进行扩大buffer，接受数据列为距离
        '''        
        df[geometry]=df[[lon,lat]].apply(lambda x:Point((x[0],x[1])),axis=1)
        df=gpd.GeoDataFrame(df,crs="epsg:4326",geometry=geometry)
        df=df.to_crs(epsg=32650)
        df[geometry]=df[[geometry,buff_col]].apply(lambda x:x[0].buffer(x[1]),axis=1)
        df=df.to_crs(epsg=4326)
        return df
    def _changjing_distance(self,
                            df,
                            changjing,
                            zhishi,
                            use_type='覆盖半径', # 站间距 或者 覆盖半径
                            beishu=1
                            ):
        '''20210308弃用，由covering_radius代替
        添加的列为‘distance，
        use_type 填写 站间距 或者 覆盖半径
        举例： df = changjing_distance(df,'场景','制式',use_type='覆盖半径'beishu=1)
        ’'''
        print('20210308弃用，由covering_radius代替')
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
                        coords=['lon','lat','height','azimuth','min','max'],
                        has_z=False,
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
        df = gpd.GeoDataFrame(df, crs="epsg:4326", geometry=sec_col)
        return df
    def maps(self,
            name='湖北地市',
            cd='g'
            ):
        '''自用，方便读取本地的文件'''
        if (name == '湖北地市') or (name == '湖北地图') or (name == '湖北'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/湖北省地市-边界-边界/全省地市边界/地市地图.shp'.format(g=cd),encoding = 'utf-8')
            city_tu = city_tu.to_crs(epsg=4326)
        elif (name=='湖北区县') or (name=='湖北县城') or (name=='县城') or (name=='区县'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/武汉新-县城图层/县界.TAB'.format(g=cd),encoding = 'gbk')
        elif (name=='地市区县'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/全省县界/2021年合并/shp/湖北地市区县图层.shp'.format(g=cd),encoding = 'gbk')
        elif (name=='武汉') or (name=='武汉地图'):
            city_tu = gpd.read_file('{g}:/1-规划/图层/武汉分公司图层20190109/武汉市区分公司区域图层201804版/武汉市区分公司区域图层201804版/武汉市区分公司区域图层201804版.TAB'.format(g=cd),encoding = 'gbk')
            city_tu = city_tu.to_crs(epsg=4326)
        elif (name=='场景') or (name=='changjing'):
            coverage='{g}:/1-规划/图层/全省区域规划图层20200110/全省区域规划图层20200110.TAB'.format(g=cd)
            city_tu = gpd.read_file(coverage,encoding = 'gbk')
        elif (name=='atu') or (name=='核心城区') or (name == '城区'):
            coverage='{g}:/1-规划/图层/ATU测试区域/ATU网格总.TAB'.format(g=cd)
            city_tu = gpd.read_file(coverage,encoding = 'gbk')
            city_tu['type'] = city_tu.type
            city_tu = city_tu.loc[tu['type']=='Polygon']
            city_tu['场景'] = 'atu'
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
        df[pnt_col] = [Point(x) for x in zip(df[lon], df[lat])]
        df_p = gpd.GeoDataFrame(df, crs="epsg:4326", geometry=pnt_col) 
        return df_p


    def min_site_two_table(self,
                            data,
                            data2,
                            lon='lon',
                            lat='lat',
                            lon2='lon2',
                            lat2='lat2',
                            num_min_results = 3,
                            juli_n = None):
        '''
        作用：两个表找最近点，1个或者多个
        min_site_two方法用于：
        1、查询一批位置点的最近的一个站点（在另一个表中），以及它的距离。
        2、查询一批位置点的最近的n个点（在另一个表中），以及它们的平均距离。（相当于平均站间距）
        data：一个数据表格
        data2:另一个数据表
        lon，lat,lon2,lat2：经纬度的字段两个表的。
        num_min_results：如果查询最近的一个站点则设置为1，如果查询多个最近站点并求平均数设置>1
        juli_n 限制距离 超出距离不计算
        例子：
        min_site_two(data1,data2,'lon','lat','lon','lat',3)
        '''
        if lon == lon2:
            data2 = data2.rename(columns={lon2:lon2+'_right'})
            lon2 = lon2+'_right'
        if lat == lat2:
            data2 = data2.rename(columns={lat2:lat2+'_right'})
            lat2 = lat2+'_right'
        if isinstance(num_min_results,str) | isinstance(num_min_results,float):
            print('错误：输入的num_min_results不能为字符或者小数，请输入大于0的整数')
            assert 0
        elif num_min_results<1:
            print('错误：输入的num_min_results不合理，请输入大于0的整数')
            assert 0
            
        data_use = data.copy()
        data_use['geometry'] = [Point(x) for x in zip(data_use[lon], data_use[lat])]
        data_zhan_pot = gpd.GeoDataFrame(data_use, crs="epsg:4326", geometry='geometry')
    #     data_zhan_pot = data_zhan_pot.reset_index(drop=True).reset_index()
        
        data2 = data2.reset_index(drop=True).reset_index()
        data_zhan_pot_name = data2[['index',lon2,lat2]]
        data2['geometry'] = [Point(x) for x in zip(data2[lon2], data2[lat2])]
        data2_pot = gpd.GeoDataFrame(data2, crs="epsg:4326", geometry='geometry')
        data_sindex = data2_pot.sindex

        if num_min_results==1:
            data_zhan_pot['minimum_index'] = data_zhan_pot['geometry'].apply(
                lambda x: list(data_sindex.nearest(x.bounds,num_results=1))[0])
            data_zhan_pot = data_zhan_pot.drop(['geometry'],axis=1)
            df = data_zhan_pot.merge(
                data_zhan_pot_name,how = 'left',left_on = 'minimum_index',right_on='index',suffixes=('','_y'))
            lon1, lat1, lon22, lat22 = map(np.radians, [df[lon], df[lat], df[lon2], df[lat2]])
            dis_t = np.sin((lat22 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat22)*np.sin((lon22 - lon1)/2)**2
            df['distance']= 2*np.arcsin(np.sqrt(dis_t))*6371*1000
            try:
                res = df.drop(['index_y'],axis=1)
            except:
                res = df.copy()
        elif num_min_results>1:
            three_minimum_point= data_zhan_pot['geometry'].apply(
                lambda x: list(data_sindex.nearest(x.bounds,num_results=num_min_results))[0:num_min_results])
            data_zhan_pot = data_zhan_pot.drop(['geometry'],axis=1)
            three_minimum_point_df = pd.DataFrame(
                [x for x in three_minimum_point],columns = 
                [ 'minimum_index_'+str(y+1) for y,z in enumerate(three_minimum_point[0])])
            data_zhan_pot_minimum3 = pd.concat([data_zhan_pot,three_minimum_point_df],axis=1)
            distance_dict = dict()

            for columns_index , name in enumerate(three_minimum_point_df.columns):
                df = data_zhan_pot_minimum3.merge(
                    data2,how='left',left_on = name,right_on = 'index',suffixes=('','_y'))
                lon1, lat1, lon22, lat22 = map(np.radians, [df[lon], df[lat], df[lon2], df[lat2]])
                dis_t = np.sin((lat22 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat22)*np.sin((lon22 - lon1)/2)**2
                name_data= 2*np.arcsin(np.sqrt(dis_t))*6371*1000
                distance_dict['distance_'+str(columns_index+1)] = name_data
            distance_dict_df = pd.DataFrame(distance_dict)
            if juli_n:
                distance_dict_df[distance_dict_df>juli_n] = 0
            distance_dict_df['mean'] = distance_dict_df.mean(axis=1)
            res = pd.concat([data_zhan_pot_minimum3,distance_dict_df],axis=1)
        res.reset_index(drop=True,inplace=True)
        return res
    def min_site_one_table(self,data,
                 id_name_column='id',
                 lon='lon',
                 lat='lat',
                 num_min_results = 3,
                 Including_itself = False,
                 juli_n = None
                 ):
        '''
        作用：表内找最近站点，一个或者多个
        nearest_site方法用于：
        1、查询一批位置点的最近的一个点的那个点，以及它的距离。
        2、查询一批位置点的最近的n个点，以及它们的平均距离。（相当于平均站间距）
        data：一个数据表格
        id_name_column：字段-每个数据的id或者名字
        lon，lat：经纬度的字段
        num_min_results：如果查询最近的一个站点则设置为1，如果查询多个最近站点并求平均数设置>1
        Including_itself:选True：包括自己; 选False:不包括自己（通常设置为False）
            在num_min_results=1选True的时候，最近站点为自身，距离都为0。
            在num_min_results>1选True的时候最，近的一个站点距离为0，结果为两个站点的平均值。
        juli_n 限制距离 超出距离不计算
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
        data_zhan_pot = gpd.GeoDataFrame(data_use, crs="epsg:4326", geometry='geometry')
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

    def min_site_one_table_only(self,data,
                 id_name_column='id',
                 lon='lon',
                 lat='lat',
                 num_min_results = 3,
                 Including_itself = False
                 ):
        '''
        弃用
        nearest_site方法用于：查询一批位置点的最近的第N个站点，以及它的距离。
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
        data_zhan_pot = gpd.GeoDataFrame(data_use, crs="epsg:4326", geometry='geometry')
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



    
    def points_coverage_merge(self,
                                df,
                                lon='lon',
                                lat='lat',
                                coverage='d:/工作/图层/规划场景图层/规划场景图层20211222.shp',
                                df_merge_coverage_columns=['区域类型'],
                                merge_only_right_mark='农村'
                                ):
        '''
            作用：给经纬度数据添加一列，匹配到图层中的属性
            示例是给df打标场景
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
                guihua = gpd.read_file(coverage,encoding='gbk')
                if guihua.crs=="epsg:4326":
                    pass
                else:
                    guihua = guihua.to_crs(epsg=4326)
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
                if guihua.crs=="epsg:4326":
                    pass
                else:
                    guihua = guihua.to_crs(epsg=4326)
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
                try:
                    if '区域类型' in list(guihua.columns):
                        res_use_ok_df['区域类型'] = res_use_ok_df['区域类型'].replace({'3A景区':'农村','4A景区':'农村','5A景区':'农村','景区':'农村','热点':'乡镇'})
                except:
                    pass
                return res_use_ok_df

    def distancea_df(self,
                        df,
                        lon_1, 
                        lat_1, 
                        lon_2, 
                        lat_2,
                        columns_name='距离'
                        ):
        '''
        作用：计算df中一行数据有两个经纬度的情况下，他们的距离
        '''
        lon1, lat1, lon2, lat2 = map(np.radians, [df[lon_1], df[lat_1], df[lon_2], df[lat_2]])
        a = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
        df[columns_name] = 2*np.arcsin(np.sqrt(a))*6371*1000
        return df
    def distancea_str(self,
                        lon_1, 
                        lat_1, 
                        lon_2, 
                        lat_2
                        ):
        '''
        作用：计算两个经纬度他们的距离
        '''
        lon1, lat1, lon2, lat2 = map(np.radians, [lon_1,lat_1,lon_2,lat_2])
        a = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
        res = 2*np.arcsin(np.sqrt(a))*6371*1000
        return res

    def add_area(self,
                    gdf,
                    column = '面积'
                    ):
        '''把gdf新增一列‘面积‘单位是平方米
        临时转换成
        gdf = gdf.to_crs({epsg=32650}) #投影坐标系WGS 84 / UTM zone 50N的ID是32650
        计算面积后转回原来的坐标系
        '''
        crs_t=gdf.crs
        gdf = gdf.to_crs(epsg=32650)
        gdf[column]=gdf.area
        gdf = gdf.to_crs(crs_t)
        return gdf
    def add_length(self,
                    gdf,
                    column = '线条长度'
                    ):
        '''把gdf新增一列‘线条长度‘单位是米
        临时转换成
        gdf = gdf.to_crs(epsg=32650) #投影坐标系WGS 84 / UTM zone 50N的ID是32650
        计算面积后转回原来的坐标系"epsg:4326"
        '''
        crs_t=gdf.crs
        gdf = gdf.to_crs(epsg=32650)
        gdf[column]=gdf.length
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
        df.loc[:, sec_col] = [self.lod_lon_lat(x,y, radius=7000) for x,y in zip(df[lon], df[lat])]
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
                        coords=['lon','lat','height','azimuth','radius'],
                        has_z=False,
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
        df = gpd.GeoDataFrame(df, crs="epsg:4326", geometry=sec_col)
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
                    has_z=False,
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
        df = gpd.GeoDataFrame(df, crs="epsg:4326", geometry=sec_col)
        return df
'''
Geometry = TypeVar('Geometry', bound=BaseGeometry)
@singledispatch
def to_coords(geometry: Geometry) -> List[Tuple[float, float]]:
    """Returns a list of unique vertices of a given geometry object."""
    raise NotImplementedError(f"Unsupported Geometry {type(geometry)}")
@to_coords.register
def _(geometry: Point):
    return [(geometry.x, geometry.y)]
@to_coords.register
def _(geometry: LineString):
    return list(geometry.coords)
@to_coords.register
def _(geometry: LinearRing):
    return list(geometry.coords[:-1])
@to_coords.register
def _(geometry: BaseMultipartGeometry):
    return list(set(chain.from_iterable(map(to_coords, geometry))))
@to_coords.register
def _(geometry: Polygon):
    return to_coords(GeometryCollection([geometry.exterior, *geometry.interiors]))
'''
