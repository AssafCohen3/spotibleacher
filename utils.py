import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import colorlog
from savify.track import Track


@dataclass
class TrackWithDir:
    track: Track
    dir_path: Path


def sanitize_for_filename(s: str) -> str:
    s = s.replace(' ', '_')
    return ''.join([c for c in s if c.isalnum() or c == '_'])


def get_track_metadata_dict(track: Track) -> dict[str, Any]:
    return {
        'name': track.name,
        'artist': ', '.join(track.artists),
        'album': track.album_name
    }


def setup_logging():
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("spotipy").setLevel(logging.INFO)
    logging.getLogger("savify").setLevel(logging.INFO)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    cformat = '%(log_color)s' + log_format
    f = colorlog.ColoredFormatter(
        cformat, date_format,
        log_colors={
            'DEBUG': 'red', 'INFO': 'blue',
            'WARNING': 'bold_yellow', 'ERROR': 'bold_red',
            'CRITICAL': 'bold_red'
        }
    )
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    root.addHandler(ch)
