#消息接收端--服务器端
 
import socket
# 创建一个socket，用函数socket()
client_send = socket.socket(type=socket.SOCK_DGRAM)
# 绑定IP地址、端口等信息到socket上，用函数bind();
ip_port = ("10.11.53.74",10086)
client_send.bind(ip_port)
# 循环接收数据，用函数recvfrom();
data,addr = client_send.recvfrom(1024)
print(str(data,encoding="utf-8"))
# 关闭网络连接
client_send.close()