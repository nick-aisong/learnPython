#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 根据输人的IP或子网返回网络、掩码、广播、反向解析、子网数、IP类型等信息

from IPy import IP

ip_s = raw_input('Please input an IP or net-range: ')
ips = IP(ip_s)

if len(ips) > 1:
    print('net: %s' % ips.net())
    print('netmask: %s' % ips.netmask())
    print('broadcast: %s' % ips.broadcast())
    print('reverse address: %s' % ips.reverseNames()[0])
    print('subnet: %s' % len(ips))
else:
    print('reverse address: %s' % ips.reverseNames()[0])

print('hexadecimal: %s' % ips.strHex())
print('binary ip: %s' % ips.strBin())
print('iptype: %s' % ips.iptype())

# [root@NickCOS72V1 python]# python ipy_sample1.py
# Please input an IP or net-range: 192.168.1.0/24
# net: 192.168.1.0
# netmask: 255.255.255.0
# broadcast: 192.168.1.255
# reverse address: 1.168.192.in-addr.arpa.
# subnet: 256
# hexadecimal: 0xc0a80100
# binary ip: 11000000101010000000000100000000
# iptype: PRIVATE

# [root@NickCOS72V1 python]# python ipy_sample1.py
# Please input an IP or net-range: 192.168.1.20
# reverse address: 20.1.168.192.in-addr.arpa.
# hexadecimal: 0xc0a80114
# binary ip: 11000000101010000000000100010100
# iptype: PRIVATE
