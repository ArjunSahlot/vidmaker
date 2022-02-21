#
#  vidmaker
#  A python library which simplifies creating and exporting videos.
#  Copyright Arjun Sahlot 2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import numpy as np
import cv2
import tempfile
from pathlib import Path


class Video:
    def __init__(self, path, fps, resolution="AUTO"):
        """
        Initialize video class.

        :param resolution: the resolution of the video you want to export
        :param fps: the frames per second of the video you want to export
        :param path: the export path of the video you want to export
        """

        self.auto = isinstance(resolution, str)
        self.res = np.array((0, 0)) if self.auto else resolution
        self.fps = fps
        self.path = Path(path)
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.frame = 0

    def update(self, frame: np.ndarray):
        """
        Get frame updates and save them in tmp dir. Later compile on export.

        :param frame: next frame to be rendered
        """
        if self.auto:
            self.res = np.maximum(self.res, frame.shape[:2])

        cv2.imwrite(self.path / f"vidmaker_{self.frame}.png")

    def export(self):
        """
        Export the generated video.
        """
        video = cv2.VideoWriter(
            self.path, cv2.VideoWriter_fourcc(*"MPEG"), self.fps, self.res
        )
        for frame in Path(self.tmp_dir).iterdir():
            video.write(cv2.imread(frame))
        video.release()
        cv2.destroyAllWindows()
        self.tmp_dir.cleanup()
