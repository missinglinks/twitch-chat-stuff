# Twitch chat tools

Tools for downloading and analysing chat logs from recorded Twitch.TV streams.

## Requirements

* Python 3.6
* Twitch.TV Client ID

## Usage

### Download video chat log

Download repo

Add config.py:

```
CLIENT_ID = "your_client_id"
```

Crate a text file with the video ids (each id in a new line).
e.g.

video_lists.txt
```
363729808
364147483
```

Download chat log for the videos listed in the text file:

```
$ python downloader.py video_lists.txt
```

### Analysis tools

Example notebook:
Twitch Chat Analysis.ipynb

## License

GPL-3.0