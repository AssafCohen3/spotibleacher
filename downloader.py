import asyncio
import logging
import os
from pathlib import Path
from tempfile import mkdtemp

import yaml
from dotenv import load_dotenv
from savify.logger import Logger
from savify.track import Track

from consts import METADATA_FILE_NAME, PLAYLIST_LINK_TEMPLATE
from my_savify import MySavify
from utils import TrackWithDir, sanitize_for_filename, get_track_metadata_dict, setup_logging

SPOTIFY_PLAYLIST_ID = '6PbPBjrUZOVBMdExUGgPGv'
SPOTIFY_PLAYLIST_LINK = 'https://open.spotify.com/playlist/6PbPBjrUZOVBMdExUGgPGv'
ONE_SONG_PLAYLIST = 'https://open.spotify.com/playlist/4gzfEZYiTJJ6jbiHA4spGw'
SESSIONS_DIR = Path('./downloads_test/')


async def create_tracks_directories(tracks: list[Track], session_dir_path: Path) -> list[TrackWithDir]:
    tracks_dirs = []
    for track in tracks:
        dir_name = f'songg_{track.id}_{sanitize_for_filename(track.name)}'
        logging.info(f'Generating {track.name} directory({dir_name})...')
        dir_path = session_dir_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        track_metadata = yaml.safe_dump(get_track_metadata_dict(track))
        metadata_file_path = dir_path / METADATA_FILE_NAME
        metadata_file_path.write_text(track_metadata)
        tracks_dirs.append(TrackWithDir(track, dir_path))

    return tracks_dirs


async def download_tracks(s: MySavify, tracks: list[TrackWithDir]):
    for track in tracks:
        logging.info(f'Downloading track {track.track.name}...')
        s.download_track(track.track, track.dir_path)


def create_savify_client() -> MySavify:
    load_dotenv()

    return MySavify(
        api_credentials=(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET']),
        logger=Logger(log_location='./loggings', log_level=logging.WARNING)
    )


async def download_playlist(playlist_id: str, session_dir: Path) -> Path:
    logging.info(f'Downloading playlist {playlist_id}...')

    s = create_savify_client()

    tracks = s.spotify.link(PLAYLIST_LINK_TEMPLATE % playlist_id)
    logging.info(f'Found {len(tracks)} tracks in the playlist.')

    logging.info('Generating tracks directories...')
    tracks_with_dirs = await create_tracks_directories(tracks, session_dir)

    logging.info('Donwloading tracks...')
    await download_tracks(s, tracks_with_dirs)

    return session_dir


if __name__ == '__main__':
    setup_logging()
    ses_dir = Path(mkdtemp(dir=SESSIONS_DIR, prefix='session_'))
    logging.info(f'Session Directory: {ses_dir.absolute()}')
    asyncio.run(download_playlist('4gzfEZYiTJJ6jbiHA4spGw', ses_dir))
