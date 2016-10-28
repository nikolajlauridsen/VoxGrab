"""
MIT License

Copyright (c) [2016] [Nikolaj Lauridsen]

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

colors = {
    "azure": "#007fff",
    "green": "#3fff00",
    "red": "#e62020",
    "yellow": "#ffc40c",
    "d-green": "#177245"
}


def get_hash(name):
    """Generate and return hash for a file"""
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


class Downloader():
    """Class handling interaction with thesubdb api"""

    def __init__(self, directory, check_flag):
        self.base_url = 'http://api.thesubdb.com/'
        self.user_agent = 'SubDB/1.0 (VoxGrab/1.0;' \
                          ' https://github.com/nikolajlauridsen/VoxGrab'
        self.header = {'User-Agent': self.user_agent}
        self.directory = directory
        self.check_flag = check_flag

    def download_file(self, file):
        """Request subtitle from thesubdb api and return true/false"""
        os.chdir(self.directory)
        file_path = file["fileName"][:-4] + '.srt'
        if os.path.isfile(file_path) and self.check_flag == 1:
            file["status"] = "Skipped"
            file["color"] = colors["d-green"]

        else:
            f_hash = get_hash(file["fileName"])
            payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
            response = requests.get(self.base_url, headers=self.header, params=payload)
            if response.status_code == 200:
                try:
                    with open(file["fileName"][:-4] + '.srt', 'wb') as subtitle:
                        for chunk in response.iter_content(4096):
                            subtitle.write(chunk)
                        subtitle.close
                    file["status"] = "Succeeded"
                    file["color"] = colors["green"]
                except:
                    file["status"] = "Failed"
                    file["color"] = colors["red"]
            else:
                file["status"] = "N/A"
                file["color"] = colors["yellow"]
