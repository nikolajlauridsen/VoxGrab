from VoxGrab.VoxGrab import VoxGrab
from tkinter import Tk


def main():
    root = Tk()
    root.title('VoxGrab')
    root.iconbitmap('favicon.ico')

    app = VoxGrab(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
