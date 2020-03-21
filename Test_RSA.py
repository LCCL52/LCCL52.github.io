#-*- coding：UTF-8 -*-
from random import randint
import random
import base64
import re
import math
import sys

def  charToAscii(message):       #将字符转化为ASCII码
  Output = []
  for i in message:
      Output.append(ord(i))
  return Output

                                  #将ASCII码变为十六进制
def AsciiToHex(message):
  Output = ''
  for each in message:
    Output = Output + str(hex(each)).split('x')[1]
  return Output


def Hex_to_dec(hexnumber):        #16进制字符串转化为十进制
    decnumber = int(hexnumber,16)
    return decnumber



def dec_to_Hex(decumber):          #十进制转化为十六进制
    hexnumber = hex(decumber)
    return hexnumber



def big_P_Q():                  #产生两个大素数
    flag = 0
    while not flag:
        p = random.randrange(10**10,10**11)

        if charge_sushu_1(p) and _ack(2,p):

            q = random.randrange(p,10**11)
            if charge_sushu_1(q) and p != q and _ack(2,q):
                flag = 1
    return p,q







def fastExpMod(b, e, m):          #快速求模
    result = 1
    while e != 0:
        if (e&1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e >>= 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b*b) % m
    return result

def gcd(a,b):                     #判断互素
    if a<b:
        a,b = b,a
    while b != 0:
        temp = a%b
        a = b
        b = temp
    return (a,b)


def find_e(En):                     #寻找e
    while 1:
        e = random.randrange(10000)
        if gcd(e,En) == (1,0):
            break

    return e

def find_d(e,s):                    #求d

    u1, u2, u3 = 1, 0, e
    v1, v2, v3 = 0, 1, s
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % s

def charge_sushu_1(n):
    Sushu = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41
                 , 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    for y in Sushu:
        if n % y == 0:
            return False
    return True

def _ack(a,n):

    a1 = pow(17-a,n,n)
    a2 = pow(17,n,n) - (a%n)
    if a1 == a2:
        return 1
    else:
        return 0

def charge_sushu_2(n, k):
    if n < 2:
           return False
    d = n - 1
    r = 0
    while not (d & 1):
            r += 1
            d >>= 1
    for i in range(k):
            a = randint(120)        #随机数
            x = fastExpMod(a, d, n)
            if x == 1 or x == n - 1:
                    continue
            for i in range(r - 1):
                    x = fastExpMod(x, 2, n)
            if x == 1:
                    return False
            if x == n - 1:
                    break
    else:
            return False
    return True


def create_key():  #生成公钥和私钥保存为txt
    p = big_P_Q()[0]
    q = big_P_Q()[1]
    n = p * q
    En = (p - 1) * (q - 1)
    e =find_e(En)
    d = int(find_d(e,En))
    with open("id_rsa_pub.txt", "w") as file:
        file.write("[%s, %s]" % (e, n))
    with open("id_rsa.txt", "w") as file:
        file.write("[%s, %s]" % (d, n))



def encryption():  #加密
    try:
        with open("id_rsa_pub.txt") as file:
            rsa = file.read()[1:-1].split(", ")
            print(rsa)
    except FileNotFoundError:
        print("Public key not found, please confirm")
    else:
        with open('Message.txt', 'r') as f:  # 读取明文
            plaindata = f.read()
            f.close()
     # base64转码，解决中文加密问题
        plaindata=str(base64.b64encode(plaindata.encode("utf-8")))
        print(plaindata)
        f_cipher = []
        for i in range(0, len(plaindata), 8):  # 明文分组
            # print(plaindata[i:i+8])
            cut_plain = Hex_to_dec(AsciiToHex(charToAscii(plaindata[i:i + 8])))
            print("明文分组：", cut_plain)
            cipher = fastExpMod(cut_plain, int(rsa[0]), int(rsa[1]))
            str_cipher_cut = str(dec_to_Hex(cipher))
            #print(str_cipher_cut)
            f_cipher.append(str_cipher_cut)
        str_cipher = ''.join(f_cipher)
        with open('secret.txt', 'w') as f:  # 写入密文
            f.write(str_cipher)
            f.close()
        print("密文为：", str_cipher)
        print("加密成功！")
        print("请查看secret.txt文件")

def Decrypt():   #解密
    try:
        with open("id_rsa.txt") as file:
            rsa = file.read()[1:-1].split(", ")
    except FileNotFoundError:
        print("Private key not found, please confirm")
    else:
        try:
            with open('secret.txt', 'r') as f:       # 读取密文
                cipher = f.read()
                f.close()
        except FileNotFoundError:
            print("encrypted text not found, please confirm")
        else:
            f_plain = cipher.split('0x')
            print(len(f_plain))
            f_cut_plain = []
            for i in range(1,len(f_plain)):
                # print(f_plain[i])
                dec_cipher = Hex_to_dec(f_plain[i])
                cut_plain = fastExpMod(dec_cipher, int(rsa[0]),int(rsa[1]))        #进行解密
                # print(cut_plain)
                str_plain_cut = str(dec_to_Hex(cut_plain))[2:]
                f_cut_plain.append(str_plain_cut)
            plain = ''.join(f_cut_plain)
            str_plain = str(plain)
            a1 = []                                                    # 写入明文
            for i in range(0, len(str_plain), 2):
                b = str_plain[i:i + 2]
                a1.append(chr(int(b, 16)))
            str_plain_char = ''.join(a1)
            s_plain_char=str(str_plain_char)
            bs=s_plain_char
           # print(bs)         正则表达式提取引号里的内容，如何再进行base64转码
            pattern = re.compile("'(.*)'")
            a = pattern.findall(bs)
            print(a)
            bbs = str(base64.b64decode(a[0]), "utf-8")
            with open('Decrypted.txt','w') as f:
                f.write(bbs)
                f.close()
            print("解密的明文为：", bbs)
            print("解密成功！")
            print("请查看Decrypted.txt文件")
if __name__ == '__main__':
    create_key()
    encryption()
    Decrypt()





