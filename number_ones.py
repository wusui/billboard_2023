# Copyright (C) 2023 Warren Usui, MIT License
"""
Find songs that reached #1
"""
import os
from collect_data import read_json, fmt_song_artist

def find_no1(song_data):
    """
    Actual number one checking code
    """
    def find_no1_inner(song_indx):
        if not song_data[song_indx]:
            return False
        return song_data[song_indx]['highest rank'] == 1
    return find_no1_inner

def get_no1s(hot_info):
    """
    Sort results of code checking for number ones
    """
    return sorted(list(filter(find_no1(hot_info), list(hot_info.keys()))))

def extract_no1s():
    """
    Read data and pass to brains of this operation
    """
    return get_no1s(read_json(os.sep.join(['data', 'song_index.json'])))

def number_ones():
    """
    Reformat extracted data
    """
    return list(fmt_song_artist(extract_no1s()))

if __name__ == "__main__":
    print(number_ones())
