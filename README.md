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

Create a text file with the video ids (each id in a new line).
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

## Elasticsearch ingest

Add elasticsearch server credentials to config.py:

```
ES_SERVER = "<user>:<pwd>@url.com:9200"
```

Load all twitch chat logs (.json dumps) in a directory into elasticsearch:

```
$ python es_ingest.py -d <directory>
```



## License

GPL-3.0
