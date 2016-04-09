#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import socket
import threading

# Usage: python main.py -p 4444

def serveClient(socket, IP, port):
    req = socket.recv(4096)

    print '  %s\n' % req

    # Reply and close
    socket.send('Hi folks! Server v0.1 here (:')
    socket.close()



def startServer(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port)) # Listen on all configured network interfaces
    server.listen(10) # Accept only 10 connections

    print 'Listening locally on port %d...' % port

    while True:
        client, address = server.accept()
        print '\n➜ Connected with client %s:%d:' % (address[0], address[1])

        # Handle clients using multi threading
        serveClientThread = threading.Thread(target=serveClient, args=(client, address[0], address[1]))
        serveClientThread.start()



def main():
    # Parse the command line arguments:
    parser = argparse.ArgumentParser('TCP Server')
    parser.add_argument('-p', '--port', type=int, help='The port number to connect with', default=4444)
    args = parser.parse_args()

    # Call startServer(...) with the -p param:
    startServer(args.port)



if __name__ == '__main__':
    main()
