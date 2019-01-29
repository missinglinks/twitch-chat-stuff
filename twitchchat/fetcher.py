import requests
import json
import os
import re
from provit import Provenance

EXPORT_DIR = "data"
META_URL = "https://api.twitch.tv/v5/videos/{video_id}?client_id={client_id}"
COMMENTS_URL = "https://api.twitch.tv/v5/videos/{video_id}/comments?client_id={client_id}&cursor={curor}"

class TwitchChatFetcher(object):

    def __init__(self, client_id, video_id, export_dir=EXPORT_DIR):
        
        comments = []
        cursor = ""
        current_len = 0

        resp = requests.get(META_URL.format(video_id=video_id, client_id=client_id))
        meta = resp.json()


        title = meta["title"][:20]
        title = re.sub('\W+','', title )

        channel = meta["channel"]["name"]

        print("load twitch chat ... ")
        print("0", end="")
        while True:
            resp = requests.get(COMMENTS_URL.format(video_id=video_id, client_id=client_id, curor=cursor)) 
            resp = resp.json()

            comments += resp["comments"]
            print("\r", end="")
            current_len = len(comments)
            print(current_len, end="")
            
            if "_next" in resp:
                cursor = resp["_next"]
            else:
                break       

        print("")

        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        video_chat = {
            "meta": meta,
            "comments": comments
        }

        out_file = os.path.join(export_dir, "{}_{}_{}.json".format(video_id, channel, title))
        json.dump(video_chat, open(out_file, "w"), indent=4)

        prov = Provenance(out_file)
        prov.add(
            agents=[ "twitch_chat_downloader" ],
            activity="download_twitch_chat",
            description="video chat download for video '{}...' of channel '{}'".format(title, channel)
        )
        prov.add_primary_source("twitchtv")
        prov.save()