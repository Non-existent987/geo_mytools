#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math,simplekml,os
import pandas as pd
import numpy as np
import mytools


# # 导入数据

# In[ ]:


grid = pd.read_pickle('G:/1-规划/评估/软采评估/2020年1季度/1-数据存放/grid_add_yanzhong_qc.data')


# # 整理数据

# In[ ]:


def df_to_kml_zb(df,lon='lon',lat='lat',distance=70,id_use='grid_id',fgl='fgl',rsrp_count='rsrp_sample_count',
                 city = '城市',qx='区县',
                 de_col = ['grid_id','rsrp_sample_count','rsrp_weak','有效栅格','fgl','弱覆盖栅格数量','严重弱覆盖栅格数量']):
    df['colour'] = pd.cut(df[fgl],bins=[-0.1, 0.7, 0.936, 1.1],labels =['red', 'yellow', 'green'] )
    df['colour'] = df['colour'].astype('object')
    df.loc[df[rsrp_count]<100,'colour']='white'
    df['description']=''
    for inde_1, name_1 in enumerate(de_col):
        df['linshi']=de_col[inde_1]+' : '+df[de_col[inde_1]].astype('str')+'\n'
        df['description'] = df['description']+df['linshi']
    df = df.reindex(columns=[city,qx,id_use, 'list_data','colour','description',lon,lat])    
    print('颜色和标注完成')
    df['distance']=distance
    df['lon1'] = df[lon] + df['distance']*np.sin(45* np.pi/180)*180/( np.pi * 6371229 * np.cos(df[lat] * np.pi/180))
    df['lat1'] = df[lat] + df['distance']*np.cos(45* np.pi/180) / ( np.pi * 6371229 / 180)
    df['lon2'] = df[lon] + df['distance']*np.sin(225* np.pi/180)*180/( np.pi * 6371229 * np.cos(df[lat] * np.pi/180))
    df['lat2'] = df[lat] + df['distance']*np.cos(225* np.pi/180) / ( np.pi * 6371229 / 180)
    df['list_data']=[([(lon_2, lat_2), (lon_2, lat_1), (lon_1, lat_1),(lon_1, lat_2),(lon_2, lat_2)],[lon_1, lat_1,lon_2, lat_2]) 
     for lon_1, lat_1,lon_2, lat_2 in zip(df['lon1'],df['lat1'],df['lon2'],df['lat2'])]
    print('生成栅格方块完成')
    df = df.reindex(columns=[city,qx,id_use, 'list_data','colour','description'])    
    return df


# In[ ]:


grid2 = df_to_kml_zb(grid,lon='lon',lat='lat',distance=70,id_use='grid_id',fgl='fgl',rsrp_count='rsrp_sample_count',city = '城市',
                qx='区县',de_col = ['grid_id','rsrp_sample_count','rsrp_weak','有效栅格','fgl','弱覆盖栅格数量','严重弱覆盖栅格数量'])


# # 切割数据导出数据

# In[ ]:


for name_g,data_g in grid2.groupby(['城市']):
    data_g.to_pickle('G:/1-规划/评估/软采评估/2020年1季度/输出个地市的小区和栅格图层/栅格图层/生成图层使用数据/{}.data'.format(name_g))


# In[ ]:


del grid2


# # 制作图层

# In[20]:


def make_kml(data_t,name='红色栅格',cc='ff0000ff',xiankuan=0,namea='grid_id',list_data = 'list_data',description='description'):
    style = simplekml.Style()
    #style.linestyle.color = simplekml.Color.changealphaint(150, cc)  # 最终线条上色
    style.polystyle.outline = xiankuan
    style.polystyle.color = simplekml.Color.changealphaint(125, cc )  # 最终形状上色
    lod1 = simplekml.Lod(minlodpixels=3, maxlodpixels=-1,minfadeextent=None, maxfadeextent=None)
    grid_red = kml.newfolder(name=name)
    for grid,list_data ,description_str in zip(data_t[namea],data_t[list_data],data_t[description]):
        pol_r = grid_red.newpolygon(name=grid,outerboundaryis=list_data[0])
        pol_r.description = description_str
        pol_r.altitudemode = simplekml.AltitudeMode.clamptoground
        lon_dd,lat_dd,lon1_dd,lat1_dd = list_data[1]
        latlonaltbox = simplekml.LatLonAltBox(east =lon_dd ,north=lat_dd ,south=lat1_dd ,west=lon1_dd,
                                              minaltitude=None, maxaltitude=None, altitudemode=None)
        pol_r.region.latlonaltbox = latlonaltbox
        pol_r.region.lod = lod1
        pol_r.style=style


# In[21]:


f = mytools.othern.file_name_paths('G:/1-规划/评估/软采评估/2020年1季度/输出个地市的小区和栅格图层/栅格图层/生成图层使用数据')


# In[22]:


for name_f in f:
    name_region = name_f.split('.')[0].split('\\')[1]
    grid_t = pd.read_pickle(name_f)
    grid_groupby = grid_t.groupby(['区县'])
    for name_qx,data_region in grid_groupby:
        kml = simplekml.Kml()
        if not os.path.exists('G:/1-规划/评估/软采评估/2020年1季度/输出个地市的小区和栅格图层/栅格图层/{}'.format(name_region)):
            os.makedirs('G:/1-规划/评估/软采评估/2020年1季度/输出个地市的小区和栅格图层/栅格图层/{}'.format(name_region))
        file = 'G:/1-规划/评估/软采评估/2020年1季度/输出个地市的小区和栅格图层/栅格图层/{}/栅格图层_{}_{}.kmz'.format(name_region,name_region,name_qx)
        for name_c,data_t in data_region.groupby('colour'):
            if 'red' ==name_c:
                make_kml(data_t,name='红色栅格{}个'.format(data_t.shape[0]),cc='ff0000ff')
            elif 'green' == name_c:
                make_kml(data_t,name='绿色栅格{}个'.format(data_t.shape[0]),cc='ff008000')
            elif 'yellow' == name_c:
                make_kml(data_t,name='黄色栅格{}个'.format(data_t.shape[0]),cc='ff00ffff')
            elif 'white' == name_c:
                make_kml(data_t,name='白色栅格{}个'.format(data_t.shape[0]),cc='ffffffff')
        kml.save(file) if 'kml' in file else kml.savekmz(file, False)
        print('生成图层成功存放在{}'.format(file))


# In[ ]:




