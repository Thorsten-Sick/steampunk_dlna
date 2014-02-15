#!python
# -*- coding: iso-8859-1 -*-

# Steampunk DB
# Stores files and playlists
# Will start with json, enhance to real db

import eyeD3
import os
import json
import pyglet
import random

class Song():
    """ A single song
    """
    def __init__(self, collection_path):
        """ Init a song

        @param collectionpath: The path containing the music collection
        """
        self.collection_path = collection_path
        self.meta = {}

    def play(self):
        """ Play the song
        http://guzalexander.com/2012/08/17/playing-a-sound-with-python.html
        """
        song = pyglet.media.load(os.path.join(self.collection_path, self.meta["Filename"]))
        song.play()
        pyglet.app.run()


    def from_data(self, data):
        """ Create a song from data
        """
        self.meta = data

    def from_file(self, filename):
        """ Generate entry from a mp3 file
        @param filename: The file name relative to the collection path
        """

        fullname = os.path.join(self.collection_path, filename)
        if eyeD3.isMp3File(fullname):
            audioFile = eyeD3.Mp3AudioFile(fullname)
            tag = audioFile.getTag()
            if tag:
                self.meta["Error"] = None
                self.meta["Album"] = tag.getAlbum().encode("utf-8")
                self.meta["Artist"] = tag.getArtist().encode("utf-8")
                self.meta["DiscNum"] = tag.getDiscNum()[0]
                self.meta["DiscNumMax"] = tag.getDiscNum()[1]
                try:
                    if tag.getGenre():
                        self.meta["Genre"] = tag.getGenre().getName().encode("utf-8")
                except eyeD3.tag.GenreException:
                    self.meta["Error"] = "Broken Genre"
                    pass  # Genre string cannot be parsed with '^([A-Z 0-9+/\-\|!&'\.]+)([,;|][A-Z 0-9+/\-\|!&'\.]+)*$': Hörbuch für Kinder
                self.meta["Title"] = tag.getTitle().encode("utf-8")
                #self.meta["Images"] = tag.getImages()
                self.meta["TrackNum"] = tag.getTrackNum()[0]
                self.meta["TrackNumMax"] = tag.getTrackNum()[1]
                #self.meta["Urls"] = tag.getURLs()
                self.meta["Year"] = tag.getYear()
                #self.meta["FileIDs"] = tag.getUniqueFileIDs()
                self.meta["Filename"] = filename

    def __str__(self):
        res = ""
        for key in self.meta:
            res += "%s  %s \n" %(key, self.meta[key])
        return res

    def get_data(self):
        return self.meta


class Playlist():
    """ A playlist of several songs
    """

    def __init__(self, album = None, pid = None):
        self.pid = pid
        self.album = album
        self.data = {"songs":[]}

    def create_card(self):
        """ Create a card
        """
        pass

    def add_song(self, song):
        """ Add a song
        """
        self.data["songs"].append(song)

    def load_from_data(self):
        """ Load from db file
        """

        pass

    def return_data(self):
        """ return data in playlist
        """

        pass

class Playlists():
    """ All playlists available
    """
    def __init__(self):
        self.playlists = {}   # id:playlist

    def load_from_file(self):
        """ Load playlists from json file
        """
        pass

    def save_to_file(self):
        pass

    def get_playlist_by_id(self, pid):
        """ Get a playlist by id

        @param pid: playlist id
        """
        if pid in self.playlists:
            return self.playlists[pid]
        return None

    def get_playlist_by_album(self, album):
        """ Get playlist by album title

        @param album: album name
        """
        for pid in self.playlists:
            pl = self.playlists[pid]
            if pl.album == album:
                return pl
        return None

    def generate_new_id(self):
        """ Generate a new random, unused id
        """
        r = random.randint(0,10000)
        while (self.get_playlist_by_id(r)):
            r = random.randint(0,10000)
        return r

    def new_playlist(self, album = None):
        """ Create a new playlist
        @param album: Album that is the base for this playlist
        """

        pid = self.generate_new_id()
        p = Playlist(album = album, pid = pid)
        self.playlists[pid] = p
        p.album = album
        return p

    def album_playlist_from_song_db(self, songdb):
        """ Take a song db and create all album playlists
        """

        for song in songdb.db:
            try:
                al = song.meta["Album"]
            except:
                pass
            else:
                pl = self.get_playlist_by_album(al)
                if not pl:
                    pl = self.new_playlist(album = al)
                pl.add_song(song)

    def __str__(self):
        res = ""
        res += "Playlists in db: %d" % len(self.playlists)

        return res

class SongDB():
    """ A List of all songs
    """
    def __init__(self, filename, basedir, new = False):
        """
        @param filename: The name of the json db
        @param basedir: The dir of the collection
        """
        self.filename = filename
        self.basedir = basedir
        if new:
            self.db = self.create_new()
        else:
            self.db = self.load()

    def load(self):
        res = []
        with open(self.filename) as fh:
            data = json.load(fh)
            for sdata in data:
                s = Song(self.basedir)
                s.from_data(sdata)
                res.append(s)

        return res

    def create_new(self):
        return []

    def update_from_dir(self):
        """
        @param dirname: Base dir to read files from
        """

        for subdir, dirs, files in os.walk(self.basedir):
            for file in files:
                fullpath = os.path.join(subdir, file)
                relpath = os.path.relpath(fullpath, self.basedir)
                s = Song(self.basedir)
                s.from_file(relpath)
                self.db.append(s)
        print (len(self.db))

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        data = []
        for asong in self.db:
            data.append(asong.get_data())
        with open(filename, "wt") as fh:
            json.dump(data, fh, indent = 4)
        #print data



if __name__ == "__main__":
    sdb = SongDB("test.json", "/home/thorsten/Musik", True)
    sdb.update_from_dir()
    #sdb.save()
    #sdb.cards()
    p = Playlists()
    p.album_playlist_from_song_db(sdb)
    print(p)