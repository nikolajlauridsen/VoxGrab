from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from downloader import Downloader

import os
import re


class SubDownload(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.directory = 'Please choose a directory'
        self.files = []
        self.status = StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(text='Subtitle downloader').grid(column=2, row=1, sticky=S)

        self.download_button = ttk.Button(root, text='Download subs',
                                          command=self.download_subs).grid(column=3, row=3, sticky=W)
        self.choose_dir = ttk.Button(root, text='Choose folder',
                                     command=self.get_directory).grid(column=1, row=3, sticky=E)

        self.canvas = Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(column=4, row=1, rowspan=2)
        self.canvas.grid(column=1, row=2, columnspan=3)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.status_label = Label(root, textvariable=self.status).grid(column=2, row=4, sticky=S)

    def get_directory(self):
        self.directory = filedialog.askdirectory()
        self.files = self.sort_files(os.listdir(path=self.directory))
        self.populate()

    def populate(self):
        i = 0
        for file in self.files:
            Label(self.frame, text=file["fileName"], width=54, borderwidth="1",
                  relief="solid").grid(row=i, column=0)
            file["row"] = i
            i += 1

    def sort_files(self, files):
        media_files = []
        for file in files:
            media_re = re.search(r"^[\s\S]*?\.(mp4|avi|mkv|m4v)$", file)
            if media_re:
                context = {"fileName": file,
                           "status": "waiting"}
                media_files.append(context)
            else:
                pass
        return media_files

    def download_subs(self):
        self.status.set('Downloading subtitles.')
        root.update()
        dl = Downloader(self.directory, self.files)
        dl.download_files()
        self.status.set('Done Downloading subtitles.')


    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



root = Tk()
root.title('Subtitle downloader')


mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

app = SubDownload(master=root)
app.mainloop()
