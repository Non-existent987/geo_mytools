from tvtk.api import tvtk
 
# 三维数据源
s = tvtk.CubeSource(x_length=1.0, y_length=2.0, z_length=3.0)
 
print("s= \n",s)
 
# 将三维数据源映射为二维图形显示
m = tvtk.PolyDataMapper(input_connection = s.output_port)
print("m=\n",m)
 
# 创建一个显示实体
a = tvtk.Actor(mapper=m)
print("a= \n",a)
# 创建一个渲染器
r = tvtk.Renderer(background=(0,0,0))
print("r= \n",r)
# 添加显示实体
r.add_actor(a)
 
# 创建一个显示窗口
w = tvtk.RenderWindow(size=(300,300),position=(300,300))
print("w= \n",w)
# 添加渲染器
w.add_renderer(r)
 
# 创建一个交互器
i = tvtk.RenderWindowInteractor(render_window=w)
print("i= \n",i)
 
# 初始化交互器
i.initialize()
# 启动
i.start()