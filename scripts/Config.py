#!/usr/bin/env python3

"""
This module contains code handling the configuration files
"""

import yaml
import re

class SongConfig:
    """
    This class represents user-defined configuration for a single song
    (well, single line in the config file, may apply to multiple songs)
    """

    def __init__(self, title=None, author=None, capo=None, transpose=None):
        
        self.title     = None if title is None else re.compile(title.replace('*', '.*'))
        self.author    = None if author is None else re.compile(author.replace('*', '.*'))
        self.capo      = capo
        self.transpose = transpose

    def _title(self):
        return str(self.title)[12:-2]

    def _author(self):
        return str(self.author)[12:-2]

    def __repr__(self):
        capo  = 'X' if self.capo      is None else self.capo
        xpose = 'X' if self.transpose is None else self.transpose
        return "SONG[capo {}, xpose {}] {:>12s} : {}".format(capo, xpose, self._author(), self._title())

    def matches(self, song):
        if self.title:
            if not self.title.search(song.title):
                return False
        if self.author:
            if song.author is None:
                return False
            if not self.author.search(song.author):
                return False

        return True
        
class Config:
    """
    This class represents user-define configuration as written in a config file
    """

    def __init__(self, filename='config.yml'):
        with open(filename, "r") as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)
            self.page_numbers = bool(self.yaml.get('page_numbers', False))
            self.songs = []
            
            for song_config in self.yaml['songs']:
                name = list(song_config.keys())[0]
                (title, author) = self._parse_title_author(name)

                props = song_config[name]
                if props is None:
                    capo = None
                    transpose = None
                else:
                    capo      = props.get('capo')
                    transpose = props.get('transpose')

                song = SongConfig(title=title, author=author, capo=capo, transpose=transpose)
                self.songs.append(song)
                #print(song)

    def _parse_title_author(self, line):
        split_name = line.split(':')

        title = split_name[-1]
        try:
            author = split_name[-2]
        except IndexError:
            author = None

        return (title, author)

    def get_config(self, song):
        for s in self.songs:
            if s.matches(song):
                return s
        
        return None

         