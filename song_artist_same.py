# Copyright (C) 2023 Warren Usui, MIT License
"""
Get instances where the song and artist are the same
"""
import os
from collect_data import read_json, fmt_song_artist

def get_raw_dups(comparison):
    """
    Perform comparisons. 'exact', 'artist' if song is in artist name,
                         'song' if artist is in song title.
    """
    def get_indv_week_dups(hot100):
        def dcheck_tf(song_artist):
            if len(song_artist) != 2:
                return False
            if song_artist[0] == song_artist[1]:
                return True
            if song_artist[0] in song_artist[1]:
                if comparison in ['all', 'artist']:
                    return True
            if song_artist[1] in song_artist[0]:
                if comparison in['all', 'song']:
                    return True
            return False
        def dup_check(sval):
            return dcheck_tf(sval.split("==="))
        return list(filter(dup_check, list(hot100.keys())))
    return get_indv_week_dups(read_json(
                        os.sep.join(["data", "song_index.json"])))

def song_artist_same(comparison='exact'):
    """
    Wrap comparison check
    """
    return fmt_song_artist(get_raw_dups(comparison))

if __name__ == "__main__":
    print(song_artist_same('exact'))
