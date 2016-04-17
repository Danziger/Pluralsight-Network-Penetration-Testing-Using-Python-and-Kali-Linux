#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import pygeoip
from IPy import IP as IPLIB
from socket import *
import time



conversations = {}
exclude_IPs = ['10.0.0.18', '127.0.0.1']



def saveToFile(traceInfo):
    try:
        # Create the file log object
        filename = 'ntw-mon-log-' + time.strftime('%Y.%m.%d') + '.txt'
        fileLog = open(filename, 'a')

        # Write the trace information to the file
        fileLog.write(traceInfo)
        fileLog.write('\r\n----------------\r\n')

        fileLog.close()
    except:
        pass

def getInfo(IPaddr):
    try: # Try to resolve the IP addr
        hostName = gethostbyaddr(IPaddr)[0]
    except:
        hostName = 'UNRESOLVED'

    # Convert IP to a valid IP object
    ip = IPLIB(IPaddr)

    # Do not proceed if the IP is private
    if ip.iptype() == 'PRIVATE':
        return 'Private IP, Host Name: ' + hostName

    try:
        # Iniialize the GEOIP object
        geoIP = pygeoip.GeoIP('GeoIP.dat')

        # Get the record info
        ipRecord = geoIP.record_by_addr(IPaddr)

        # Extract the country name
        return 'Country: %s, Host: %s' % (ipRecord['country_name'], hostName)
    except Exception, ex:
        # GeoIP could not locate the IP addr
        return 'Can\'t locate %s, Host: %s' % (IPaddr, hostName)

def printPacket(srcIP, dstIP):
    traceInfo = 'SRC %s: %s → DST %s: %s' % (srcIP, getInfo(srcIP), dstIP, getInfo(dstIP))
    print traceInfo
    saveToFile(traceInfo)

def startMonitoring(pkt):
    try:
        if pkt.haslayer(IP):
            # Get the source and destination IP addresses
            srcIP = pkt.getlayer(IP).src
            dstIP = pkt.getlayer(IP).dst

            if dstIP in exclude_IPs:
                return

            # Generate a unique key to avoid duplication
            uniqueKey = srcIP + dstIP

            # Skip already processed packets
            if not conversations.has_key(uniqueKey):
                # Store a flag in the array to avoid duplication
                conversations[uniqueKey] = True
                printPacket(srcIP, dstIP)
    except Exception, ex:
        print 'Exception: ' + str(ex)
        pass

def main():
    # Start sniffing by filtering only the IP packets without storing anything inside memory:
    sniff(prn=startMonitoring, store=0, filter='ip')

if __name__ == '__main__':
    main()