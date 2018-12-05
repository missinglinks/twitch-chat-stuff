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

Download chat log:

```
$ python downloader.py <video_id>
```

### Analysis tools

Example notebook:
Twitch Chat Analysis.ipynb

## License

GPL-3.0