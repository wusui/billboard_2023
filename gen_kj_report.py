# Copyright (C) 2023 Warren Usui, MIT License
"""
Generate report of artists and song names matching (Steam, for example).
"""
import os
import itertools
from collect_data import read_json
from song_another_artist_same import song_another_artist_same

def yformat(yrange):
    """
    Extract range of years from date ranges
    """
    def yfmt(yvalues):
        if yvalues[0] == yvalues[1]:
            return yvalues[0]
        return '-'.join(yvalues)
    return yfmt(list(map(lambda a: a.split('-')[0], yrange.split(' : '))))

def set_string_parms(hot100):
    """
    Find and extract data needed for the lines that will be printed
    """
    def get_txt_info(sa_key):
        return {'song': sa_key.split("===")[0],
                'artist': sa_key.split("===")[1],
                'chart range': yformat(hot100[sa_key]['chart dates']),
                'highest rank': str(hot100[sa_key]['highest rank'])}
    def handle_sa(pair_to_check):
        def song_keys():
            return list(filter(lambda a: a.startswith(
                pair_to_check[0] + '==='), hot100.keys()))
        def artist_keys():
            return list(filter(lambda a: a.endswith(
                '===' + pair_to_check[1]), hot100.keys()))
        return [get_txt_info(song_keys()[0]), get_txt_info(artist_keys()[0])]
    def ssp_inner(same_dict):
        def handle_exact(elist):
            def he_inner(samev):
                return handle_sa([samev, samev])
            return list(map(he_inner, elist))
        def handle_close(cvalues):
            return list(map(handle_sa, cvalues))
        return handle_exact(same_dict['exact']) + [
                    [{'header': 'Not quite exact matches'}, {}]
                    ] + handle_close(same_dict['close'])
    return ssp_inner(song_another_artist_same())

def fmt_pt1(line_info):
    """
    Format the first part of each song/artist comparison
    """
    return f'In {line_info["chart range"]} {line_info["artist"]} ' + \
           f'reached {line_info["highest rank"]} with ' + \
           f'<b>{line_info["song"]}</b>'

def fmt_pt2(line_info):
    """
    Format the second part of each song/artist comparison
    """
    return f'<b>{line_info["artist"]}</b> reached ' + \
           f'{line_info["highest rank"]} in {line_info["chart range"]} ' + \
           f'with {line_info["song"]}'

def fmt_an_answer(sinfo_pair):
    """
    Format each two line section
    """
    if 'header' in sinfo_pair[0].keys():
        return [f'<br><h3><b>{sinfo_pair[0]["header"]}</b></h3>']
    if sinfo_pair[0]['artist'] == sinfo_pair[1]['artist']:
        return []
    return ['<p>', fmt_pt1(sinfo_pair[0]), '<br>', fmt_pt2(sinfo_pair[1])]

def html_fmt(info):
    """
    Step through each pairing
    """
    return list(map(fmt_an_answer, info))

def gen_html(info):
    """
    Wrapper for html writing code
    """
    def gh_out():
        return [['<h3><b>Exact matches</b></h3>']] + html_fmt(info)
    def gh_chain():
        return '\n'.join(list(itertools.chain.from_iterable(gh_out())))
    with open(os.sep.join(['data', 'kj_answers.html']), 'w',
                    encoding='utf-8') as outfile:
        outfile.write(gh_chain())

def gen_kj_report():
    """
    Report entry point
    """
    return gen_html(set_string_parms(read_json(os.sep.join(
                    ["data", "song_index.json"]))))

if __name__ == "__main__":
    gen_kj_report()
