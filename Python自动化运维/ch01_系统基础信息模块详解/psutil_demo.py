# 参考：https://github.com/giampaolo/psutil
# 依赖模块：yum -y install python-devel

# 物理内存total值： free -m | grep Mem | awk '{print $2}'
# 物理内存used值：  free -m | grep Mem | awk '{print $3}'

# 获取CPU信息
[root@NickCOS72V1 ~]# python
Python 2.7.5 (default, Aug  7 2019, 00:51:29)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import psutil
>>> psutil.cpu_times()
scputimes(user=58203.3, nice=9.54, system=27699.06, idle=8965624.88, iowait=234.33, irq=0.0, softirq=785.2, steal=0.0, guest=0.0, guest_nice=0.0)
>>> psutil.cpu_times().user
58203.42
>>> psutil.cpu_count()
8
>>> psutil.cpu_count(logical=False)
2

# 获取内存信息
>>> mem = psutil.virtual_memory()
>>> mem
svmem(total=16825335808, available=15094845440, percent=10.3, used=1365942272, free=14174466048, active=1573937152, inactive=569917440, buffers=2199552, cached=1282727936, shared=18178048, slab=270893056)
>>> mem.total
16825335808
>>> mem.free
14174466048
>>> psutil.swap_memory()
sswap(total=0, used=0, free=0, percent=0.0, sin=0, sout=0)
>>>

# 获取磁盘信息
>>> psutil.disk_partitions()
[sdiskpart(device='/dev/mapper/centos_shcentos72x64-root', mountpoint='/', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota'), sdiskpart(device='/dev/sda1', mountpoint='/boot', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota')]
>>> psutil.disk_usage('/')
sdiskusage(total=129367273472, used=17037328384, free=112329945088, percent=13.2)
>>> psutil.disk_io_counters()
sdiskio(read_count=67683, write_count=551200, read_bytes=1935468032, write_bytes=4927847936, read_time=276487, write_time=720096, read_merged_count=36, write_merged_count=5104, busy_time=564921)
>>> psutil.disk_io_counters(perdisk=True)
{'fd0': sdiskio(read_count=0, write_count=0, read_bytes=0, write_bytes=0, read_time=0, write_time=0, read_merged_count=0, write_merged_count=0, busy_time=0), 'sr0': sdiskio(read_count=0, write_count=0, read_bytes=0, write_bytes=0, read_time=0, write_time=0, read_merged_count=0, write_merged_count=0, busy_time=0), 'sda2': sdiskio(read_count=25409, write_count=160065, read_bytes=715675648, write_bytes=1527613952, read_time=101982, write_time=218837, read_merged_count=33, write_merged_count=3612, busy_time=197742), 'sda3': sdiskio(read_count=8373, write_count=112718, read_bytes=249284096, write_bytes=935241216, read_time=35674, write_time=133556, read_merged_count=3, write_merged_count=1491, busy_time=93105), 'sda': sdiskio(read_count=33918, write_count=273324, read_bytes=973805568, write_bytes=2465043968, read_time=138001, write_time=352674, read_merged_count=36, write_merged_count=5104, busy_time=282419), 'sda1': sdiskio(read_count=105, write_count=541, read_bytes=7133696, write_bytes=2188800, read_time=319, write_time=281, read_merged_count=0, write_merged_count=1, busy_time=546), 'dm-0': sdiskio(read_count=33677, write_count=277886, read_bytes=959278592, write_bytes=2462855168, read_time=138449, write_time=367432, read_merged_count=0, write_merged_count=0, busy_time=282478), 'dm-1': sdiskio(read_count=88, write_count=0, read_bytes=2383872, write_bytes=0, read_time=37, write_time=0, read_merged_count=0, write_merged_count=0, busy_time=30)}

# 获取网络信息
>>> psutil.net_io_counters()
snetio(bytes_sent=1088880194, bytes_recv=6090333011, packets_sent=4799963, packets_recv=72224647, errin=0, errout=0, dropin=0, dropout=0)

# 获取其他系统信息
>>> psutil.net_io_counters()
snetio(bytes_sent=1088880194, bytes_recv=6090333011, packets_sent=4799963, packets_recv=72224647, errin=0, errout=0, dropin=0, dropout=0)
>>>
>>> psutil.users()
[suser(name='root', terminal='pts/0', host='cnnikais01.apj.softwaregrp.net', started=1570788864.0, pid=26649), suser(name='root', terminal='pts/1', host='sgdlitvm0841.hpeswlab.net', started=1570860416.0, pid=30460), suser(name='root', terminal='pts/5', host='cnnikais01.apj.softwaregrp.net', started=1569810816.0, pid=18296)]
>>> import datetime
>>> psutil.boot_time()
1569734482.0
>>> datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
'2019-09-29 13:21:22'


