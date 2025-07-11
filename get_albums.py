import os
import click
import shutil
import music_tag
from tqdm import tqdm
from art import text2art
from libpytunes.libpytunes.Library import Library

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
    return l
def easy_choicer(lst):
    for x, opt in enumerate(lst):
        print(f"{x+1}. {opt}")
    choice = int(input("Please enter a choice: ")) - 1 
    return lst[choice]
@click.command()
@click.option('--write', default= False, help='Should we generate the files?')

def main( write):
    print(text2art("Max's Disc Burning Utility"))
    lib = read_library()
    make_tracklist = True
    options = ["album", "artist", "playlist", "quit"]
    chs = easy_choicer(options)
    while chs != "quit":
        if chs == "album":
           albums = lib.albums()     
           songs = albums[easy_choicer(list(albums.keys()))]
        if chs == "artist":
           artists = lib.artists()     
           songs = artists[easy_choicer(list(artists.keys()))]
        if chs == "playlist":
            playlist = easy_choicer(lib.getPlaylistNames())
            songs = lib.playlist(playlist)

        if make_tracklist:
            print(f"Writing {len(songs)} songs to tracklist.txt")
            with open("tracklist.txt" , "w") as f:
                for l in tqdm(songs):
                    f.write(l.location.split("/")[-1])
                    f.write('\n')
        if write:
            copy_tracklist(songs)

        chs = easy_choicer(options)
    #dct = get_dict_of_tracks(group_by = chs)
    #key = easy_choicer(list(dct.keys()))
    #songs = dct[key]

if __name__ == "__main__":
    main()
     


    
