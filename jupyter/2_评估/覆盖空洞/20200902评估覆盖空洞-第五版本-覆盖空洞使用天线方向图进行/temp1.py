from geographiclib.geodesic import Geodesic
from shapely.geometry import Polygon,Point,LineString
import pandas as pd
import geopandas as gpd
import mytools,os ,sys,time,multiprocessing
from multiprocessing import Pool
mx_900 = mytools.othern.pickle_read('G:/mypy/mycloud/jupyter/2_评估/覆盖空洞/20200902评估覆盖空洞-第五版本-覆盖空洞使用天线方向图进行/1-基础数据/44低增益900M0下倾P3_935覆盖模型.data')
mx_f = mytools.othern.pickle_read('G:/mypy/mycloud/jupyter/2_评估/覆盖空洞/20200902评估覆盖空洞-第五版本-覆盖空洞使用天线方向图进行/1-基础数据/F频段模型fad天线.data')
mx_d = mytools.othern.pickle_read('G:/mypy/mycloud/jupyter/2_评估/覆盖空洞/20200902评估覆盖空洞-第五版本-覆盖空洞使用天线方向图进行/1-基础数据/D频段模型fad天线.data')
data_z = pd.read_pickle('temp1.data')
#导入区县图层
def jm_z(x,jd_dp,lon,lat):
    jl = int(x['distance_use'])
    lon = x[lon]
    lat = x[lat]
    fw = x['方位角']
    jd_dp['distance_use'] = jd_dp['电平_正'].apply(lambda x: x/37.052 *jl)
    jd_dp_use = jd_dp.loc[(jd_dp['角度']<=90) | (jd_dp['角度']>=270)]
    jd_dp_use['角度'] = pd.to_numeric(jd_dp_use['角度'] )
    jd_dp_use['角度2'] = jd_dp_use['角度'].apply(lambda x: x-0+fw if x-0+fw<360 else x-0+fw-360 )
    points=[]
    dict_use = dict()
    for jiao , jl in zip(jd_dp_use['角度2'],jd_dp_use['distance_use']):
        res = Geodesic.WGS84.Direct(lat, lon, jiao, jl)
        if int(jiao)%10==0:
            dict_use[jiao]=res['lon2'], res['lat2']
        points.append((res['lon2'], res['lat2']))
    points.append(points[0])
    pol = Polygon(points)
    return pol
def fcgo(data_t):
    data_t['geometry'] = data_t.apply(lambda x:jm_z(x,mx_900,'RRU经度','RRU纬度'),axis=1)

    return data_t
if __name__ == '__main__':
    threads = []
    with Pool(processes=6) as pool:         # start 4 worker processes
        aa = pd.DataFrame()
        for name , data_t in data_z.groupby('所属地区'):
            print(name,'开始')
            result = pool.apply_async(fcgo, (data_t,)) # evaluate "f(10)" asynchronously in a single process
            threads.append(result)
        pool.close()#防止将更多任务提交到池中。完成所有任务后，工作进程将退出。
        # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的线程加入到pool,
        # join函数等待所有子线程结束
        pool.join()
        for result_t in threads:
            data_tp = result_t.get()
            aa = aa.append(data_tp)
            print(data_tp.shape,aa.shape)
        print(aa.shape)
        aa.to_pickle('res.pkl')