# 管理进程信息
>>> psutil.pids()
[1, 2, 3, 5, 7, 8, 9, 10, 13, 14, 16, 18, 19, 21, 23, 24, 26, 28, 29, 31, 33, 34, 36, 38, 39, 41, 43, 44, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 66, 67, 68, 69, 77, 79, 80, 81, 83, 96, 132, 398, 412, 438, 598, 599, 603, 604, 605, 606, 609, 610, 639, 659, 709, 710, 719, 720, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 830, 831, 856, 857, 867, 873, 1047, 1205, 1206, 1207, 1210, 1211, 1212, 1213, 1216, 1275, 1276, 1278, 1280, 1301, 1303, 1307, 1309, 1311, 1312, 1313, 1314, 1318, 1322, 1329, 1331, 1332, 1333, 1334, 1337, 1345, 1350, 1361, 1363, 1423, 1565, 1657, 1659, 1668, 1671, 1674, 1678, 1683, 1684, 1692, 1706, 1707, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1733, 1978, 1995, 1996, 2000, 2002, 2020, 2482, 3144, 5096, 6919, 7742, 7747, 9329, 9897, 10138, 11075, 11347, 11390, 11927, 11960, 13071, 13581, 16079, 17860, 18296, 19739, 22289, 24880, 24896, 24984, 25333, 25334, 25335, 25336, 25337, 25338, 25339, 25340, 26621, 26627, 26630, 26649, 28020, 28361, 29895, 30415, 30428, 30437, 30460]
>>> p = psutil.Process(2020)
>>> p.name()
'java'
>>> p.exe()
'/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.222.b10-0.el7_6.x86_64/jre/bin/java'
>>> p.cwd()
'/'
>>> p.status()
'sleeping'
>>> p.create_time()
1569734502.67
>>> p.uids()
puids(real=988, effective=988, saved=988)
>>> p.gids()
pgids(real=983, effective=983, saved=983)
>>> p.cpu_times()
pcputimes(user=2880.39, system=1504.11, children_user=0.0, children_system=0.0)
>>> p.cpu_affinity()
[0, 1, 2, 3, 4, 5, 6, 7]
>>> p.memory_percent()
6.001366198705471
>>> p.memory_info()
pmem(rss=1009750016, vms=10079301632, shared=23871488, text=4096, lib=0, data=9865318400, dirty=0)
>>> p.io_counters()
pio(read_count=23495, write_count=1897, read_bytes=146182144, write_bytes=643772416, read_chars=31575001, write_chars=4362795)
>>> p.connections()
[pconn(fd=162, family=10, type=1, laddr=addr(ip='::', port=8080), raddr=(), status='LISTEN'), pconn(fd=351, family=10, type=2, laddr=addr(ip='::', port=33848), raddr=(), status='NONE'), pconn(fd=352, family=10, type=2, laddr=addr(ip='::', port=5353), raddr=(), status='NONE')]
>>> p.num_threads()
49

>>> from subprocess import PIPE
>>> p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"], stdout=PIPE)
>>> p.name
<bound method Popen.name of psutil.Popen(pid=14930, name='python', started='18:57:07')>
>>> p.name()
'python'
>>> p.username()
'root'
>>> p.cpu_times()
pcputimes(user=0.02, system=0.01, children_user=0.0, children_system=0.0)
>>> p.communicate()
('hello\n', None)
>>> p.cpu_times()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.7/site-packages/psutil/_common.py", line 345, in wrapper
    return fun(self)
  File "/usr/lib64/python2.7/site-packages/psutil/__init__.py", line 1159, in cpu_times
    return self._proc.cpu_times()
  File "/usr/lib64/python2.7/site-packages/psutil/_pslinux.py", line 1513, in wrapper
    return fun(self, *args, **kwargs)
  File "/usr/lib64/python2.7/site-packages/psutil/_pslinux.py", line 1705, in cpu_times
    values = self._parse_stat_file()
  File "/usr/lib64/python2.7/site-packages/psutil/_pslinux.py", line 1524, in wrapper
    raise NoSuchProcess(self.pid, self._name)
psutil.NoSuchProcess: psutil.NoSuchProcess process no longer exists (pid=15153)
