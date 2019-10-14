#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现NS记录查询方法

import dns.resolver

domain = raw_input('Please input an domain: ')
ns = dns.resolver.query(domain, 'NS')
for i in ns.response.answer:
     for j in i.items:
          print j.to_text()

# [root@NickCOS72V1 python]# python dns_sample3.py
# Please input an domain: baidu.com
# ns4.baidu.com.
# ns3.baidu.com.
# ns7.baidu.com.
# ns2.baidu.com.
# dns.baidu.com.
