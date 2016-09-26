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
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from downloader import Downloader

import os
import re

colors = {
    "azure": "#007fff",
    "green": "#3fff00",
    "red": "#e62020",
    "yellow": "#ffc40c",
    "d-green": "#177245"
}


class SubDownload(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.directory = 'Please choose a directory'
        self.files = []
        self.status = StringVar()
        self.check_flag = IntVar()  # 1 for True 0 for false
        self.check_flag.set(1)      # Set default state to true
        self.status.set("Please choose a folder")
        self.create_widgets()

    def create_widgets(self):
        """create widgets (saves __init__ from becoming overly long)"""
        # Create & place labels
        self.title_label = ttk.Label(text='Subtitle downloader').grid(column=2, row=1, sticky=W, pady=5)
        self.status_label = Label(root, textvariable=self.status).grid(column=2, row=4, sticky=W)

        # Create & place buttons
        self.choose_dir = ttk.Button(root, text='Choose folder',
                                     command=self.load_files).grid(column=2, row=3, sticky=W, pady=5)
        self.download_button = ttk.Button(root, text='Download subs',
                                          command=self.download_subs).grid(column=2, row=3, sticky=E)
        self.file_Checkbutton = Checkbutton(root, text="Skip downloaded subs",
                                            variable=self.check_flag, justify=LEFT).grid(column=1, row=3, sticky=W+E)

        # Crate canvas, file_frame and vertical scrollbar (subtitle area)
        self.canvas = Canvas(root, borderwidth=0, background="#f0f0f0", width=600, height=400)
        self.file_frame = Frame(self.canvas)
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # Add title labels
        Label(self.file_frame, text="Files", width="70",
              borderwidth="1", relief="solid").grid(row=0, column=0)
        Label(self.file_frame, text="Status", width="14",
              borderwidth="1", relief="solid").grid(row=0, column=1)

        # Place vertical scrollbar, canvas and create windows
        self.vsb.grid(column=4, row=2, rowspan=1, padx=(0,5), sticky=N+S+W)
        self.canvas.grid(column=1, row=2, columnspan=3, padx=(15,0), pady=(0,10))
        self.canvas.create_window((4,4), window=self.file_frame, anchor="nw",
                                  tags="self.file_frame")
        # Bind scrolling
        self.file_frame.bind("<Configure>", self.onFrameConfigure)
        self.file_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.file_frame.bind('<Leave>', self._unbound_to_mousewheel)

    def load_files(self):
        """Prompt for directory, load files and populate gui"""
        try:
            self.directory = filedialog.askdirectory()
            self.files = self.sort_files(os.listdir(path=self.directory))
            self.populate()
            if len(self.files) > 0:
                self.status.set("Click download")
            else:
                self.status.set("No media in folder")
        except FileNotFoundError:
            self.status.set("That's not a folder")

    def clear_download_frame(self):
        """Clears file_frame"""
        for widget in self.file_frame.winfo_children():
            widget.destroy()

    def populate(self):
        """Populate/refresh file_frame"""
        self.clear_download_frame()

        for i, file in enumerate(self.files):
            Label(self.file_frame, text=file["fileName"], width=70,
                  borderwidth="1", relief="solid").grid(row=i+1, column=0)

            Label(self.file_frame, text=file["status"], width="14", borderwidth="1",
                  relief="solid", bg=file["color"]).grid(row=i+1, column=1)
            file["row"] = i+1

    def sort_files(self, files):
        """Sort out non media files"""
        media_files = []
        for file in files:
            media_re = re.search(r"^[\s\S]*?\.(mp4|avi|mkv|m4v)$", file)
            if media_re:
                context = {"fileName": file,
                           "status": "Waiting",
                           "color": colors["azure"]}
                media_files.append(context)
            else:
                pass
        return media_files

    def download_subs(self):
        """Attempt to download subs to all files in self.files and set status label"""
        if len(self.files) > 0:
            self.status.set('Downloading subtitles.')
            root.update()
            dl = Downloader(self.directory, self.check_flag.get())
            for file in self.files:
                dl.download_file(file)
                Label(self.file_frame, text=file["status"], width="14", borderwidth="1",
                      relief="solid", bg=file["color"]).grid(row=file["row"], column=1)
                root.update()
            self.status.set('Done Downloading subtitles.')
        else:
            self.status.set('No subtitles to download')

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner file_frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bound_to_mousewheel(self, event):
        """Bind mousewheel to scroll function"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        """Unbind mousewheel"""
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Scrolling function"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root = Tk()
root.title('VoxGrab')

app = SubDownload(master=root)
app.mainloop()
