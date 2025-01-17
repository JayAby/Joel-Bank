from tkinter import *
from Ashling_UserLogin import UserLogin

if __name__ == "__main__":
    window = Tk()

    window.geometry('1024x768')
    window.state('zoomed')
    window.title("Ashling Bank")
    window.resizable(0, 0)

    UserLogin(window)

    window.mainloop()
