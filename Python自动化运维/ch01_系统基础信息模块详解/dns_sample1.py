#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 实现A记录查询方法

import dns.resolver

domain = raw_input('Please input an domain: ')

A = dns.resolver.query(domain, 'A')
for i in A.response.answer:
    for j in i.items:
        print j.address

# [root@NickCOS72V1 python]# python dns_sample1.py
# Please input an domain: www.google.com
# 172.217.12.36

# [root@NickCOS72V1 python]# python dns_sample1.py
# Please input an domain: www.baidu.com
# Traceback (most recent call last):
#   File "dns_sample1.py", line 12, in <module>
#     print j.address
# AttributeError: 'CNAME' object has no attribute 'address'

# [root@NickCOS72V1 python]# python dns_sample1.py
# Please input an domain: www.wshifen.com
# 104.193.88.77
# 104.193.88.123
