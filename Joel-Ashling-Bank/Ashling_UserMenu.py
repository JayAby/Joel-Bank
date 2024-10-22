from tkinter import *
from tkinter import font
from PIL import ImageTk, Image

class UserMenu:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

        # Create a frame for the signup section
        self.menu_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Text
        self.txt = 'M e n u'
        signup_font = font.Font(family="Verdana", size=30, weight="bold")
        self.heading = Label(self.menu_frame, text=self.txt, font=signup_font, fg='#000000', bg='#f0f0f0')
        self.heading.place(x=46, y=290, width=400, height=60)

        # Logo
        self.side_logo = Image.open('Image/AshlingBankSmall.png')
        photo = ImageTk.PhotoImage(self.side_logo)
        self.side_logo_label = Label(self.menu_frame, image=photo, bg='#f0f0f0')
        self.side_logo_label.image = photo
        self.side_logo_label.place(x=90, y=80)

        # Set Window Icon
        window_logo = Image.open('Image/AshlingBank.png')
        window_logo = ImageTk.PhotoImage(window_logo)
        window.iconphoto(False, window_logo)

        # Buttons/Labels
        # Using Labels because of the border around the button
        self.view_account_balance = Label(self.menu_frame, highlightthickness=2, text='Account Details',
                                          font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                          bd=2)
        self.view_account_balance.bind("<Button-1>")
        self.view_account_balance.place(x=690, y=100, width=300, height=30)

        #
        self.transfer_money = Label(self.menu_frame, highlightthickness=2, text='Transfer Money',
                                    font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                    bd=2)
        self.transfer_money.bind("<Button-1>")
        self.transfer_money.place(x=690, y=160, width=300, height=30)

        #
        self.pay_bills = Label(self.menu_frame, highlightthickness=2, text='Pay Bills',
                               font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                               bd=2)
        self.pay_bills.bind("<Button-1>")
        self.pay_bills.place(x=690, y=220, width=300, height=30)

        #
        self.transaction_history = Label(self.menu_frame, highlightthickness=2, text='Transaction History',
                                         font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                         bd=2)
        self.transaction_history.bind("<Button-1>")
        self.transaction_history.place(x=690, y=280, width=300, height=30)

        #
        self.view_personal_details = Label(self.menu_frame, highlightthickness=2, text='Personal Details',
                                           font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                           bd=2)
        self.view_personal_details.bind("<Button-1>")
        self.view_personal_details.place(x=690, y=340, width=300, height=30)


if __name__ == "__main__":
    window = Tk()
    UserMenu(window)
    window.title("Ashling-User Menu")
    window.mainloop()
