import pexpect

# http://pexpect.readthedocs.io/en/stable/overview.html#windows
# pexpect.spawn and pexpect.run() are not available on Windows,
# as they rely on Unix pseudoterminals (ptys). Cross platform code must not use these.

PROMPT = ['# ', '>>> ', '> ', '\$ ']
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting'
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting'
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = 'localhost'
    user = 'root'
    password = 'root'
    child = connect(user, host, password)
    send_command(child, 'cat /etc/shadow | grep root')

if __name__ == '__main__':
    main()

#[root@NickCOS72V1 python]# python PexpectSSH.py
#cat /etc/shadow | grep root
#root:$6$8m3G3lUK$H3cWyHO27W.wB.vXHizi/9LaHKc.O0F3llrO9bT51KUeQRTI/qm3Y/mYJ4OTk404caM5BQ3.SO5CuaKQjg49G0:17837:0:99999:7:::
#[root@SGDLITVM0172 ~]
