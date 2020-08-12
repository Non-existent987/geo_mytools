from python_up_d import *
import os 
import socket,uuid

ssh = SSHConnection()
ssh.connect(host='121.41.2.208',port=22, username='root',pwd='Helong123')
# ssh.cmd("ls")
# ssh.upload('d:/ddd.txt','/root/root_helong/ks77.txt')
ssh.download('/root/root_helong/ks77.txt','ks77.txt')
f = open('ks77.txt','r')
# a = f.read()
list_name=[]
for x in f:
    list_name.append(x)
# print(a)
print('-------------n',list_name)
print(list_name[0])
if 'v-0.1\n' == list_name[0]:
    print('相等')
    ssh.download('/root/root_helong/GB2UTF8.exe','GB2UTF8.exe')
    main = "GB2UTF8.exe"
    r_v = os.system(main) 
    print (r_v )
ip = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
ip = ip[ip.find(':')+1:ip.find('\n')]
print(ip)

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

#获取本机电脑名
myname = socket.getfqdn(socket.gethostname(  ))
#获取本机ip
myaddr = socket.gethostbyname(myname)
print(myname)
print(myaddr)
print(get_mac_address())

# ssh.cmd("df")
# ssh.close()