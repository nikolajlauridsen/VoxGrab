"""
MIT License

Copyright (c) 2016-17 Nikolaj Lauridsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import requests
import hashlib
import os

from VoxGrab import COLORS


class SubtitleDownloader:
    """Class handling interaction with thesubdb api"""

    def __init__(self, check_flag):
        # TODO: Change link
        self.base_url = 'http://sandbox.thesubdb.com'
        self.user_agent = 'SubDB/1.0 (VoxGrab/1.0;' \
                          ' https://github.com/nikolajlauridsen/VoxGrab'
        self.header = {'User-Agent': self.user_agent}
        self.check_flag = check_flag

    @staticmethod
    def get_hash(name):
        """Generate and return hash for a file"""
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def download_sub(self, file_model):
        """Request subtitle from thesubdb api and return true/false"""
        file_path = file_model["fileName"][:-4] + '.ENG' + '.srt'
        if os.path.isfile(file_path) and self.check_flag == 1:
            file_model["status"] = "Skipped"
            file_model["color"] = COLORS["d-green"]

        else:
            f_hash = self.get_hash(file_model["fileName"])
            payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
            response = requests.get(self.base_url, headers=self.header,
                                    params=payload)

            if response.status_code == 200:
                try:
                    with open(file_path, 'wb') as subtitle:
                        for chunk in response.iter_content(4096):
                            subtitle.write(chunk)
                    file_model["status"] = "Succeeded"
                    file_model["color"] = COLORS["green"]
                except:
                    file_model["status"] = "Failed"
                    file_model["color"] = COLORS["red"]
            else:
                file_model["status"] = "N/A"
                file_model["color"] = COLORS["yellow"]

