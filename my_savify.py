import time
from pathlib import Path
from typing import Optional

from savify import Savify
from savify.track import Track
from savify.utils import clean


class MySavify(Savify):
    def check_for_updates(self) -> None:
        pass

    def download_track(self, track: Track, downloads_dir: Optional[Path] = None) -> bool:
        old_downloads_dir = self.path_holder.downloads_path
        if downloads_dir is not None:
            self.path_holder.downloads_path = downloads_dir

        try:
            start_time = time.time()

            res = self._download(track)

            self.logger.info(f'Finished Downloading {track.name}! Finished in {time.time() - start_time:.0f}s, '
                             f'Status: {res["returncode"]}')
        finally:
            clean(self.path_holder.get_temp_dir())
            self.path_holder.downloads_path = old_downloads_dir

        return res['returncode'] == 0
