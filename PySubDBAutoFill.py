import requests
import glob
import hashlib
import os


# this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

base_url = 'http://sandbox.thesubdb.com/'
user_agent = "SubDB/1.0 (PySubDBAutoFill/0.1; http://github.com/nikolajlauridsenn/PySubDB"

format = input("file format: ")
files = glob.glob('*.' + format)
headers = {'User-Agent': user_agent}

for file in files:
    f_hash = get_hash(file)
    payload = {'action': 'download', 'hash': f_hash, 'language': 'en'}
    print("Getting subtitle for " + file)
    response = requests.get(base_url, headers=headers, params=payload)
    print("done")
    f = open(file + '.srt', 'wb')
    f.write(response.content)
    f.close
