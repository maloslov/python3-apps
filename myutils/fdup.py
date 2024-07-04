# -*- coding: UTF-8 -*-
import os 
import sys 
import time
import hashlib 


### PARAMS ###
# base directory to scan recursively
basedir = ['source/dir']
# ignore lists
ignoredir = ['ignore/dir']
ignorefile = ['ignore.file']
# dup output file 
logpath = 'fdup.py.log'
### flags ###
logmode = 'both' # 'cmd' for terminal-only, 'file' for file-only, 'both' for both
debug = False # prints some steps
recursive = True # scan subdirectories

with open(logpath, 'w') as _:
    pass

# Calculates file hash 
def Hash_File(path, strbu): 
    # Opening file in afile 
    afile = open(path, 'rb') 
    hasher = hashlib.md5() 
    blocksize=4096
    buf = afile.read(blocksize) 
    cnt = 1
    print('{}/{}\t{:.3f}%,\tread_path: {}\t_'.format(strbu, total_files, strbu/total_files*100, path),end='\r')
    
    while len(buf) > 0: 
        if debug: print('{},\tread_path: {}\tread_blocks: {}\t_'.format(strbu, path, cnt),end='\r')
        hasher.update(buf) 
        buf = afile.read(blocksize) 
        cnt+=1
    afile.close() 
    return hasher.hexdigest() 


### custom log ###
def myprint(string, mode='cmd', file=None):
    if mode=='cmd' or mode=='both':
        print(string)
    if (mode=='file' or mode=='both') and file is not None:
        with open(file,mode='a',encoding='utf-8') as f:
            f.write('{}\r'.format(string))


def listallsubfiles(targdir):
    dict = []
    dirs = targdir
    cnt_f = 0
    while len(dirs)>0:
        for dir in dirs:
            if dir in ignoredir:
                dirs.remove(dir)
                continue
            for i in os.listdir(dir):
                if os.path.isdir('{}/{}'.format(dir,i)):
                    if recursive:
                        dirs.append('{}/{}'.format(dir,i))
                else:
                    if i in ignorefile:
                        continue
                    cnt_f += 1
                    f = '{}/{}'.format(dir,i)
                    dict.append([f, Hash_File(f,cnt_f)])
            dirs.remove(dir)
    return dict
    
    
def countallfiles(targdir):
    dict = []
    dirs = targdir.copy()
    cnt_f = 0
    cnt_t = 0
    while len(dirs)>0:
        for dir in dirs:
            if dir in ignoredir:
                dirs.remove(dir)
                continue
            cnt_t += len(os.listdir(dir))
            for i in os.listdir(dir):
                if os.path.isdir('{}/{}'.format(dir,i)):
                    if recursive:
                        dirs.append('{}/{}'.format(dir,i))
                    cnt_t -= 1
                else:
                    if i in ignorefile:
                        continue
                    cnt_f += 1
                    print('counting total files: {}/{}\t{:.3f}%'.format(cnt_f, cnt_t, cnt_f/cnt_t*100),end='\r')
            dirs.remove(dir)
    return cnt_t
    

def sortlistbyhash(list2d):
    resdict = {}
    cnt_l = 0
    prev_l = ''
    for i in sorted(list2d, key=lambda row: (row[1])):
        if i[1] in resdict:
            resdict[i[1]].append(i[0])
        else:
            resdict[i[1]] = [i[0]]
    return resdict        


avgtime = 1
strbuf = ''
Duplic = {} 
total_files=countallfiles(basedir)
files = listallsubfiles(basedir)

myprint('Basedir: {}'.format(basedir), mode=logmode,file=logpath)
myprint('Total files: {}'.format(len(files)), mode=logmode,file=logpath)

results = sortlistbyhash(files)
print(len(results))

for key,value in results.items():
    if len(value)>1:
        #myprint('\t<dupfile>',mode=logmode,file=logpath)
        for i in range(len(value)):
            myprint(f'{"del" if i < (len(value)-1) else "echo"} "{value[i]}\"',mode=logmode,file=logpath)
        #myprint('\t</>',mode=logmode,file=logpath)

input('\aPress enter to exit...')
