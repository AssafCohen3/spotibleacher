import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from savify import Quality
from savify.logger import Logger
from savify.track import Track
from savify.utils import PathHolder

from my_savify import MySavify
from utils import TrackWithDir

SPOTIFY_PLAYLIST_ID = '6PbPBjrUZOVBMdExUGgPGv'
SPOTIFY_PLAYLIST_LINK = 'https://open.spotify.com/playlist/6PbPBjrUZOVBMdExUGgPGv'
ONE_SONG_PLAYLIST = 'https://open.spotify.com/playlist/4gzfEZYiTJJ6jbiHA4spGw'
SONG_LINK_TEMPLATE = 'https://open.spotify.com/track/%s'
DOWNLOADS_DIR = Path('./downloads_test/')


async def create_tracks_directories(savify: MySavify, tracks: list[Track], session_dir_path: Path) -> list[TrackWithDir]:
    for track in tracks:


async def main():
    load_dotenv()

    s = MySavify(
        api_credentials=(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET']),
        quality=Quality.BEST,
        logger=Logger(log_location='./loggings'),
        path_holder=PathHolder(downloads_path='./downloads')
    )

    # s.download(ONE_SONG_PLAYLIST)
    tracks = s.spotify.link(ONE_SONG_PLAYLIST)

    for track in tracks:
        s.download_track(track)


if __name__ == '__main__':
    asyncio.run(main())
