import requests
import glob
import hashlib
import os
import re
from time import sleep


# this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

base_url = 'http://api.thesubdb.com/'
user_agent = "SubDB/1.0 (PySubDBAutoFill/0.1; http://github.com/nikolajlauridsenn/PySubDB"
headers = {'User-Agent': user_agent}

files = glob.glob('*')
media_files = []
for file in files:
    media_re = re.search(r"^\S*?\.(mp4|avi|mkv)$", file)
    if media_re:
        media_files.append(file)
    else:
        pass

fail_count = 0
max_fails = 10

for file in media_files:
    f_hash = get_hash(file)
    payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
    print("Getting subtitle for " + file + "...", end="")
    response = requests.get(base_url, headers=headers, params=payload)
    if response.status_code == 200:
        f = open(file + '.srt', 'wb')
        f.write(response.content)
        f.close
        print("Done!\n")
        fail_count = 0
    else:
        print("\nThere's unfortunately no subtitle for this file at the moment\n")
        fail_count += 1

    if fail_count > max_fails:
        print("More than " + str(max_fails) + " files has failed in a row, exiting script.")
        break
sleep(2)
