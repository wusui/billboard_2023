# Copyright (C) 2023 Warren Usui, MIT License
"""
Find song that have same name as another artist (Prince->Kiss) for example
"""
import os
from collect_data import read_json

def get_info():
    """
    Read stashed data and convert to [song, artist]
    """
    return list(map(lambda a: a.split('==='),
                read_json(os.sep.join(["data", "song_index.json"]))))

def get_sep_list(hot100):
    """
    Separate the artist and song lists
    """
    def get_indv_list(indx):
        def get_an_elem(song_artist):
            if len(song_artist) < 2:
                return 'invalid entry'
            return song_artist[indx]
        return list(map(get_an_elem, hot100))
    return list(map(get_indv_list, list(range(0, 2))))

def get_as_lists():
    """
    Make sure entries are unique
    """
    return list(map(lambda a: list(set(a)), get_sep_list(get_info())))

def drop_articles(sa_value):
    """
    Remove articles for close comparisions
    """
    if sa_value.split(' ')[0] in ['a', 'an', 'the']:
        return sa_value[1:]
    return sa_value

def unplural(sa_value):
    """
    Remove s suffix plurals for close comparisons
    """
    if sa_value.endswith('s'):
        return sa_value[0 : -1]
    return sa_value

def more_manips(sa_value):
    """
    For close entries, fix spacing and punctuation to match
    """
    return unplural(drop_articles(sa_value).replace(' ', '')).replace(
        '-', '').replace(',', '').replace('.', '').replace('$', '')

def find_close(as_list):
    """
    Make sure kickin' reads as kicking for example
    """
    def label_elem(sa_value):
        return [more_manips(sa_value.lower().replace("'", "g")), sa_value]
    def make_labels(indx):
        return dict(list(map(label_elem, as_list[indx])))
    return list(map(make_labels, range(0, 2)))

def pair_up(as_dicts):
    """
    Pair up entries so conversion to dictionary works.
    Filter out invalid entries
    """
    def pair_up2(kvalue):
        if kvalue in as_dicts[1].keys():
            return [as_dicts[0][kvalue], as_dicts[1][kvalue]]
        return None
    return list(filter(None, list(map(pair_up2, as_dicts[0].keys()))))

def find_similar(as_list):
    """
    Wrap find similar function calls
    """
    def find_sim_in1(exact_list):
        def crunch_a_list(indx):
            return list(filter(lambda a: a not in exact_list, as_list[indx]))
        def crunch_list():
            return list(map(crunch_a_list, range(0, 2)))
        return {'exact': exact_list,
                'close': pair_up(find_close(crunch_list()))}
    return find_sim_in1(list(filter(lambda a: a in as_list[0],
                                    as_list[1])))

def title_clean(messy):
    """
    Remove invalid entry from list
    """
    return list(filter(lambda a: not a == 'invalid entry', messy['exact']))

def extra_clean(messy):
    """
    Remove improper connections (found manually, slightly kludgy.
    I should probably make the list a readable file.
    """
    return list(filter(lambda a: a[0] not in ['99', 'SOS'], messy['close']))

def cleanup(messy):
    """
    Return formatted dictionary
    """
    return {'exact': title_clean(messy), 'close': extra_clean(messy)}

def song_another_artist_same():
    """
    Main single entry point
    """
    return cleanup(find_similar(get_as_lists()))

if __name__ == "__main__":
    print(song_another_artist_same())
