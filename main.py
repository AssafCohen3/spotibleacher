import asyncio
import logging
from pathlib import Path
from tempfile import mkdtemp

from downloader import download_playlist
from utils import setup_logging
from zipper import zip_session_songs

SESSIONS_DIR = Path('./downloads_test/')
SPOTIFY_PLAYLIST_ID = '6PbPBjrUZOVBMdExUGgPGv'


async def main():
    setup_logging()
    ses_dir = Path(mkdtemp(dir=SESSIONS_DIR, prefix='session_'))
    logging.info(f'Session Directory: {ses_dir.absolute()}')
    ses_dir = await download_playlist(SPOTIFY_PLAYLIST_ID, ses_dir)
    res = zip_session_songs(ses_dir, Path('zips_test'))
    logging.info(f'Resulting zips: {res}')


if __name__ == '__main__':
    asyncio.run(main())
