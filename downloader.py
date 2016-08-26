"""
Class handling interaction with thesubdb api
"""
import requests
import hashlib
import os


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

    def __init__(self, directory):
        self.base_url = 'http://api.thesubdb.com/'
        self.user_agent = 'SubDB/1.0 (PySubDBAutoFill/0.2;' \
                          ' https://github.com/nikolajlauridsen/PySubDBAutoFill'
        self.header = {'User-Agent': self.user_agent}
        self.directory = directory

    def download_file(self, file):
        """Request subtitle from thesubdb api and return true/false"""
        os.chdir(self.directory)

        print("Getting subtitle for " + file["fileName"] + "...", end="")
        f_hash = get_hash(file["fileName"])
        payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
        response = requests.get(self.base_url, headers=self.header, params=payload)
        if response.status_code == 200:
            f = open(file["fileName"][:-4] + '.srt', 'wb')
            f.write(response.content)
            f.close
            print("Done!\n")
            return True
        else:
            print('\nThere\'s unfortunately no subtitle'
                    ' for this file at the moment\n')
            return False
