#/usr/bin/venv python3

import time
import hashlib
import sys


def patch_bin(orgfile,newfile,diffile):
    items=[]
    with open(diffile,'r') as idf:
        lines = filter(lambda x: x.find(":")!=-1, idf.readlines())
        for l in lines:
            i = list(map(lambda x:x.strip(),l.split(" ")))
            k = {'offset':int(i[0].strip(':'),16),'old':int(i[1],16),'new':int(i[2],16) }
            items.append(k)
        idf.close()
    if len(items) == 0:
        print("patch item is empty!\n")
        return
    nowTime = lambda:str(int(round(time.time() * 1000)))
    newname = newfile+"."+nowTime()
    orgdata = bytearray()
    with open(orgfile,'rb') as oldfile:
        orgdata = bytearray(oldfile.read())
        oldfile.close()
    print("patched file at " + newname)
    with open(newname,'wb') as patchedfile:
        for i in items:
            offset = i['offset']
            old = i['old']
            new = i['new']
            if orgdata[offset] != old:
                print("[x]The old content at %x is not equl to dif file record %x to %s" % (offset,orgdata[offset],old))
                print("[x]Please check it carefully!")
            orgdata[offset] = new
        patchedfile.write(orgdata)
        print("MD5 hash is %s" % hashlib.md5(orgdata).digest().hex())
        patchedfile.close()
    
def print_usage():
    usage = \
    """
    The tool use to create a new file by the idf file.
    usage: python3 patch_idf.py oldfile newfile idffile
    """
    print(usage)
if __name__ == '__main__':
    try:
        orgf = sys.argv[1]
        newf = sys.argv[2]
        difff= sys.argv[3]
        patch_bin(orgf,newf,difff)
    except Exception:
        print_usage()
        
#patch_bin(r'./Dump.bin',r'./Dump.bin.patched',r'./Dump.dif')