import time

from savify import Savify
from savify.track import Track
from savify.utils import clean


class MySavify(Savify):

    def download_track(self, track: Track):
        self.logger.info(f'Downloading {track.name}...')
        start_time = time.time()

        res = self._download(track)

        self.logger.info(f'Finished Downloading {track.name}! Finished in {time.time() - start_time:.0f}s, '
                         f'Status: {res["returncode"]}')
        self.logger.info('Cleaning up...')
        clean(self.path_holder.get_temp_dir())
