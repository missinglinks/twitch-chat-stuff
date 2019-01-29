import sys
import os
import click
from twitchchat import TwitchChatFetcher
from config import CLIENT_ID

@click.command()
@click.argument("videolist")
@click.option("--out_dir", default="data")
def download_videos(videolist, out_dir):
    with open(videolist) as f:
        video_ids = [ x.strip() for x in f.readlines() ]
        
        filename = os.path.basename(videolist)

        out_sub_dir = filename.replace(".txt", "")
        out_dir = os.path.join(out_dir, out_sub_dir)


        for video_id in video_ids:
            print(video_id)
            fetcher = TwitchChatFetcher(CLIENT_ID, video_id, export_dir=out_dir)



if __name__ == "__main__":
    download_videos()
    # if len(sys.argv) <= 1:
    #     sys.exit(0)
    
    # video_id = sys.argv[1]
    # fetcher = TwitchChatFetcher(CLIENT_ID, video_id)