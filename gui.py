from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class SubDownload(Frame):

    def print_dir(self):
        print(self.directory)

    def get_directory(self):
        self.directory = filedialog.askdirectory()

    def createWidgets(self):
        self.print_button = ttk.Button(root, text="Print dir", command=self.print_dir).grid(column=1, row=1, sticky=S)
        self.choose_dir = ttk.Button(root, text="Choose folder", command=self.get_directory).grid(column=2, row=1, sticky=S)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.directory = "Please choose a directory"
        self.createWidgets()

root = Tk()
root.title('Subtitle downloader')


mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

app = SubDownload(master=root)
app.mainloop()
