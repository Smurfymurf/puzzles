#!/usr/bin/env python3
# piddate.py - is a wrong pid md5(content + <timestamp/date>)?
import hashlib, datetime, time
def md5(s): return hashlib.md5(s.encode()).hexdigest()
TARGETS=[('8b71bade9685d3388452bc4755b06a0d','"What?"'),
         ('bf0df75f9cd317fcf4062da51aab0b75','Block 1'),
         ('dec871dacfb023c2fe1d92eea3fd5d49','Block 1'),
         ('4a55f5541cba460f95e7d82fe2a40b28','Block 1')]
t0=time.time()
# 1) date strings for every day 2019-01-01 .. 2026-12-31, many formats
FMT=['%Y-%m-%d','%d/%m/%Y','%m/%d/%Y','%Y/%m/%d','%d-%m-%Y','%Y%m%d','%b %d, %Y','%d %B %Y',
     '%Y-%m-%dT%H:%M:%SZ','%Y-%m-%d %H:%M:%S','%a %b %d %Y','%d.%m.%Y','%Y-%m-%dT%H:%M:%S','%Y%m%d%H%M%S']
d=datetime.date(2019,1,1); end=datetime.date(2026,12,31)
days=[]
while d<=end:
    days.append(d); d+=datetime.timedelta(days=1)
print('days',len(days),'formats',len(FMT))
for pid,base in TARGETS:
    for day in days:
        for f in FMT:
            s=day.strftime(f)
            if md5(base+s)==pid: print('HIT suffix date %r base=%r'%(s,base))
            if md5(s+base)==pid: print('HIT prefix date %r base=%r'%(s,base))
print('phase1 %.1fs'%(time.time()-t0))
# 2) epoch seconds 1.50e9..1.60e9 (2017-09..2020-09) as seconds and as seconds*1000
lo,hi=1500000000,1600000000
for pid,base in TARGETS:
    for n in range(lo,hi):
        s=str(n)
        if md5(base+s)==pid: print('HIT suffix epoch %s base=%r'%(s,base))
        if md5(s+base)==pid: print('HIT prefix epoch %s base=%r'%(s,base))
        s=str(n*1000)
        if md5(base+s)==pid: print('HIT suffix epochms %s base=%r'%(s,base))
print('phase2 %.1fs'%(time.time()-t0))
