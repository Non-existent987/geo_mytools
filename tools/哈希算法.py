import hashlib

db = {}

#计算密码的md5值
def get_md5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

#注册新的用户
def register(username,password):
    db[username] = get_md5(password + username + 'SSC')
    return db[username]

#验证用户登录
def login(username,password):
    if not username in db:
        print('用户不存在')
        return
    if db[username] == get_md5(password + username + 'SSC'):
        print('登录成功')
    else:
        print('密码错误')

#主程序
if __name__ == '__main__':
    user1 = 'xiaoming'
    psw1 = '123456'
    a = register('helong','123')  #注册新用户
    print(a)
    login('helong','123')     #登录成功
    login(user1,psw1+' ')  #密码错误，登录失败
    login(user1+' ',psw1)  #用户名错误，登录失败