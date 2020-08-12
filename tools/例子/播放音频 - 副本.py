import winsound
import struct
import array
import dog
import base64
tmp = open("tmp.wav","wb+")  
tmp.write(base64.b64decode(dog.dog))#写入到临时文件中
tmp.close()
winsound.PlaySound(base64.b64decode(dog.dog), winsound.SND_FILENAME)
encodestr = base64.b64encode(sound_wav_rb)


# # 读取wav文件，二进制要记得用b
# file = open('dog.wav', 'rb')
# # 获取前44个字节，文件信息。
# info = file.read(44)
# # 获取文件大小， 将指针移动到文件末尾
# file_size = file.seek(0, 2)
# # 计算数组大小
# n = (file_size - 44) // 2
# # 生成buf
# buf = array.array('h', (0 for _ in range(n)))
# # 将文件指针定位到44
# file.seek(44)
# # 将数据读入到buf中
# file.readinto(buf)
# # 将声音变小
# for i in range(n):
# #     buf[i] //= 10
# # 写入数据
# f = open('demo3.wav', 'wb')
# # f.write(info)
# dog.dog.tofile(f)
# # 关闭文件
# f.close()
# # file.close()
