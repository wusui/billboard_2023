# Copyright (C) 2023 Warren Usui, MIT License
"""
Reformat information into dict indexed by song===artist
"""
import os
import json
import itertools
from collect_data import read_json

def get_hot100():
    """
    Read saved hot 100 lisst
    """
    return read_json(os.sep.join(['data', 'hot100.json']))

def get_indv_week_recs(hot100):
    """
    Extract weekly data
    """
    def parse_indv_week(weekv):
        def format_record(recordv):
            if not recordv:
                return ['invalid entry', []]
            return [recordv['song'] + '===' + recordv['artist'],
                    [weekv, recordv['position']]]
        return list(map(format_record, hot100[weekv]))
    return list(map(parse_indv_week, list(hot100.keys())))

def get_raw_data():
    """
    Chain together each week's data
    """
    return list(itertools.chain.from_iterable(
                get_indv_week_recs(get_hot100())))

def song_artist_key(hot100):
    """
    Filter out duplicate data when scrunching information
    """
    def song_inner(entry):
        def song_inner2(wk_ent):
            if wk_ent[0] == entry:
                return True
            return False
        return [entry, list(map(lambda a: a[1],
                                list(filter(song_inner2, hot100))))]
    return song_inner

def mk_song_artist_recs(hot100):
    """
    Run artist_key checks for each entry
    """
    return list(map(song_artist_key(hot100), list(dict(hot100))))

def get_song_rex():
    """
    Pass extracted information to mk_song_artist_recs
    """
    return mk_song_artist_recs(get_raw_data())

def process_dates(date_info):
    """
    Generate the date information
    """
    def proc_dates(ranks):
        def proc_dates2(best_info):
            return {'chart dates': ' : '.join([date_info[0][0],
                                               date_info[-1][0]]),
                'weeks on charts': len(ranks),
                'highest rank': best_info[0],
                'weeks at highest': len(best_info)
        }
        return proc_dates2(list(filter(lambda a: a == min(ranks), ranks)))
    if not date_info[0]:
        return {}
    return proc_dates(list(map(lambda a: int(a[1]), date_info)))

def gen_song_index(song_data):
    """
    Wrap the code to generate the date information
    """
    return dict(list(map(lambda a: [a[0], process_dates(a[1])], song_data)))

def get_song_recs():
    """
    Save the data to a json file
    """
    with open(os.sep.join(['data', 'song_index.json']), 'w',
                  encoding='utf-8') as outfile:
        json.dump(gen_song_index(get_song_rex()), outfile)

if __name__ == '__main__':
    get_song_recs()
