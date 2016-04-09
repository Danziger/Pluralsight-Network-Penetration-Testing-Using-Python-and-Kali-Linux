#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from socket import *

# To test it against a TCP server, use the TCP Server under '003 - TCP Server'
# To test it against a UDP server, use 'netcat -v -l -u -p 5555'
# -v Verbose, -l Listen, -u UDP, -p Port
# You will be able to send back whatever you want once a client connects to the
# UPD server just by typing it into the terminal window.

# Usage: python main.py -a 192.168.0.1 -p 21,80 [--udp]

def printBanner(connSock, tgtPort):
    try:
        # Send data to target:
        if tgtPort == 80:
            connSock.send('GET HTTP/1.1 \r\n')
        else:
            connSock.send('\r\n')

        # Receive data from target & print the banner
        print str(connSock.recv(4096))
    except:
        print '✖ Banner not available'



def connScanUDP(tgtHost, tgtPort):
    try:
        # Create the socket object
        connSock = socket(AF_INET, SOCK_DGRAM) # Meaning: IPv4, UDP

        # Try to connect with the target
        connSock.connect((tgtHost, tgtPort))

        print '➜ %d UDP open...:' % tgtPort
        printBanner(connSock, tgtPort)
    except:
        # Print the failure results
        print '✖ %d UDP closed' % tgtPort
    finally:
        # Close the socket
        connSock.close()



def connScanTCP(tgtHost, tgtPort):
    try:
        # Create the socket object
        connSock = socket(AF_INET, SOCK_STREAM) # Meaning: IPv4, TCP

        # Try to connect with the target
        connSock.connect((tgtHost, tgtPort))

        print '➜ %d TCP open...:' % tgtPort
        printBanner(connSock, tgtPort)
    except:
        # Print the failure results
        print '✖ %d TCP closed' % tgtPort
    finally:
        # Close the socket
        connSock.close()



def portScan(tgtHost, tgtPorts, isUDP):
    try:
        # if -a was not an IP address this will resolve it to an IP
        tgtIP = gethostbyname(tgtHost)
    except:
        print '✖ ERROR: Unknown Host'
        exit(0)

    try:
        # We try to resolve the domain
        tgtName = gethostbyaddr(tgtIP)
        print 'Scanning ' + tgtName + '...'
    except:
        print 'Scanning ' + tgtIP + '...'

    # https://docs.python.org/2/library/socket.html
    setdefaulttimeout(None)    # This is already the default TODO: Use an arg for this

    # For each port number call the connScan function:
    # TODO: Use multithreading here!
    if isUDP:
        for tgtPort in tgtPorts:
            connScanUDP(tgtHost, int(tgtPort))
    else:
        for tgtPort in tgtPorts:
            connScanTCP(tgtHost, int(tgtPort))



def main():
    # TODO: Use multiple IPs!
    # Parse the command line arguments:
    parser = argparse.ArgumentParser('TCP/UDP Port Scanner')
    parser.add_argument('-a', '--address', type=str, help='The target IP adrdess')
    parser.add_argument('-p', '--port', type=str, help='The port number to connect with')
    parser.add_argument('-u', '--udp', help='Include a UDP port scan', action='store_true')
    args = parser.parse_args()

    # Store the arguments values:
    ipaddress = args.address
    portNumbers = args.port.split(',')
    isUDP = args.udp

    # Call the portScan(...):
    portScan(ipaddress, portNumbers, isUDP)



if __name__ == '__main__':
    main()
