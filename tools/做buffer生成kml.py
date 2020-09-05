# 做buffer生成kml

data = pd.read_clipboard()
data_buffer = mytools.gisn.add_buffer(data,'lon','lat',100)

# 设置
#导出目录
otu_file = 'd:/res.kmz'
#- 标注 -添加标注列
de_col = list(data.columns)
data_buffer['description']=''
for inde_1, name_1 in enumerate(de_col):
    data_buffer['linshi']=de_col[inde_1]+' : '+data[de_col[inde_1]].astype('str')+'\n'
    data_buffer['description'] = data_buffer['description']+data_buffer['linshi']
    data_buffer.drop(columns='linshi')
#固定变量
xiankuan = 1
#最终使用的列
data_use = data_buffer.reindex(columns=['id', 'colour','description','geometry'])   

# 生成图层
kml = simplekml.Kml()
dic_use = {'红':'ff0000ff','蓝':'ffff0000','黄':'ff00ffff','白':'ffffffff','绿':'ff008000'}
for colourname,data_t in data_buffer.groupby('colour'):
    out_file_use = otu_file+'_'+colourname+'.kml'
    style = simplekml.Style()
    colour_str = dic_use[colourname]
    style.linestyle.color = simplekml.Color.changealphaint(220, colour_str)  # 最终线条上色
    style.polystyle.outline = xiankuan
    style.polystyle.color = simplekml.Color.changealphaint(125, colour_str )  # 最终形状上色
    grid_red = kml.newfolder(name=colourname)
    for id_use,des_use,geo in zip(data_t['id'],data_t['description'],data_t['geometry']):
        pol_r = grid_red.newmultigeometry(name=id_use)
        pol_r.newpolygon(outerboundaryis=list(geo.exterior.coords),innerboundaryis=[po.coords for po in list(geo.interiors)])
        pol_r.description = des_use
        pol_r.altitudemode = simplekml.AltitudeMode.clamptoground
        pol_r.style=style
    print(colourname,'色，制作完成')
#     kml.save(out_file_use) if 'kml' in out_file_use else kml.savekmz(out_file_use, False)
kml.save(otu_file) if 'kml' in otu_file else kml.savekmz(otu_file, False)
print('程序结束')