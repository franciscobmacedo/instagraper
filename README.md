# `instagraper`

Scrape instagram profile posts including the corresponding locations. It can preform cleaning and produce json, geojson or leaflet map outputs.

It can be used as a python package or as a CLI tool.

## Python package

## Installation

```bash
pip install "instagraper"
```

## Usage

### Get posts

returns a list of `Post` dataclass defined [here](./instagraper/models.py).

```python
import instagraper

posts = instagraper.scrape("anthonybourdain", compact=True)
print(posts)
"""
[
    Post(
        taken_at=datetime.datetime(2018, 6, 4, 11, 48, 9),
        username='anthonybourdain',
        caption='Light lunch. #Alsace', 
        lng=11.25, 
        lat=43.7833,
        image_url='https://scontent-lhr6-1.cdninstagram.com/v/t51...',
        pk='1794233220902862216',
        id='1794233220902862216_6113104',
        code='BjmZZuwHr2I',
        user_id='6113104',
        ...
    ),
    ...
]
"""
```

### Dump posts into a json file

```python
import instagraper
# in raw format
instagraper.scrape("anthonybourdain", json_output="anthonybourdain_posts.json")
# creates the "anthonybourdain_posts.json" file

# in compact format
instagraper.scrape("anthonybourdain", compact=True, json_output="anthonybourdain_compact_posts.json")
# creates the "anthonybourdain_compact_posts.json" file
```

### Dumps posts into geojson

Creates geojson points with the posts that have a location (lat and lng).

```python
import instagraper

instagraper.scrape("anthonybourdain", geojson_output="anthonybourdain_posts.geojson")
# creates the "anthonybourdain_posts.geojson" file

```

### Creates map with locations

Creates a leaflet map. It uses the generated geojson file. If not provided, the geojson_output file is created with the corresponding username.

```python
import instagraper

# with a geojson output
instagraper.scrape("anthonybourdain", geojson_output="anthonybourdain_posts.geojson", map_output="anthonybourdain.html")
# creates the "anthonybourdain.html" and "anthonybourdain_posts.geojson" files.

# without a geojson output it still creates one, using the username as the default file name
instagraper.scrape("anthonybourdain", map_output="anthonybourdain.html")
# creates the "anthonybourdain.html" and "anthonybourdain.geojson" files.
```

## CLI

To use the CLI program, you need to install it first:

```bash
pip install "instagraper[cli]"
```

**Usage**:

```console
$ instagraper USERNAME [OPTIONS]
```

**Arguments**:

- `USERNAME`: [required] The instagram username

**Options**:

- `--x-ig-app-id TEXT` Instagram app id (x-ig-app-id) header to authenticate the requests. If not provided, the tool will try to read it from the environment variable `X_IG_APP_ID`
- `--session-id TEXT` Instagram session id (sessionid) cookie to authenticate the requests. If not provided, the tool will try to read it from the environment variable `SESSION_ID`
- `--compact` or `-c`: wether to compact the JSON output or not [default: True]
- `--json` or `-j`: whether to dump the posts to a JSON file or not [default: False]
- `--geojson` or `-g`: whether to dump the posts to a GeoJSON file or not. If map is enabled, this will be enabled by default.
- `--map` or `-m`: whether to create a map with the posts or not. It will enable GeoJSON output by default.
- `--images` or `-i`: whether to download post's images or not.
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.
