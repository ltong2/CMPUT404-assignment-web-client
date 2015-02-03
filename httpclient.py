#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
	if port == None:
		port=80
	if host == None:
		host ="localhost"
	con=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		con.connect((host,port))
	except:
		print("Connection failed, host name: \n"+ host+" with port "+str(port))
		sys.exit()
        return con

    def get_code(self, data):
	var=data.split()
	try:
		num=int(var[1])
	except:
		num=200
        return num

    def get_headers(self,data):
	var=data.split("\r\n\r\n",2)
	num1=var[0]
        return num1

    def get_body(self, data):
	try:
		var=data.split("\r\n\r\n",2)
		num2=var[1]
	except:
		var=data.split("<head>")
		num2=var[1]
        return num2

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def send_reponse(self,host,port,reply):

	create_connection=self.connect(host,port)
	create_connection.send(reply)

	res=self.recvall(create_connection)
	return res


    def GET(self, url, args=None):

	url_breake=urlparse(url)


	reply="GET %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nConnection: close\r\n\r\n" % (url_breake.path,url_breake.hostname) 
	res=self.send_reponse(url_breake.hostname,url_breake.port,reply)

	return HTTPRequest(self.get_code(res), self.get_body(res))


    def POST(self, url, args=None):
	url_breake=urlparse(url)
	con=""
	if (args != None):
		con = urllib.urlencode(args)
	else:
		con = ""


	reply = "POST %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %d\r\n\r\n%s\r\n" % (url_breake.path,url_breake.hostname,len(con),con)
	res=self.send_reponse(url_breake.hostname,url_breake.port,reply)

	return HTTPRequest(self.get_code(res), self.get_body(res))	

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1],command )     
