from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import customtkinter


class UserViewAccount:
    def __init__(self, window):
        self.window = window
        self.setup_ui()

    def setup_ui(self):
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

        # Create a frame for the account details section
        self.account_details_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.account_details_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Text
        self.txt = 'View Account Details'
        signup_font = font.Font(family="Verdana", size=20, weight="bold")
        self.heading = Label(self.account_details_frame, text=self.txt, font=signup_font, fg='#000000', bg='#f0f0f0')
        self.heading.place(x=46, y=290, width=400, height=60)

        # Logo
        self.side_logo = Image.open('Image/AshlingBankSmall.png')
        photo = ImageTk.PhotoImage(self.side_logo)
        self.side_logo_label = Label(self.account_details_frame, image=photo, bg='#f0f0f0')
        self.side_logo_label.image = photo
        self.side_logo_label.place(x=90, y=80)

        # Set Window Icon
        window_logo = Image.open('Image/AshlingBank.png')
        window_logo = ImageTk.PhotoImage(window_logo)
        window.iconphoto(False, window_logo)

        # Authentication

        # Textboxes with placeholders
        self.username_placeholder_text = 'Username'
        self.password_placeholder_text = 'Password'

        # Username Entry
        self.username = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'))
        self.username.insert(0, self.username_placeholder_text)
        self.username.bind("<FocusIn>", self.on_entry_click)
        self.username.bind("<FocusOut>", self.on_focus_out)
        self.username.place(x=620, y=160, width=300, height=30)

        # Password Entry
        self.password = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'), show='')  # Initially show nothing
        self.password.insert(0, self.password_placeholder_text)  # Use the placeholder
        self.password.bind("<FocusIn>", self.on_password_focus)
        self.password.bind("<FocusOut>", self.on_password_focus_out)
        self.password.bind("<Key>", self.on_password_key)  # Bind key event to manage input
        self.password.place(x=620, y=220, width=192, height=30)

        # Buttons/Labels
        # Using Labels because of the border around the button
        self.reveal_btn = Label(self.account_details_frame, highlightthickness=2, text='Reveal Account Details',
                                font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                                bd=2, cursor='hand2')
        self.reveal_btn.bind("<Button-1>", self.reveal)
        self.reveal_btn.place(x=695, y=300)

        self.show_password_btn = Label(self.account_details_frame, highlightthickness=2, text='Show password',
                                       font=('Helvetica', 12, 'bold'), fg='black', bg='white',
                                       bd=2, cursor='dot')
        self.show_password_btn.bind("<Button-1>", self.toggle_password)
        self.show_password_btn.place(x=820, y=220, width=100, height=30)


    # Functions
    def save_money(self):
        pass

    def add_money(self, event):
        while True:
            # Display the input dialog to ask user how much they want to deposit
            deposit_amount_dialog = customtkinter.CTkInputDialog(text="How much would you like to Add? ", title="AshlingBank- Deposit")

            # Retreive User input
            deposit_amount = deposit_amount_dialog.get_input()

            if deposit_amount is None:
                messagebox.showerror("AshlingBank- Error", "No amount added.")
                return None

            try:
                deposit_amount = float(deposit_amount)
                if deposit_amount <= 0:
                    messagebox.showerror("AshlingBank- Error", "Please enter a positive value.")
                elif deposit_amount > 5000:
                    messagebox.showerror("AshlingBank- Error", "You can only deposit a maximum of £5,000.")
                else:
                    messagebox.showinfo("AshlingBank - Confirmation", " £" + deposit_amount + " has been added to your balance")
                    return deposit_amount

            except ValueError:
                messagebox.showerror("AshlingBank- Error", "Invalid input. Please enter a valid amount. ")



    def reveal(self, event):
        entered_username = self.username.get()
        entered_password = self.password.get()

        if self.validate_user_input(entered_username, entered_password):
            user_details = self.get_user_details_from_db(entered_username, entered_password)
            if user_details:
                firstname = user_details[0]
                messagebox.showinfo("AshlingBank- Confirmation", f"Login Successful!\n Hi, {firstname}.")
                self.reset_entry()
            else:
                messagebox.showerror("AshlingBank- Error", "Invalid Login Details")
        else:
            messagebox.showerror("AshlingBank- Error", "Invalid Details")

    def validate_user_input(self, username, password):
        return username != self.username_placeholder_text and password != self.password_placeholder_text

    def get_user_details_from_db(self, username, password):
        try:
            db = sqlite3.connect('Ashling-UserRecords.db')
            cursor = db.cursor()
            cursor.execute("SELECT firstname FROM userPersonalDetails WHERE username=? AND password=?", (username, password))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f'Database Error: {e}')
            return None
        finally:
            db.close()


    # Functions
    def reset_entry(self):
        entered_username= self.username.get()
        entered_password = self.password.get()

        self.username.destroy()
        self.password.destroy()
        self.show_password_btn.destroy()
        self.reveal_btn.destroy()

        # Account Label & Entry
        self.account_balance_label = Label(self.account_details_frame, text="Personal (£): ", font=('Helevtica', 10, 'bold'),fg='black', bg='#f0f0f0' )
        self.account_balance_label.place(x=620, y=100)
        self.account_balance = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',font=('Helvetica', 12, 'bold'))
        self.account_balance.place(x=620, y=140, width=300, height=30)

        # Put a separator
        separator = ttk.Separator(self.account_details_frame, orient='horizontal')
        separator.place(x=520, y=205, width=500)

        # Account Number & Entry
        self.account_number_label = Label(self.account_details_frame, text="Account Number: ", font=('Helevtica', 10, 'bold'),fg='black', bg='#f0f0f0' )
        self.account_number_label.place(x=620, y=218)
        self.account_number = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',font=('Helvetica', 12, 'bold'))
        self.account_number.place(x=620, y=250, width=300, height=30)

        # Sortcode & Entry
        self.sortcode_label = Label(self.account_details_frame, text="Sort Code: ",
                                          font=('Helevtica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.sortcode_label.place(x=620, y=318)
        self.sortcode = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0',
                                    fg='grey', font=('Helvetica', 12, 'bold'))
        self.sortcode.place(x=620, y=350, width=300, height=30)

        # Deposit Money Button
        self.deposit_btn = Label(self.account_details_frame, highlightthickness=2, text='Add Money',
                               font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                               bd=2, cursor='hand2')
        self.deposit_btn.bind("<Button-1>", self.add_money)
        self.deposit_btn.place(x=730, y=420)

        # Get the values from the db
        db = sqlite3.connect('Ashling-UserRecords.db')
        cursor = db.cursor()
        # Query to join tables and retrieve neccesary details
        cursor.execute('''
        SELECT userAccountDetails.balance, userAccountDetails.account_number, userAccountDetails.sort_code
        FROM userAccountDetails
        JOIN userPersonalDetails ON userAccountDetails.customer_id = userPersonalDetails.customer_id
        WHERE userPersonalDetails.username = ? AND userPersonalDetails.password = ?;
        ''', (entered_username, entered_password))

        # fetch the result
        result = cursor.fetchone()

        # Check if result was found
        if result:
            balance, account_number, sort_code = result
            self.account_balance.delete(0,END)
            self.account_balance.insert(0,balance)
            self.account_balance.config(state=DISABLED)
            self.account_number.delete(0, END)
            self.account_number.insert(0, account_number)
            self.account_number.config(state=DISABLED)
            self.sortcode.delete(0,END)
            self.sortcode.insert(0,sort_code)
            self.sortcode.config(state=DISABLED)

        else:
            messagebox.showerror("AshlingBank- Error", "No matching records found or Incorrect username/password")

        db.close()

    def on_entry_click(self, event):
        # Remove placeholder text when entry is clicked
        widget = event.widget
        placeholder_text = None

        if widget == self.username:
            placeholder_text = self.username_placeholder_text

        if placeholder_text and widget.get() == placeholder_text:
            widget.delete(0, "end")
            widget.config(fg='black')

    def on_focus_out(self, event):
        # Add placeholder when focus is lost and field is empty
        widget = event.widget
        placeholder_text = None

        if widget == self.username:
            placeholder_text = self.username_placeholder_text

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

    def on_password_focus_out(self, event):
        widget = event.widget
        # Restore placeholder if field is empty
        if widget == self.password:
            if self.password.get().strip() == '':
                self.password.insert(0, self.password_placeholder_text)  # Restore placeholder
                self.password.config(fg='grey')
                self.password.config(show='')  # Show normal text
    def on_password_key(self, event):
        widget = event.widget
        # Change to bullet points when typing
        if widget == self.password:
            if self.password.get() != self.password_placeholder_text:
                self.password.config(show='•')  # Show bullet points while typing

    def toggle_password(self, event):
        if self.password.cget('show') == '•':
            self.password.config(show='')
            self.show_password_btn.config(text='Hide password')
        else:
            self.password.config(show='•')
            self.show_password_btn.config(text='Show password')



if __name__ == "__main__":
    window = Tk()
    UserViewAccount(window)
    window.title("Ashling-View Account Details")
    window.mainloop()
