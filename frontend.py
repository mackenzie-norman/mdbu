import pytermgui as ptg
from get_albums import read_library, copy_tracklist
from art import text2art

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""


with ptg.WindowManager() as manager:

    def selector(songs, title="Untitled"):
        global manager
        write_tracklist = True
        copy_files = False
        songs_to_write = {s.name: True for s in songs}
        old_windows = [w for w in manager]

        window = ptg.Window().set_title(f"[210 bold] {title}").center()

        def flip_var(x):
            x = not x
            print(f"Writing {len(songs)} songs to tracklist.txt")
            with open("tracklist.txt", "w") as f:
                for l in songs:
                    f.write(l.location.split("/")[-1])
                    f.write("\n")
            # copy_tracklist([s.name for s in songs])
            copy_tracklist()
            manager.remove(window)
            for w in old_windows:
                manager.add(w)

        song_list = ptg.Container()
        for l in songs:
            splt = ptg.Splitter(l.name, ptg.Checkbox(True)).set_char("seperator", "")
            song_list += splt
            # song_list += l.name

        max_char_len = max([len(song.name) for song in songs])
        window.width = max_char_len * 3
        layout = ptg.Splitter(song_list, ptg.Container())
        window += layout
        window += ptg.Splitter(
            ptg.Button("Burn to CD", lambda x: flip_var(copy_files)),
            ptg.Button("Back", show_albums),
        )
        clear_windows()
        manager.add(window)

    def list_picker(options):
        return_win = ptg.Window()
        splitter = ptg.Splitter()
        for l in list(options.keys()):
            return_win += [str(l), lambda x: selector(options[x.label], x.label)]
        # return_win += splitter
        return return_win

    def clear_windows():
        global manager
        for w in manager:
            manager.remove(w)

    library = read_library()
    show_albums = lambda x: show_albums(x)
    window = (
        ptg.Window(
            "" "",
            ["Albums", show_albums],
            ["Artists"],
            [
                "Playlists",
            ],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]Max's Disc Burning Utility")
        .center()
    )

    def show_albums(x):
        global manager
        clear_windows()
        albums = library.albums()
        manager.add(list_picker(albums))

    manager.add(window)
    # manager.add(list_picker(library.artists()))
    # manager
    manager.__enter__()
