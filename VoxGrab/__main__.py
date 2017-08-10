from VoxGrab.VoxGrab import VoxGrab
from tkinter import Tk


def main():
    root = Tk()
    root.title('VoxGrab')

    app = VoxGrab(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
