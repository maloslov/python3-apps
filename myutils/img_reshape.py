import os
import numpy as np
from PIL import Image

all_dirs = ['source/dir']
dir_to = 'destination/dir'
ignored = ['ignored/dir']
exc = []
excepted_log = 'excepted_files.txt'
pairs = []
size = 200
total = 0
counter = 0
is_gray = True
is_recursive = True
save_exc = False

if save_exc:
    with open('excepts.txt', 'w') as fp:
        fp.writelines(exc)

while len(all_dirs)>0:
    dir = all_dirs[0]
    total = total + len(os.listdir(dir))
    for i, j in enumerate(os.listdir(dir)):
        img_path = f'{dir}/{j}'
        counter = counter + 1
    
        print(f'p\t{counter/total*100:.3f}%\t{counter}/{total}\tExcepted: {len(exc)}\t{img_path}\t|', end='\r') 
        
        if os.path.isdir(f'{dir}/{j}'):
            if is_recursive and f'{dir}/{j}' not in ignored:
                all_dirs.append(f'{dir}/{j}')
                continue
                
        img_new_path = f'{dir_to}/reshaped_{"gray" if is_gray else "rgb"}_{size}/{j}'
    
        if(os.path.exists(img_new_path)):
            continue
    
        try:
            img = Image.open(img_path)
        except:
            exc.append(img_path)
            continue

        try:
            img_resized = img.resize((size, size))
            if is_gray:
                img_resized = img_resized.convert('L')
        except:
            exc.append(img_path)
            continue
        
        with open(img_new_path, 'w') as fp:
            pass

        try:
            img_resized.save(img_new_path)
        except:
            exc.append(img_path+'\n')

    all_dirs.remove(dir)

if save_exc:
    with open(excepted_log, 'a') as fp:
        fp.writelines(exc)

input('\aPress Enter to exit...')
