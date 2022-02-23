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

import shutil
import time
import numpy as np
import cv2
import tempfile
import os


class Video:
    def __init__(self, path, fps, resolution="AUTO"):
        """
        Initialize video class.

        :param resolution: the resolution of the video you want to export
        :param fps: the frames per second of the video you want to export
        :param path: the export path of the video you want to export
        """

        self.auto = isinstance(resolution, str)
        self.res = np.array((0, 0)) if self.auto else np.array(resolution)
        self.fps = fps
        self.path = path
        self.tmp_dir = tempfile.mkdtemp()
        self.frame = 0
        self.frames = []

    def update(self, frame: np.ndarray):
        """
        Get frame updates and save them in tmp dir. Later compile on export.

        :param frame: next frame to be rendered
        """
        if self.auto:
            self.res = np.maximum(self.res, frame.shape[:2])

        saved = os.path.join(self.tmp_dir, f"vidmaker_{self.frame}.png")
        cv2.imwrite(saved, frame)
        self.frames.append(saved)
        self.frame += 1

    def export(self, verbose=False):
        """
        Export the generated video.
        """
        self.res = self.res[::-1]
        video = cv2.VideoWriter(
            self.path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, tuple(self.res)
        )
        frames = self.frames
        if verbose:
            print(f"Location: {self.path}")
            print("Format: .mp4")
            print(f"Resolution: {tuple(self.res)}")
            print(f"FPS: {self.fps}")
            from tqdm import tqdm

            frames = tqdm(self.frames, unit="frames", desc="Compiling")

        for frame in frames:
            img = cv2.cvtColor(
                cv2.imread(os.path.join(self.tmp_dir, frame)),
                cv2.COLOR_BGR2RGB,
            )
            video.write(img)

        video.release()
        cv2.destroyAllWindows()
        shutil.rmtree(self.tmp_dir)

        if verbose:
            vid_size = os.stat(self.path).st_size
            for unit in ["bytes", "KB", "MB", "GB", "TB"]:
                if vid_size < 1024:
                    print(f"File size: {round(vid_size, 2)} {unit}")
                    break
                vid_size /= 1024
