"""
Wrapper classes for Twitch VOD API
"""

import json
import datetime
import math
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict, Counter
from .utils import timestamp


class TwitchChat(object):
    
    def __init__(self, filepath):
        
        data = json.load(open(filepath))
        self._meta = data["meta"]
        self.id = self._meta["_id"]
        self.channel = {
            "id": self._meta["channel"]["_id"],
            "name": self._meta["channel"]["display_name"]
        }
        self.title = self._meta["title"]
        self.views = self._meta["title"]
        self.length = self._meta["length"]
        
        self.comments = []
        for comment in data["comments"]:
            self.comments.append(Comment(comment))
            
    def __getitem__(self, val):
        start = val.start
        end =  val.stop
        for c in self.comments:
            if c.offset_seconds >= start and c.offset_seconds <= end:
                yield c
            
    def duration(self):
        return str(datetime.timedelta(seconds=self.length))
    
    def commenters(self):
        commenters = Counter( [ c.commenter["name"] for c in self.comments ])
        return commenters
    
    def badges(self):
        badges = Counter()
        for c in self.comments:
            badges.update( [ x["_id"] for x in c.badges ] )
        return badges
    
    def emoticons(self, info="link"):
        emoticons = Counter()
        for c in self.comments:
            if info == "link":
                emoticons.update( [ x.link for x in c.emoticons ] )
            else:
                emoticons.update( [ x.text for x in c.emoticons ] )
        return emoticons
    
    def plot_messages(self, start=0, end=None, ticks=5000):
        if not end:
            end = self.length 
        message_times = [ c.offset_seconds for c in self.comments if c.offset_seconds >= start and c.offset_seconds < end]
        start = math.floor(start/ticks)*ticks
        end = math.ceil(end/ticks)*ticks
        plt.figure(figsize=(25,10))
        plt.hist(message_times, bins=round((end-start)/60))
        plt.ylabel('No of messages')
        tick = np.arange(start, end, ticks)
        labels = [ "{1} - {0}".format(timestamp(int(x)),x) for x in tick ]
        plt.xticks(tick, labels, rotation=90)
        plt.show()
        
    def plot_emoticons(self, start=0, end=None, ticks=5000):
        if not end:
            end = self.length 
            
        emoticons = [  ]
        for comment in self.comments:
            if comment.offset_seconds >= start and comment.offset_seconds <= end:
                for emoticon in comment.emoticons:
                    emoticons.append(comment.offset_seconds)

        start = math.floor(start/ticks)*ticks
        end = math.ceil(end/ticks)*ticks
        plt.figure(figsize=(25,10))
        plt.hist(emoticons, bins=round((end-start)/60))
        plt.ylabel('No of emoticons')
        tick = np.arange(start, end, ticks)
        #print(tick)
        labels = [ "{1} - {0}".format(timestamp(int(x)),x) for x in tick ]
        plt.xticks(tick, labels, rotation=90)
        plt.show()



class Comment(object):
    
    def __init__(self, data):
        self._data = data
        
        self.id = data["_id"]
        self.commenter = {
            "id": data["commenter"]["_id"],
            "name": data["commenter"]["display_name"]
        }
        self.message = data["message"]["body"]
        
        self.emoticons = []
        if "emoticons" in data["message"]:
            for fragment in data["message"]["fragments"]:
                if "emoticon" in fragment:
                    self.emoticons.append(Emoticon(fragment))
                    
        if "user_badges" in data["message"]:
            self.badges = data["message"]["user_badges"]
        else:
            self.badges = []
        
        self.offset_seconds = data["content_offset_seconds"]
        self.sate = data["state"]
        self.updated = data["updated_at"]

    def __str__(self):
        return "{:18s} [{}] - {}".format(str(datetime.timedelta(seconds=self.offset_seconds))[:-4], self.commenter["name"], self.message)
        

class Emoticon(object):
    
    EMOTE_URL = "https://static-cdn.jtvnw.net/emoticons/v1/{id}/3.0"
    
    def __init__(self, data):
        
        self.id = data["emoticon"]["emoticon_id"]
        self.text = data["text"]
        self.link = self.EMOTE_URL.format(id=self.id)