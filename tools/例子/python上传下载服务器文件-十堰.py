from python_up_d import *
ssh = SSHConnection()
ssh.connect(host='121.41.2.208',port=22, username='root',pwd='Helong123')
# ssh.cmd("ls")
# ssh.upload('d:/ddd.txt','/root/root_helong/ks77.txt')
ssh.download('/root/root_helong/ks77.txt','ks77.txt')
# ssh.cmd("df")
# ssh.close()