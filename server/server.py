# Echo server program
# Course: CSE3320-001
# Author: Minjung Yoo
# Submission Date : May 7,2015

import socket
import base64
import os,sys
import sys
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 32
secret = os.urandom(BLOCK_SIZE)

#need to fix path if path is different location 
#path = 'C:\\Users\\min\\Desktop\\lab5_minjungyoo\\server\\file\\'

path = os.path.abspath('server.py').strip('server.py')+'file\\'

def encrypt(password,secret):
    
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    #DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(secret)
    return EncodeAES(cipher, password)

#update path and send it to client
def Update():

    c.send(path)

def CheckString (str1,str2):
    if len(str1) is not len(str2):
        return False
    i=0
    for element in str2:
        if (element is not str1[i]):
            return False
        i=i+1
    return True

def Switch(num):
    if CheckString(num,'1'):
        filename = c.recv(1024)+'.enc'
        newfile = os.path.join(path,filename)
        print 'uploading ',filename
        try:
            fo = open(newfile,'w')
            fline = c.recv(1024)
            fo.write(fline)
            fo.close()
        except IOError as e:
            print 'error: opening/writing file'
        except:
            print 'unexpected error:',sys.exc_info()[0]
            raise

    elif CheckString(num,'2'):
        filename = c.recv(1024)
        try:
            newfile = os.path.join(path,filename)
            print 'sending ',filename

            fo = open(newfile,'r')
            line = fo.read()
            c.send(line.strip('\n'))
            fo.close()
        except IOError as e:
            print 'error:opening file'
    elif CheckString(num,'4'):
        print 'Good Bye!'
        c.close()
        exit(1)

# main
s = socket.socket()

HOST = socket.gethostname()    
PORT = 9702

s.bind((HOST, PORT))
s.listen(5)

print 'server waiting...\n'
c,addr = s.accept()
print 'connected from (127.0.0.1, 9734)'
c.send('thanks for connecting') #connecting success
c.send(secret)
    
#ask for login information; send it to client
c.send(encrypt(raw_input('User ID: '),secret))
c.send(encrypt(raw_input("password: "),secret))

Update()

while 1:
    num= c.recv(1024)
    Switch(num)
