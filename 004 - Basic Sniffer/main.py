#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
from ctypes import *



class IPHeader(Structure):

    _fields_ = [
        ('ihl',             c_ubyte, 4),
        ('version',         c_ubyte, 4),
        ('tos',             c_ubyte),
        ('len',             c_ushort),
        ('id',              c_ushort),
        ('offset',          c_ushort),
        ('ttl',             c_ubyte),
        ('protocol_num',    c_ubyte),
        ('sum',             c_ushort),
        ('src',             c_uint32),
        ('dst',             c_uint32)
    ]

    def __new__(self, data=None):
        return self.from_buffer_copy(data)

    def __init__(self, data=None):
        # Map source and destination IP addresses
        self.source_address = socket.inet_ntoa(struct.pack('@I', self.src))
        self.destination_address = socket.inet_ntoa(struct.pack('@I', self.dst))

        # Map protocol constants
        # TODO: Extend protocol support
        self.protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

        # Get protocol name
        try:
            self.protocol = self.protocols[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

def initTCPSocket():
    # Create the socket object
    sniffer_TCP = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    # Bind it to localhost
    sniffer_TCP.bind(('0.0.0.0', 0))

    # Include the IP header
    sniffer_TCP.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    return sniffer_TCP

def startSniffing():
    # TCP
    sniffer_TCP = initTCPSocket()

    print 'Sniffer is listening for incoming connections...'

    try:
        while True:
            raw_buffer_TCP = sniffer_TCP.recvfrom(65535)[0]
            IP_header_TCP = IPHeader(raw_buffer_TCP[0:20])

            if IP_header_TCP.protocol == 'TCP':
                print '%s\t%s → %s' % (IP_header_TCP.protocol, IP_header_TCP.source_address, IP_header_TCP.destination_address)

    except KeyboardInterrupt:
        print 'Exiting program...'
        exit(0)

def main():
    startSniffing()

if __name__ == '__main__':
    main()