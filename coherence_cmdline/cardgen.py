import json
import random


class CardGen():
    def __init__(self):
        self.data = {}

    def get_new_id(self):
        while True:
            n = random.randint(1,50000)
            if not n in self.data:
                return n

    def add_card(self, ctype, url, data):
        if ctype == "album":
            if not self.album_in_cards(data["album"]):
                nid = self.get_new_id()
                self.data[nid] = {"ctype": "album",
                                                "songs": [],
                                                "name": data["album"]}
            self.add_song(url, data)

    def album_in_cards(self, album):
        for i in self.data:
            if self.data[i]["ctype"] == "album" and self.data[i]["name"] == album:
                return i
        return 0

    def add_song(self, url, sdata):
        i = self.album_in_cards(sdata["album"])
        if sdata["originalTrackNumber"] is None:
            sdata["originalTrackNumber"] = 0
        self.data[i]["songs"].append({"url": url,
                                      "data": sdata})

    def add_music(self, mfile):
        data = json.load(open(mfile))
        for url in data:
            self.add_card("album", url, data[url])
        self.repair_cards()

    def repair_cards(self):
        for cid in self.data:
            if self.data[cid]["ctype"] == "album":
                self.data[cid]["songs"] = sorted(self.data[cid]["songs"], key = lambda sk: (sk["data"]['originalTrackNumber'], sk["data"]['title']))


    def print_cards(self):
        """ Pretty print cards
        """
        i=1
        for cid in self.data:
            print ("%d: %s %s" % (i, self.data[cid]["ctype"], self.data[cid]["name"]))
            for s in self.data[cid]["songs"]:
                print ("\t %s %s" % (str(s["data"]["originalTrackNumber"]), s["data"]["title"]))
            i += 1



if __name__ == "__main__":
    c = CardGen()
    c.add_music("music_data.json")
    c.print_cards()