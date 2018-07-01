from Crypto.Cipher import AES
import os
import pickle

#存储加密后的信息
info=[]

def to16Bytes(s):
    return (s+'\0'*(16-len(s)%16)).encode()
def EncryptAES(key,strS):
    aes=AES.new(to16Bytes(key),AES.MODE_ECB)
    encodeS=aes.encrypt(to16Bytes(strS))
    return encodeS
def DecriptAES(key,byteS):
    aes=AES.new(to16Bytes(key),AES.MODE_ECB)
    decodeS=aes.decrypt(byteS).decode().strip('\0')
    return decodeS
def addPassword(key,message,userName,password):
    if message=='' or userName=='' or password=='':
        return False
    hasIn=False
    for i,row in enumerate(info):
        if message==DecriptAES(key,row[0]) and userName==DecriptAES(key,row[1]):
            hasIn=True
            p=i
            break 
    if not hasIn:
        print((message,userName,password),'has been added in the list.')
        info.append([EncryptAES(key,message),EncryptAES(key,userName),EncryptAES(key,password)])
    else:
        print((DecriptAES(key,row[0]),DecriptAES(key,row[1]),DecriptAES(key,row[2])),'is updated by',(message,userName,password))
        info[p]=[EncryptAES(key,message),EncryptAES(key,userName),EncryptAES(key,password)]
    return True

def lookPassword(key,message,userName):
    for row in info:
        r0=DecriptAES(key,row[0])
        r1=DecriptAES(key,row[1])
        r2=DecriptAES(key,row[2])
        if message=='' or (r0==message and userName=='') or (r0==message and r1==userName):
            print(r0,r1,r2)

if os.path.exists('info.pkl'):
    with open('info.pkl','rb') as f:
        info=pickle.load(f)
key=input('Input the key:')
while(True):
    oper=input('Input the operation(add or look or nothing):')
    if oper=='add':
        message=input('Input the message:')
        userName=input('Input the userName:')
        password=input('Input the password:')
        addPassword(key,message,userName,password)
    elif oper=='look':
        message=input('Input the message:')
        userName=input('Input the userName:')
        lookPassword(key,message,userName)
    elif oper=='':
        with open('info.pkl','wb') as f:
            pickle.dump(info,f)
        print('Writed')
        break