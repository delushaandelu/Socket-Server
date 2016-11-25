#!/usr/bin/python

import socket
import signal
import time 

class Server:
    
 def __init__(self, port = 10500):
     """ Constructor """
     self.host = ''
     self.port = port
     self.www_dir = 'src'

 def activate_server(self):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try:
         print "Starting HTTP server on ", self.host, ":",self.port
         self.socket.bind((self.host, self.port))

     except Exception as e:
         print "Warning: Could not find a port:",self.port,"\n"
         print "Trying a upward port"
         user_port = self.port
         self.port = 8080

         try:
             print "Starting HTTP server on ", self.host, ":",self.port
             self.socket.bind((self.host, self.port))

         except Exception as e:
             print "ERROR: Failed to turn sockets for ports ", user_port, " and 8080. "
             print "Try running the Server in a privileged client mode."
             self.shutdown()
             import sys
             sys.exit(1)

     print "Server successfully turned on the socket with port:", self.port
     self._wait_for_connections()

 def shutdown(self):
     try:
         print "Stopping down the server..."
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print "Warning: could not shut down the socket!",e

 def _gen_headers(self,  code):
     hosting = ''
     if (code == 200):
        hosting = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        hosting = 'HTTP/1.1 404 Not Found\n'
     
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     hosting += 'Date: ' + current_date +'\n'
     hosting += 'Server: Rushan WebServer\n'
     hosting += 'Connection: stop\n\n' 

     return hosting
    
 def _wait_for_connections(self):
     while True:
         print "Awaiting for New connection..."
         self.socket.listen(1)

         conn, addr = self.socket.accept()
         
         print "Got new connection from:", addr

         data = conn.recv(1024)
         string = bytes.decode(data)

         
         request_method = string.split(' ')[0]
         print "Request Method: ", request_method
         print "Request body: ", string
         
         if (request_method == 'GET') | (request_method == 'HEAD'):
             file_requested = string.split(' ')
             file_requested = file_requested[1]
             
             file_requested = file_requested.split('?')[0]

             if (file_requested == '/'):  
                 file_requested = '/index.html' 

             file_requested = self.www_dir + file_requested
             print "Serving web page [",file_requested,"]"

             
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):
                     response_content = file_handler.read() 
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e:
                 print "Warning, file not found. Serving response code 404:ERROR\n", e
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'GET'):
                    response_content = "<html><body><center></br></br></br></br></br></br></br></br></br></br><font color='red'><h1>Error 404: File not found</h1><p>LOCAL SERVER: ERROR: invalid format of file</p></font></center></body></html>"

             server_response =  response_headers.encode()
             if (request_method == 'GET'):
                 server_response +=  response_content  

             conn.send(server_response)
             print "server response:"
             print server_response
             print "Closing connection with client call"
             print ""
             conn.close()

         else:
             print "Unidentificial HTTP request method:", request_method

print ("Starting new web server")
s = Server(10500)
s.activate_server()
