from dataclasses import dataclass
from pathlib import Path

from savify.track import Track


@dataclass
class TrackWithDir:
    track: Track
    dir_path: Path
