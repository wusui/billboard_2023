# Copyright (C) 2023 Warren Usui, MIT License
"""
Extract Billboard Hot-100 information
"""
import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fmt_song_artist(results):
    """
    Reformat song===artist string into [song, artist] list
    """
    return list(map(lambda a: a.split("==="), results))

def get_date_range(start_date):
    """
    Generate range of dates when Billboard Hot-100 rankings were released
    """
    return list(map(lambda a: datetime.strftime(
            datetime.fromordinal(a), '%Y-%m-%d'),
                list(range(
                    datetime.strptime(start_date, '%Y-%m-%d').toordinal(),
                    datetime.now().toordinal(), 7))))

def get_chart(datev):
    """
    Extract the information from a Billboard chart
    """
    def get_url():
        return requests.get(
                f'https://www.billboard.com/charts/hot-100/{datev}',
                timeout=600).text
    def get_soup(url):
        return BeautifulSoup(url, 'html.parser')
    def get_entries():
        return get_soup(get_url()).find_all('div',
                            class_='o-chart-results-list-row-container')
    def fmt_dict_entry(xxx):
        return {
                'position': xxx[0].text.strip().split()[0],
                'artist': xxx[3].find('span').text.strip(),
                'song': xxx[3].find('h3').text.strip()
            }
    def extract_info(entries):
        def inner_extract(indx):
            if indx >= len(entries):
                return {}
            return fmt_dict_entry(entries[indx].find_all('li',
                                      class_='o-chart-results-list__item'))
        return inner_extract
    print(datev)
    return list(map(extract_info(get_entries()), range(0, 100)))

def get_all_charts(start_date):
    """
    Get all charts within a data range
    """
    return dict(list(map(lambda a: [a, get_chart(a)],
                         get_date_range(start_date))))

def save_charts(setup):
    """
    Collect data and save in a json file.
    """
    with open(os.sep.join(['data', setup[1]]), 'w',
                    encoding='utf-8') as outfile:
        json.dump(get_all_charts(setup[0]), outfile)

def read_json(fname):
    """
    Extract dict from the json file named in fname
    """
    with open(fname, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def merge_json_data():
    """
    Merge the hot100.json file with the latest data found
    """
    def mjd_inner(hot100):
        def mjd_inner2(temp):
            return read_json(hot100) | read_json(temp)
        return mjd_inner2(os.sep.join(['data', 'temp.json']))
    return mjd_inner(os.sep.join(['data', 'hot100.json']))

def get_last_date_found():
    """
    Find last date saved in hot100.json file
    """
    def gldf_inner(hot100):
        return list(hot100.keys())[-1]
    return gldf_inner(read_json(os.sep.join(['data', 'hot100.json'])))

def do_it_all():
    """
    Generate the hot100 json file from scratch
    """
    save_charts(['1958-08-04', 'hot100.json'])

def update():
    """
    Update the hot100 json file
    """
    save_charts([get_last_date_found(), 'temp.json'])
    with open(os.sep.join(['data', 'newhot.json']), 'w',
                    encoding='utf-8') as outfile:
        json.dump(merge_json_data(), outfile)
    os.remove(os.sep.join(['data', 'temp.json']))
    os.remove(os.sep.join(['data', 'hot100.json']))
    os.rename(os.sep.join(['data', 'newhot.json']),
              os.sep.join(['data', 'hot100.json']))

def collect_data():
    """
    Use existing hot100 data if available
    """
    if os.path.exists(os.sep.join(['data', 'hot100.json'])):
        update()
    else:
        do_it_all()

if __name__ == "__main__":
    collect_data()
