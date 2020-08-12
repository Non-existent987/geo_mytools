import uuid,hashlib,pickle,time,datetime
from os.path import exists
from os import makedirs
def get_secort(mac_ads):
    namespace = uuid.uuid1()
    md5 = hashlib.md5()
    md5.update(mac_ads.encode("utf-8"))
    return md5.hexdigest()

if __name__=='__main__':
    if not exists(r"d:/Users/NR_Interfence/licf"):
        makedirs(r"d:/Users/NR_Interfence/licf")
    login_path = r"d:/Users/NR_Interfence/licf"
    address = hex(uuid.getnode())[2:]
    #获取本机MAC并加密生成license
    mac_ads='-'.join(address[i:i+2] for i in range(0, len(address), 2))
    mac_ads = get_secort(mac_ads.strip())
    #手动输入MAC并加密生成license
    # mac_ads='1b2cc3efb9bc87a2c5975d1af15e9d41'
    pick_path=(login_path+'/'+f"{mac_ads}.key")
    pid = get_secort(mac_ads.strip())
    username=input('请输入用户名: ')
    password=get_secort(input('请输入密码(不少于6位数): '))
    time1=datetime.date.today()
    time2=time1+datetime.timedelta(days=120)
    with open(pick_path,'wb') as user_file:
        user_info={get_secort('username'):username,
                   get_secort('password'):password,
                   get_secort('macid'):pid,
                   get_secort('start_time'):time1,
                   get_secort('end_time'):time2}
        pickle.dump(user_info,user_file)
