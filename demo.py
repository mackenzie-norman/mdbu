"""A simple application using examples/boilerplate.py as a basis."""

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

import pytermgui as ptg
from get_albums import read_library, copy_tracklist

PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_DARK = "#4D4940"
PALETTE_DARKER = "#242321"


def _process_arguments(argv: list[str] | None = None) -> Namespace:
    """Processes command line arguments.

    Note that you don't _have to_ use the bultin argparse module for this; it
    is just what the module uses.

    Args:
        argv: A list of command line arguments, not including the binary path
            (sys.argv[0]).
    """

    parser = ArgumentParser(description="My first PTG application.")

    return parser.parse_args(argv)


def _create_aliases() -> None:
    """Creates all the TIM aliases used by the application.

    Aliases should generally follow the following format:

        namespace.item

    For example, the title color of an app named "myapp" could be something like:

        myapp.title
    """

    ptg.tim.alias("app.text", "#cfc7b0")

    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")

    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "inverse app.button.label")

    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def _configure_widgets() -> None:
    """Defines all the global widget configurations.

    Some example lines you could use here:

        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)

    ptg.Button.styles.label = "app.button.label"
    ptg.Button.styles.highlight = "app.button.highlight"

    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT

    ptg.Label.styles.value = "app.text"

    ptg.Window.styles.border__corner = "#C2B280"
    ptg.Container.styles.border__corner = PALETTE_DARK

    ptg.Splitter.set_char("separator", "")


def _define_layout() -> ptg.Layout:
    """Defines the application layout.

    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=3)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body")

    # A slot in the same row as body, using the full non-occupied height and
    # 40% of the terminal's height.
    layout.add_slot("Body right", width=0.2)

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=3)

    return layout


def _confirm_quit(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def _confirm_burn(manager: ptg.WindowManager, song_count: int, burn_fn) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        f"[app.title]Are you sure you want to burn {song_count} songs? ",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: burn_fn()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:

        library = read_library()

        def show_albums(x):
            albums = library.albums()
            manager.add(list_picker(albums), assign="body")

        def show_artists(x):
            artists = library.artists()
            manager.add(list_picker(artists), assign="body")

        def show_playlists(x):
            playlists = {
                p: library.getPlaylist(p).tracks for p in library.getPlaylistNames()
            }
            manager.add(list_picker(playlists), assign="body")

        def selector(songs, title="Untitled"):

            write_tracklist = True
            copy_files = False

            old_windows = [w for w in manager]

            # window = ptg.Window().set_title(f"[210 bold] {title}").center()
            window = ptg.Window()
            songs_to_write = {s: True for s in songs}

            def set_song(song_name, value):
                songs_to_write[song_name] = value

            def write_and_burn():
                with open("tracklist.txt", "w") as f:
                    for l in songs_to_write:
                        if songs_to_write[l]:
                            f.write(l.location.split("/")[-1])
                            f.write("\n")
                # copy_tracklist([s.name for s in songs])
                copy_tracklist()

            song_list = ptg.Container()
            for l in songs:
                splt = ptg.Splitter(
                    l.name,
                    ptg.Checkbox(lambda x: set_song(l, x), True),
                )
                song_list += splt
                # song_list += l.name

            max_char_len = max([len(song.name) for song in songs])
            window.width = max_char_len * 3
            # layout = ptg.Splitter(song_list, ptg.Container())
            # window += layout
            window += song_list
            window += ptg.Splitter(
                ptg.Button(
                    "Burn to CD",
                    lambda x: _confirm_burn(
                        manager,
                        len([s for s in songs_to_write if songs_to_write[s]]),
                        write_and_burn,
                    ),
                ),
                ptg.Button("Back", show_albums),
            )
            manager.add(window, assign="body")

        def list_picker(options, max_size=10, current_idx=0):
            return_win = ptg.Window()
            splitter = ptg.Splitter()
            i = 0
            key_vals = list(options.keys())
            key_vals = (
                key_vals[current_idx % len(key_vals) :]
                + key_vals[current_idx % len(key_vals) :]
            )

            for l in key_vals:
                i += 1
                if i <= max_size:
                    return_win += [
                        str(l),
                        lambda x: selector(options[x.label], x.label),
                    ]

            return_win += ptg.Splitter(
                ptg.Button(
                    "Back",
                    lambda *_: manager.add(
                        list_picker(options, max_size, current_idx - max_size),
                        assign="body",
                    ),
                ),
                ptg.Button(
                    "Next",
                    lambda *_: manager.add(
                        list_picker(options, max_size, current_idx + max_size),
                        assign="body",
                    ),
                ),
            )
            # return_win += splitter

            return return_win

        manager.layout = _define_layout()

        header = ptg.Window(
            "[app.header] Max's Disc Burning Utility",
            is_persistant=True,
        )

        header.styles.fill = "app.header.fill"

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)

        footer = ptg.Window(
            ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
        )
        footer.styles.fill = "app.footer"

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"
        manager.add(footer, assign="footer")

        manager.add(
            ptg.Window(
                "",
                ["Albums", show_albums],
                ["Artists", show_artists],
                ["Playlists", show_playlists],
            ),
            assign="body_right",
        )

        def swap_footer(footer):

            manager.remove(footer)
            ofooter = ptg.Window("Test")
            ofooter.styles.fill = "app.footer"
            manager.add(ofooter, assign="footer")
            footer = ofooter
            return ofooter

        albums = library.albums()
        manager.add(
            list_picker(albums),
            assign="body",
        )

    ptg.tim.print(f"[{PALETTE_LIGHT}]Goodbye!")


if __name__ == "__main__":
    main(sys.argv[1:])
