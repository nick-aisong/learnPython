>>> import nmap
>>> nm = nmap.PortScanner()
>>> nm.scan('16.155.194.52-53', '22,80')
{'nmap': {'scanstats': {'uphosts': '2', 'timestr': 'Mon Oct 14 17:52:06 2019', 'downhosts': '0', 'totalhosts': '2', 'elapsed': '1.55'}, 'scaninfo': {'tcp': {'services': '22,80', 'method': 'syn'}}, 'command_line': 'nmap -oX - -p 22,80 -sV 16.155.194.52-53'}, 'scan': {'16.155.194.52': {'status': {'state': 'up', 'reason': 'localhost-response'}, 'hostnames': [{'type': 'PTR', 'name': 'nickcos72v1.hpeswlab.net'}], 'vendor': {}, 'addresses': {'ipv4': '16.155.194.52'}, 'tcp': {80: {'product': '', 'state': 'closed', 'version': '', 'name': 'http', 'conf': '3', 'extrainfo': '', 'reason': 'reset', 'cpe': ''}, 22: {'product': 'OpenSSH', 'state': 'open', 'version': '7.4', 'name': 'ssh', 'conf': '10', 'extrainfo': 'protocol 2.0', 'reason': 'syn-ack', 'cpe': 'cpe:/a:openbsd:openssh:7.4'}}}, '16.155.194.53': {'status': {'state': 'up', 'reason': 'arp-response'}, 'hostnames': [{'type': 'PTR', 'name': 'smora18ci.hpeswlab.net'}], 'vendor': {'00:50:56:B0:29:9C': 'VMware'}, 'addresses': {'mac': '00:50:56:B0:29:9C', 'ipv4': '16.155.194.53'}, 'tcp': {80: {'product': '', 'state': 'closed', 'version': '', 'name': 'http', 'conf': '3', 'extrainfo': '', 'reason': 'reset', 'cpe': ''}, 22: {'product': '', 'state': 'closed', 'version': '', 'name': 'ssh', 'conf': '3', 'extrainfo': '', 'reason': 'reset', 'cpe': ''}}}}}
>>> nm.command_line()
'nmap -oX - -p 22,80 -sV 16.155.194.52-53'
>>> nm.scaninfo()
{'tcp': {'services': '22,80', 'method': 'syn'}}
>>> nm.all_hosts()
['16.155.194.52', '16.155.194.53']
>>> nm['16.155.194.52'].hostname()
'nickcos72v1.hpeswlab.net'
>>> nm['16.155.194.52'].state()
'up'
>>> nm['16.155.194.52'].all_protocols()
['tcp']
>>> nm['16.155.194.52'].all_tcp()
[22, 80]
>>> nm['16.155.194.52'].tcp(22)
{'product': 'OpenSSH', 'state': 'open', 'version': '7.4', 'name': 'ssh', 'conf': '10', 'extrainfo': 'protocol 2.0', 'reason': 'syn-ack', 'cpe': 'cpe:/a:openbsd:openssh:7.4'}
