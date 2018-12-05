import sys
from twitchchat import TwitchChatFetcher
from config import CLIENT_ID

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(0)
    
    video_id = sys.argv[1]
    fetcher = TwitchChatFetcher(CLIENT_ID, video_id)