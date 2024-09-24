from tkinter import *
from tkinter import font
from PIL import ImageTk, Image


class UserSignup:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

        # Create a frame for the signup section
        self.signup_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.signup_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Text
        self.txt = 'C r e a t e  A c c o u n t'
        signup_font = font.Font(family="Verdana", size=30, weight="bold")
        self.heading = Label(self.signup_frame, text=self.txt, font=signup_font, fg='#000000', bg='#f0f0f0')
        self.heading.place(x=46, y=290, width=400, height=60)

        # Logo
        self.side_logo = Image.open('Image/AshlingBankSmall.png')
        photo = ImageTk.PhotoImage(self.side_logo)
        self.side_logo_label = Label(self.signup_frame, image=photo, bg='#f0f0f0')
        self.side_logo_label.image = photo
        self.side_logo_label.place(x=90, y=80)

        # Textboxes with placeholders
        self.firstname_placeholder_text = 'Firstname'
        self.lastname_placeholder_text = 'Lastname'
        self.email_placeholder_text = 'Email'
        self.date_of_birth_placeholder_text = 'DD/MM/YYYY'
        self.password_placeholder_text = 'Password'
        self.confirm_password_placeholder_text = 'Confirm Password'

        self.firstname = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                               font=('Helvetica', 12, 'bold'))
        self.firstname.insert(0, self.firstname_placeholder_text)  # Placeholder text
        self.firstname.bind("<FocusIn>", self.on_entry_click)
        self.firstname.bind("<FocusOut>", self.on_focus_out)
        self.firstname.place(x=620, y=40, width=300, height=30)

        self.lastname = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'))
        self.lastname.insert(0, self.lastname_placeholder_text)  # Placeholder text
        self.lastname.bind("<FocusIn>", self.on_entry_click)
        self.lastname.bind("<FocusOut>", self.on_focus_out)
        self.lastname.place(x=620, y=100, width=300, height=30)

        self.email = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                           font=('Helvetica', 12, 'bold'))
        self.email.insert(0, self.email_placeholder_text)
        self.email.bind("<FocusIn>", self.on_entry_click)
        self.email.bind("<FocusOut>", self.on_focus_out)
        self.email.place(x=620, y=160, width=300, height=30)

        self.date_of_birth = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                                   font=('Helvetica', 12, 'bold'))
        self.date_of_birth.insert(0, self.date_of_birth_placeholder_text)
        self.date_of_birth.bind("<FocusIn>", self.on_entry_click)
        self.date_of_birth.bind("<FocusOut>", self.on_focus_out)
        self.date_of_birth.place(x=620, y=220, width=300, height=30)

        # Password Entry
        self.password = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'), show='')  # Initially show nothing
        self.password.insert(0, self.password_placeholder_text)  # Use the placeholder
        self.password.bind("<FocusIn>", self.on_password_focus)
        self.password.bind("<FocusOut>", self.on_password_focus_out)
        self.password.bind("<Key>", self.on_password_key)  # Bind key event to manage input
        self.password.place(x=620, y=280, width=192, height=30)

        self.confirm_password = Entry(self.signup_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                                      font=('Helvetica', 12, 'bold'), show='')
        self.confirm_password.insert(0, self.confirm_password_placeholder_text)
        self.confirm_password.bind("<FocusIn>", self.on_password_focus)
        self.confirm_password.bind("<FocusOut>", self.on_password_focus_out)
        self.confirm_password.bind("<Key>", self.on_password_key)
        self.confirm_password.place(x=620, y=340, width=300, height=30)

        # Buttons/Labels
        # Using Labels because of the border around the button
        self.create_account_btn = Label(self.signup_frame, highlightthickness=2, text='Create Account',
                                        font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                        bd=2, cursor='hand1')
        self.create_account_btn.bind("<Button-1>", self.create_account)
        self.create_account_btn.place(x=705, y=400)

        self.show_password_btn = Label(self.signup_frame, highlightthickness=2, text='Show password',
                                       font=('Helvetica', 12, 'bold'), fg='black', bg='white',
                                       bd=2, cursor='dot')
        self.show_password_btn.bind("<Button-1>", self.toggle_password)
        self.show_password_btn.place(x=820, y=280, width=100, height=30)


    def toggle_password(self, event):
        if self.password.cget('show') == '•':
            self.password.config(show='')
            self.show_password_btn.config(text='Hide password')
        else:
            self.password.config(show='•')
            self.show_password_btn.config(text='Show password')
    def create_account(self, event):
        print("It works")

    def on_entry_click(self, event):
        # Remove placeholder text when entry is clicked
        widget = event.widget
        placeholder_text = None

        if widget == self.firstname:
            placeholder_text = self.firstname_placeholder_text
        elif widget == self.lastname:
            placeholder_text = self.lastname_placeholder_text
        elif widget == self.email:
            placeholder_text = self.email_placeholder_text
        elif widget == self.date_of_birth:
            placeholder_text = self.date_of_birth_placeholder_text

        if placeholder_text and widget.get() == placeholder_text:
            widget.delete(0, "end")
            widget.config(fg='black')

    def on_focus_out(self, event):
        # Add placeholder when focus is lost and field is empty
        widget = event.widget
        placeholder_text = None

        if widget == self.firstname:
            placeholder_text = self.firstname_placeholder_text
        elif widget == self.lastname:
            placeholder_text = self.lastname_placeholder_text
        elif widget == self.email:
            placeholder_text = self.email_placeholder_text
        elif widget == self.date_of_birth:
            placeholder_text = self.date_of_birth_placeholder_text

        if placeholder_text and widget.get().strip() == '':
            widget.insert(0, placeholder_text)
            widget.config(fg='grey')

    def on_password_focus(self, event):
        widget = event.widget
        # Clear placeholder when focused
        if widget == self.password:
            if self.password.get() == self.password_placeholder_text:
                self.password.delete(0, "end")  # Remove placeholder text
                self.password.config(fg='black')
                self.password.config(show='')  # Show normal text
        elif widget == self.confirm_password:
            if self.confirm_password.get() == self.confirm_password_placeholder_text:
                self.confirm_password.delete(0, "end")
                self.confirm_password.config(fg='black')
                self.confirm_password.config(show='')

    def on_password_focus_out(self, event):
        widget = event.widget
        # Restore placeholder if field is empty
        if widget == self.password:
            if self.password.get().strip() == '':
                self.password.insert(0, self.password_placeholder_text)  # Restore placeholder
                self.password.config(fg='grey')
                self.password.config(show='')  # Show normal text
        elif widget == self.confirm_password:
            if self.confirm_password.get().strip() == '':
                self.confirm_password.insert(0, self.confirm_password_placeholder_text)
                self.confirm_password.config(fg='grey')
                self.confirm_password.config(show='')

    def on_password_key(self, event):
        widget = event.widget
        # Change to bullet points when typing
        if widget == self.password:
            if self.password.get() != self.password_placeholder_text:
                self.password.config(show='•')  # Show bullet points while typing
        elif widget == self.confirm_password:
            if self.confirm_password.get() != self.confirm_password_placeholder_text:
                self.confirm_password.config(show='•')


if __name__ == "__main__":
    window = Tk()
    UserSignup(window)
    window.title("Ashling-Create Account")
    window.mainloop()
