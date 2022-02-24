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
    def __init__(self, path, fps="AUTO", resolution="AUTO", img_ext="jpg", cap=0):
        """
        Initialize video class.

        :param path: the export path of the video you want to export
        :param fps: the frames per second of the video you want to export, defaults to AUTO
        :param resolution: the resolution of the video you want to export, defaults to AUTO
        :param img_ext: the extension of the tmp image files, defaults to jpg
        :param cap: crash if video reaches length of _ hrs (worsens performance), defaults to 0 (no cap)
        """

        self.auto_res = isinstance(resolution, str)
        self.res = np.array((0, 0)) if self.auto_res else np.array(resolution)
        self.auto_fps = isinstance(fps, str)
        self.fps = fps
        self.path = path
        self.tmp_dir = tempfile.mkdtemp()
        self.frame = 0
        self.frames = []
        self.start_time = 0
        self.end_time = 0
        self.img_ext = img_ext
        self.cap = cap
        self.check_cap = cap != 0

    def update(self, frame: np.ndarray):
        """
        Get frame updates and save them in tmp dir. Later compile on export.

        :param frame: next frame to be rendered
        """
        if self.auto_res:
            self.res = np.maximum(self.res, frame.shape[:2])

        saved = os.path.join(self.tmp_dir, f"vidmaker_{self.frame}.{self.img_ext}")
        cv2.imwrite(saved, frame)
        self.frames.append(saved)
        self.frame += 1

        if self.frame == 1:
            self.start_time = time.time_ns()
        else:
            self.end_time = time.time_ns()

        if self.check_cap:
            if ((self.end_time - self.start_time) / 36000000000) > self.cap:
                print("Video cap reached, exporting and quiting...")
                self.export(True)
                raise SystemExit("vidmaker crashed because video length hit cap")

    def export(self, verbose=False):
        """
        Export the generated video.

        :param verbose: allow useful infomation to be outputted, defaults to False
        """

        if self.auto_res:
            self.res = self.res[::-1]

        secs = (self.end_time - self.start_time) / 1000000000
        if self.auto_fps:
            self.fps = round(self.frame / secs, 2)

        video = cv2.VideoWriter(
            self.path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, tuple(self.res)
        )
        frames = self.frames
        if verbose:
            print(f"Location: {self.path}")
            print("Format: .mp4")
            print(f"Resolution: {tuple(self.res)}")
            print(f"FPS: {self.fps}")

            m, s = divmod(secs, 60)
            h, m = divmod(m, 60)
            time_output = []
            if h > 0:
                time_output.append(f"{round(h, 1)} hours")
            if m > 0:
                time_output.append(f"{round(m, 1)} minutes")
            if s > 0:
                time_output.append(f"{round(s, 1)} seconds")
            print(f"Duration: {', '.join(time_output)}")

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
