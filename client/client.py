# Echo client program
# Course: CSE3320-001
# Author: Minjung Yoo
# Submission Date : May 7, 2015

import os, sys
import sys
import time
import base64
from Crypto.Cipher import AES
from Crypto import Random

login_info =[]
BLOCK_SIZE =32
secret =''

#encrypt message
def encrypt(password):
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    cipher = AES.new(secret)
    return EncodeAES(cipher, password)
#decrypt message
def decrypt(encoded):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(secret)
    return DecodeAES(cipher, encoded)
#read file in encrypted message
def encryptFile(filename):
    filename = filename
    try:
        fo = open(filename,'r')
        s.send(filename)

        line=fo.read()
        encoded=encrypt(line)
        s.send(encoded)
        fo.close()
    except IOError as e:
        print 'error: opening file. please try again'
    except:
        print 'unexpected error:', sys.exc_info()[0]
        raise

#write encrpyted file from server, decrypt message
def GetFile(filename):
    s.send(filename)
    filename = filename.strip('.enc')
    #downloadpath = 'C:\\Users\\min\\Desktop\\lab5_minjungyoo\\client\\downloads\\'
    downloadpath = os.path.abspath('client.py').strip('client.py')+'downloads\\'
    newfile = os.path.join(downloadpath,filename)
    print 'writing ',filename
    try:
        fo = open(newfile,'w')
        fline= decrypt(s.recv(1024))
        fo.write(fline)
        fo.close()
    except IOError as e:
        print 'error: opening/writing file'
    except:
        print 'unexpected error:',sys.exc_info()[0]
        raise


def CheckString (str1,str2):
    if len(str1) is not len(str2):
        return False
    i=0
    for element in str2:
        if (element is not str1[i]):
            return False
        i=i+1
    return True

#get login information from login.txt file, save them in encrypted message
def GetLoginInfo(secret):
    fo = open("login.txt", "r")
    for line in fo.readlines():
        i=0
        line = line.strip()
        parts = line.split(",")
        array =[]
        for part in parts:
            array.append(encrypt(part))
        login_info.append(array)

#check encrypted user information
def CheckLoginInfo(userID,password):
    for i in login_info:
        if CheckString(i[0],userID) and CheckString(i[1],password):
            return True
    return False

#get file size
def GetFileSize(filename):
    return os.stat(filename).st_size

#update file list (path:server/file)
def Update(path):
    dirs = os.listdir(path)
    print '\nupdate file list...'
    for files in dirs:
        pathname = path+files
        statinfo = os.stat(pathname)
        print files,"   ",time.ctime(statinfo.st_mtime),"   ",GetFileSize(pathname),"bytes"

def Switch(answer):
    if answer is '1':
        s.send('1')
        filename = raw_input('File name? ')
        encryptFile(filename)
        return 1
    elif answer is '2':
        s.send('2')
        filename = raw_input('File name? ')
        GetFile(filename)
        return 1
    elif answer is '3':
        Update(path)
        return 1
    elif answer is '4':
        print 'close the client...'
        s.send(answer)
        s.close()
        exit(1)
    else:
        print 'error: incorrect input. please try again'
        return 1


# menu
def PrintMenu():
    flag =1
    while flag:
        print '\n1. put file'
        print '2. get file'
        print '3. update filelist'
        print '4. exit'
        answer= raw_input('Please enter the number of options: ')
        flag = Switch(answer)


#main
import socket

s=socket.socket()
HOST = socket.gethostname()
PORT = 9702
s.connect((HOST,PORT))

print s.recv(1024)
secret = s.recv(1024)

#Get user information from file in client directory
GetLoginInfo(secret)

#Check login information from server
userID= s.recv(1024)
if CheckLoginInfo(userID,s.recv(1024)) is False:
    print 'Wrong login information. Please try again'
    exit(1)

print 'user verified'   #login success

path = s.recv(1024)
Update(path)
PrintMenu()

s.close()
