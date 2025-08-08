from libpytunes import Library
from datetime import datetime

lib = Library("Library.xml")

songs = [lib.songs[s] for s in lib.songs]
songs = [s for s in songs if s.play_count is not None]
songs = sorted(songs, key=lambda x: x.play_count)
for s in songs:
    total_time = s.total_time.split(".")[0]
    format_string = "%H:%M:%S"  # Format matching your time string

    dt_object = datetime.strptime(
        total_time, format_string
    )  # Convert to datetime object
    seconds = dt_object.second + dt_object.minute * 60
    total_time = seconds * s.play_count
    print(f"{s.name}: {total_time}")
