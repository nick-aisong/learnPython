import optparse
from socket import *
from threading import *

'''
multithread
lock
'''
screenLock = Semaphore(value=1)
def connScan (tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print '[+]%d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '[-]%d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        print '\n[+] Scan Restuls for ' + tgtIP
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan , args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost is None) | (tgtPorts[0] is None):
        print parser.usage
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
    
#[root@NickCOS72V1 python]# python TCPScan2.py -H www.baidu.com -p 80,443,5432
#
#[+] Scan Restuls for 104.193.88.123
#[+]443/tcp open
#[+]
#[+]80/tcp open
#[+] HTTP/1.1 400 Bad Request
#
#
#[-]5432/tcp closed
