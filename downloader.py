import requests
import hashlib
import os
import re


# this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


class Downloader():

    def __init__(self, directory, files):
        self.base_url = 'http://api.thesubdb.com/'
        self.user_agent = 'SubDB/1.0 (PySubDBAutoFill/0.2;' \
                          ' https://github.com/nikolajlauridsen/PySubDBAutoFill'
        self.header = {'User-Agent': self.user_agent}
        self.files = files
        self.directory = directory
        self.media_files = []

    def sort_files(self):
        for file in self.files:
            media_re = re.search(r"^[\s\S]*?\.(mp4|avi|mkv|m4v)$", file)
            if media_re:
                self.media_files.append(file)
            else:
                pass

    def download_files(self):
        os.chdir(self.directory)
        fail_count = 0
        max_fails = 10

        for file in self.media_files:
            print("Getting subtitle for " + file + "...", end="")
            f_hash = get_hash(file)
            payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
            response = requests.get(self.base_url, headers=self.header, params=payload)
            if response.status_code == 200:
                f = open(file[:-4] + '.srt', 'wb')
                f.write(response.content)
                f.close
                print("Done!\n")
                fail_count = 0
            else:
                print('\nThere\'s unfortunately no subtitle' +
                      ' for this file at the moment\n')
                fail_count += 1

            if fail_count > max_fails:
                print('More than ' + str(max_fails) +
                      ' files has failed in a row, exiting script.')
                break
