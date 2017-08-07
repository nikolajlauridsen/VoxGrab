"""
MIT License

Copyright (c) 2016-2017 Nikolaj Lauridsen

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


class SubDownloader(Frame):

    def __init__(self, master=None):
        # Inherit from frame
        Frame.__init__(self, master)
        self.master = master

        # String vars
        self.directory = StringVar()
        self.status = StringVar()
        self.status.set("Please choose a folder")

        # Pseudo booleans
        self.check_flag = IntVar()
        self.check_flag.set(1)

        self.files = []

        # Create widgets
        # The "important" widgets needed later
        self.status_label = Label(self.master, textvariable=self.status)
        self.file_area = Frame(self.master)

        self.canvas = Canvas(self.file_area, borderwidth=0,
                             background='#f0f0f0',
                             width=600, height=400)
        self.file_frame = Frame(self.canvas)

        self.create_widgets()

    def create_widgets(self):
        """Create widgets, saves init from becoming ridiculous"""
        # Create labels
        title_label = Label(self.master, text='VoxGrab\n subtitle downloader', font=16)

        # Create folder text input frame
        folder_fame = Frame(self.master)
        Entry(folder_fame, width=75,
              textvariable=self.directory).grid(column=0, row=1, padx=0, sticky=W)
        ttk.Button(folder_fame, text='Load files',
                   command=self.load_files).grid(column=1, row=1, padx=10)

        # Create scrolling area and scroll bar
        scrollbar = Scrollbar(self.file_area, orient='vertical',
                              command=self.canvas.yview)

        # Add title labels for columns
        Label(self.file_frame, text="File name", width="70",
              borderwidth="1", relief="solid").grid(row=0, column=0)
        Label(self.file_frame, text="Status", width="14",
              borderwidth="1", relief="solid").grid(row=0, column=1)

        # Configure, create & pack
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.create_window((4, 4), window=self.file_frame,
                                  anchor="nw", tags="self.file_frame")
        self.canvas.pack(side=LEFT)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create button pane
        button_pane = Frame(self.master)

        Checkbutton(button_pane, text='Skip downloaded subs',
                    variable=self.check_flag, justify=LEFT).grid(column=1, row=1, padx=100)
        ttk.Button(button_pane, text='Choose folder',
                   command=self.prompt_directory).grid(column=2, row=1, padx=10)
        ttk.Button(button_pane, text="Download subs",
                   command=self.download_subs).grid(column=3, row=1, padx=10)

        # Pack it all
        title_label.pack(pady=5)
        self.file_area.pack(padx=15, pady=5)
        folder_fame.pack(padx=5, pady=5)
        button_pane.pack(pady=5)
        self.status_label.pack(padx=5, pady=5)
        # Bind scrolling
        self.file_frame.bind("<Configure>", self.onFrameConfigure)
        self.file_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.file_frame.bind('<Leave>', self._unbound_to_mousewheel)
        self.master.bind('<Return>', self.load_files)

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

    def prompt_directory(self):
        """Prompt for directory, load files and populate gui"""
        self.directory.set(filedialog.askdirectory())
        self.load_files()

    def load_files(self, *args):
        try:
            self.files = self.sort_files(os.listdir(path=self.directory.get()))
            self.populate()
            if len(self.files) > 0:
                self.status.set("Click Download")
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

        # Re-create title labels for columns
        Label(self.file_frame, text="File name", width="70",
              borderwidth="1", relief="solid").grid(row=0, column=0)
        Label(self.file_frame, text="Status", width="14",
              borderwidth="1", relief="solid").grid(row=0, column=1)

        for i, file in enumerate(self.files):
            Label(self.file_frame, text=file["fileName"], width=70,
                  borderwidth="1", relief="solid").grid(row=i+1, column=0)

            Label(self.file_frame, text=file["status"], width="14", borderwidth="1",
                  relief="solid", bg=file["color"]).grid(row=i+1, column=1)
            file["row"] = i+1

    @staticmethod
    def sort_files(files):
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
        """
        Attempt to download subs to all files in self.files
        and set status label
        """
        if len(self.files) > 0:
            self.status.set('Downloading subtitles.')
            self.master.update()
            dl = Downloader(self.directory.get(), self.check_flag.get())
            for file in self.files:
                dl.download_file(file)

                label_config = {
                    'text': file['status'],
                    'width': 14,
                    'borderwidth': '1',
                    'relief': 'solid',
                    'bg': file['color']
                }
                Label(self.file_frame, **label_config).grid(row=file["row"],
                                                            column=1)
                self.master.update()
            self.status.set('Done Downloading subtitles.')
        else:
            self.status.set('No subtitles to download')


root = Tk()
root.title('VoxGrab')

app = SubDownloader(master=root)
app.mainloop()
