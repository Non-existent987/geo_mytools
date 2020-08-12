# -*- coding:utf-8 -*-
import paramiko
import uuid
 
class SSHConnection(object):
 
    def __init__(self, host='121.41.2.208', port=22, username='root',pwd='Helong123'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
 
    def connect(self,host,port,username,pwd):
        transport = paramiko.Transport((host,port))
        transport.connect(username=username,password=pwd)
        self.__transport = transport
 
    def close(self):
        self.__transport.close()
 
    def upload(self,local_path,target_path):
        # 连接，上传
        # file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)
 
    def download(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path,local_path)
 
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result,encoding='utf-8'))
        return result
 
# ssh = SSHConnection()
# ssh.connect()
# ssh.cmd("ls")
# ssh.upload('s1.py','/tmp/ks77.py')
# ssh.download('/tmp/test.py','kkkk',)
# ssh.cmd("df")
# ssh.close()