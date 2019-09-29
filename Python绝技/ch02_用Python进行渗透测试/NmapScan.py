import nmap
import optparse
'''
python-namp
need installed nmap first (https://nmap.org/download.html)
must use IP as tgtHost
'''
def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print " [*] " + tgtHost + " tcp/" + tgtPort + " " + state

def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    if (tgtHost is None) | (tgtPorts[0] is None):
        print parser.usage
        exit(0)
    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
    main()
    
#[root@NickCOS72V1 python]# python NmapScan.py -H 16.155.194.52 -p 80
# [*] 16.155.194.52 tcp/80 closed
#[root@NickCOS72V1 python]# python NmapScan.py -H 16.155.194.52 -p 22
# [*] 16.155.194.52 tcp/22 open
