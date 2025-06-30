import os
import click
import shutil
import music_tag
from tqdm import tqdm
from art import text2art
from libpytunes import Library

def get_dict_of_tracks(group_by = 'album',base_path = '/home/max/shared/media/music/'):
    print(f"Scanning {base_path}")
    groups = {}
    for line in tqdm(os.listdir(base_path)):
        file_path = os.path.join(base_path, line)
        music = music_tag.load_file(file_path)  
        keyed = str(music[group_by] )
        if keyed in groups.keys():
            groups[keyed].append(line)
        else:
            groups[keyed] = [line]
    return groups
def copy_tracklist(songs = [],base_path = '/home/max/shared/media/music/'):
    if songs is []:
        with open('tracklist.txt', 'r') as f:
            for line in f.readlines():
                line = line[:-1]
                songs.append(line)
    for song in songs:
        file_path = os.path.join(base_path, song)
        print(f"Copying {line}")
        shutil.copy(file_path, song)
def read_library(file_path = "Library.xml"):
    l = Library(file_path)
    print(l.getPlaylistNames())
def easy_choicer(lst):
    for x, opt in enumerate(lst):
        print(f"{x+1}. {opt}")
    choice = int(input("Please enter a choice: ")) - 1 
    return lst[choice]
@click.command()
@click.option('--write', default= False, help='Should we generate the files?')

def main( write):
    print(text2art("Max's Disc Burning Utility"))
    read_library()
    make_tracklist = True
    chs = easy_choicer(["album", "artist"])
    dct = get_dict_of_tracks(group_by = chs)
    key = easy_choicer(list(dct.keys()))
    songs = dct[key]
    if make_tracklist:
        with open("tracklist.txt" , "w") as f:
            for l in songs:
                f.write(l)
                f.write('\n')
    if write:
        copy_tracklist(songs)

if __name__ == "__main__":
    main()
     


    
