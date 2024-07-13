import logging
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from downloader import METADATA_FILE_NAME
from utils import setup_logging


def is_valid_song_dir_name(d: Path) -> bool:
    return d.is_dir() and d.name.startswith('songg_')


def is_valid_song_dir(d: Path) -> bool:
    if not d.is_dir():
        return False

    if not is_valid_song_dir_name(d):
        return False

    dir_files = list(d.iterdir())

    if len(dir_files) != 2:
        # We expecting exactly 2 songs in each dir.
        return False

    if not (d / METADATA_FILE_NAME).exists():
        # We expecting the dir to contain the metadata dile.
        return False

    if len(list(d.glob('*.mp3'))) != 1:
        # We expecting exactly one mp3 file in the dir.
        return False

    return True


def zip_song_dir(song_dir: Path, output_path: Path) -> Path:
    logging.info(f'Zipping {song_dir}...')
    zip_path = output_path / song_dir.with_suffix('.zip').name
    with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED) as zipfile:
        for f in song_dir.iterdir():
            zipfile.write(f, f.name)

    return zip_path


def encode_zip_file(file_path: Path) -> Path:
    logging.info(f'Encoding {file_path}...')
    file_path = file_path.rename(file_path.with_suffix('.txt'))
    with open(file_path, 'r+b') as f:
        f.seek(0)
        f.write(b'\x40')

    return file_path


def zip_session_songs(session_dir: Path, output_path: Path) -> list[Path]:
    output_path = output_path / session_dir.name
    output_path.mkdir(parents=True, exist_ok=True)

    zips_paths = []

    for d in session_dir.iterdir():
        if is_valid_song_dir_name(d):
            if is_valid_song_dir(d):
                zip_file = zip_song_dir(d, output_path)
                zip_file = encode_zip_file(zip_file)
                zips_paths.append(zip_file)
            else:
                logging.warning(f'Directory {d.absolute()} looks like a song dir but has invalid properties.')

    return zips_paths


if __name__ == '__main__':
    setup_logging()
    zip_session_songs(
        Path('/home/assaf/spotibleacher/downloads_test/session_yo7e7vmc'),
        Path('./zips_test')
    )
