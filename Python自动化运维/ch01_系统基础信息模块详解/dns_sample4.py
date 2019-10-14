#!/usr/bin/env python
# -*- coding:utf-8 -*-
#实现CNAME记录查询方法

import dns.resolver

domain = raw_input('Please input an domain: ')

cname = dns.resolver.query(domain, 'CNAME')
for i in cname.response.answer:
    for j in i.items:
        print j.to_text()

# [root@NickCOS72V1 python]# python dns_sample4.py
# Please input an domain: www.baidu.com
# www.a.shifen.com.
# [root@NickCOS72V1 python]# python dns_sample4.py
# Please input an domain: www.a.shifen.com
# www.wshifen.com.
# [root@NickCOS72V1 python]# python dns_sample4.py
# Please input an domain: www.wshifen.com
# Traceback (most recent call last):
#   File "dns_sample4.py", line 9, in <module>
#     cname = dns.resolver.query(domain, 'CNAME')
#   File "/usr/lib/python2.7/site-packages/dns/resolver.py", line 1102, in query
#     lifetime)
#   File "/usr/lib/python2.7/site-packages/dns/resolver.py", line 1004, in query
#     raise_on_no_answer)
#   File "/usr/lib/python2.7/site-packages/dns/resolver.py", line 234, in __init__
#     raise NoAnswer(response=response)
# dns.resolver.NoAnswer: The DNS response does not contain an answer to the question: www.wshifen.com. IN CNAME
