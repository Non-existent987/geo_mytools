from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
fig = plt.figure()
ax = Axes3D(fig)
x = [0,1,1,0]
y = [0,0,1,1]
z = [0,1,0,1]
verts = [list(zip(x,y,z))]
ax.add_collection3d(Poly3DCollection(verts))
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def himmelblau(x):
#     return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2

# x = np.linspace(-6, 6, 200)
# y = np.linspace(-6, 6, 200)
# X, Y = np.meshgrid(x, y)

# fig = plt.figure(figsize=(12, 10))
# ax = fig.gca(projection='3d')
# ax.plot_surface(X, Y, Z)   # 画曲面
# # ax.plot(X, Y, Z)       # 画曲线，好像x， y得是一维的
# ax.view_init(60, -30)       # 好像是调成图的角度
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# plt.show()
