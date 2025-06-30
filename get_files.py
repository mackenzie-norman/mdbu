import os
import shutil
base_path = '/home/max/shared/media/music/'
with open('tracklist.txt', 'r') as f:
    #for line in os.listdir(base_path):
    for line in f.readlines(): 
        line = line[:-1]
        print(line)
        file_path = os.path.join(base_path, line)
        shutil.copy(file_path, line) 
