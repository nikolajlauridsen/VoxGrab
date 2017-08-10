# VoxGrab
Subtitles the easy way, as served by [TheSubDB](http://thesubdb.com/)

(I'm not affiliated with TheSubDB in any way shape or form other than using their service.)
<center>![VoxGrab](screenshot.PNG)<\center>

VoxGrab is fairly self explanatory, downloading subtitles one at a time can be a real pain! 
 Especially if you need subtitles for an entire season of a tv show. 
 This is where VoxGrab comes to the rescue, with a few clicks VoxGrab will have downloaded 
 all the subtitles in mere seconds (depending on internet speed, and quality of potato). 

# How to use
Using VoxGrab is as easy as it comes, if you're a windows user enter the VoxGrab folder and 
launch VoxGrab.exe, Linux/Mac users double click VoxGrab.pyw.

(if you wish to launch VoxGrab from the desktop simply make a shortcut to VoxGrab.exe and move that.) 

Once the program is up and running click choose folder and navigate to the folder with your 
media files and hit enter (or copy/paste the folder path into the entry frame and click load files, this is often faster)

The media files will now show up in the file list with a blue waiting status, 
now simply click the download button and your subtitles will be downloaded.

#### Where's my subtitles?
VoxGrab will save the subtitles in the same folder as the media files under the same name, 
but suffixed with .ENG (this will let [Plex](https://www.plex.tv/) find the subtitles and properly qualify them as English)

#### Why aren't you supporting more languages?
TheSubDB also supports:
* Dutch
* French
* Italian
* Polish
* Portuguese (Brazil)
* Romanian
* Spanish
* Swedish
* Turkish

However since I speak none of those languages I chose to focus on other features first, 
but multi language support is coming in version 1.3!

# Install process
#### Windows
1. Download VoxGrab.zip and extract
2. You're good to go

#### GNU/Linux & Mac
1. Download and install python from https://www.python.org/ (If you're unsure download version 3.6 and chose default install)
2. Clone or download/extract the repository
3. Install requirements with 
```
python -m pip install -r requirements.txt
```
(You might have to use python3 or py instead of python depending on your system/install)

##### Requirements
* requests
* Tkinter

# In case of bugs or concerns
If you have any issue with VoxGrab please create an issue [here](https://github.com/nikolajlauridsen/VoxGrab/issues)

Or email me at: nikolajlauridsen@protonmail.ch

# Interested in contributing?
That would make me happy! Simply fork the repository, make your changes and submit a pull request.
It would be very helpful if you create an issue first stating what you'll be doing and 
that you're working on it, that way no one steps on anyone's toes.
