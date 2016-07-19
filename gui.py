from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import os


class SubDownload(Frame):

    def print_dir(self):
        print(self.directory)

    def print_files(self):
        self.get_files()
        for file in self.files:
            print(file)

    def get_directory(self):
        self.directory = filedialog.askdirectory()

    def get_files(self):
        self.files = os.listdir(path=self.directory)

    def create_widgets(self):
        self.title_label = ttk.Label(text='Subtitle downloader').grid(column=2, row=1, sticky=NSEW)
        self.print_button = ttk.Button(root, text='Print dir',
                                       command=self.print_dir).grid(column=2, row=2, sticky=S)
        self.choose_dir = ttk.Button(root, text='Choose folder',
                                     command=self.get_directory).grid(column=1, row=2, sticky=S)
        self.print_files = ttk.Button(root, text='Print files',
                                      command=self.print_files).grid(column=3, row=2, sticky=S)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.directory = 'Please choose a directory'
        self.files = []
        self.create_widgets()

root = Tk()
root.title('Subtitle downloader')


mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

app = SubDownload(master=root)
app.mainloop()
