#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现MX记录查询方法

import dns.resolver

domain = raw_input('Please input an domain: ')

MX = dns.resolver.query(domain, 'MX')
for i in MX:
    print 'MX preference =', i.preference, 'mail exchanger =', i.exchange

# [root@NickCOS72V1 python]# python dns_sample2.py
# Please input an domain: baidu.com
# MX preference = 15 mail exchanger = mx.n.shifen.com.
# MX preference = 20 mail exchanger = mx1.baidu.com.
# MX preference = 20 mail exchanger = jpmx.baidu.com.
# MX preference = 20 mail exchanger = mx50.baidu.com.
# MX preference = 10 mail exchanger = mx.maillb.baidu.com.
