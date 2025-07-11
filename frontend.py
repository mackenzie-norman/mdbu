import pytermgui as ptg

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
def list_picker(options):
    return_win = ptg.Window()
    splitter = ptg.Splitter()
    for l in options:
        splitter += ([str(l), lambda l: l])
    return_win += splitter
    return return_win

with ptg.YamlLoader() as loader:
    loader.load(CONFIG)

with ptg.WindowManager() as manager:
    window = (
        ptg.Window(
            ""
            "",
            "Albums",
            ["Artists"],
            ["Playlists", ],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]Max's Disc Burning Utility")
        .center()
    )

    manager.add(list_picker([r for r in range(40)]))