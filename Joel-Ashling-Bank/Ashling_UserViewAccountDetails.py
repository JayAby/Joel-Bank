from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from tkinter import font
from PIL import ImageTk, Image
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

DB_PATH = 'Ashling_UserRecords.db'

class UserViewAccount:
    def __init__(self, window):
        self.window = window
        self.logged_in_username = None  # Variable to store the logged-in username
        self.setup_ui()

    def setup_ui(self):
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

        # Create a frame for the account details section
        self.account_details_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.account_details_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Heading
        signup_font = font.Font(family="Verdana", size=20, weight="bold")
        self.heading = Label(self.account_details_frame, text="View Account Details", font=signup_font, fg='#000000',
                             bg='#f0f0f0')
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
        self.window.iconphoto(False, window_logo)

        # Authentication: Username and Password entries
        self.create_authentication_entries()

    def create_authentication_entries(self):
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
                              font=('Helvetica', 12, 'bold'), show='')
        self.password.insert(0, self.password_placeholder_text)
        self.password.bind("<FocusIn>", self.on_password_focus)
        self.password.bind("<FocusOut>", self.on_password_focus_out)
        self.password.bind("<Key>", self.on_password_key)
        self.password.place(x=620, y=220, width=192, height=30)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        # Reveal Account Details Button
        self.reveal_btn = Label(self.account_details_frame, highlightthickness=2, text='Reveal Account Details',
                                font=('Helvetica', 13, 'bold'), fg='black', bg='white', bd=2, cursor='hand2')
        self.reveal_btn.bind("<Button-1>", self.reveal)
        self.reveal_btn.place(x=695, y=300)

        # Show Password Button
        self.show_password_btn = Label(self.account_details_frame, highlightthickness=2, text='Show password',
                                       font=('Helvetica', 12, 'bold'), fg='black', bg='white', bd=2, cursor='dot')
        self.show_password_btn.bind("<Button-1>", self.toggle_password)
        self.show_password_btn.place(x=820, y=220, width=100, height=30)

    def reveal(self, event):
        entered_username = self.username.get()
        entered_password = self.password.get()

        if self.validate_user_input(entered_username, entered_password):
            user_details = self.get_user_details_from_db(entered_username, entered_password)
            if user_details:
                firstname = user_details[0]
                email_address = user_details[1]  # Assume the email is also returned
                self.logged_in_username = entered_username  # Store the logged-in username
                messagebox.showinfo("AshlingBank- Confirmation", f"Login Successful!\n Hi, {firstname}.")
                self.reset_entry(entered_username, entered_password)
            else:
                messagebox.showerror("AshlingBank- Error", "Invalid Login Details")
        else:
            messagebox.showerror("AshlingBank- Error", "Invalid Details")

    def validate_user_input(self, username, password):
        return username != self.username_placeholder_text and password != self.password_placeholder_text

    def get_user_details_from_db(self, username, password):
        try:
            db = sqlite3.connect(DB_PATH)
            cursor = db.cursor()
            cursor.execute("SELECT firstname, email FROM userPersonalDetails WHERE username=? AND password=?",
                           (username, password))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f'Database Error: {e}')
            return None
        finally:
            db.close()

    def reset_entry(self, entered_username, entered_password):
        # Destroy old widgets
        self.username.destroy()
        self.password.destroy()
        self.show_password_btn.destroy()
        self.reveal_btn.destroy()

        # Create new widgets for account details
        self.create_account_info_entries()

        # Fetch user details from the database and populate the fields
        self.populate_account_info(entered_username)

    def create_account_info_entries(self):
        # Account Balance Entry
        self.balance_label = Label(self.account_details_frame, text="Personal (£): ",
                                   font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.balance_label.place(x=620, y=100)
        self.balance = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0',
                             fg='grey', font=('Helvetica', 12, 'bold'))
        self.balance.config(state=DISABLED)  # Set as read-only initially
        self.balance.place(x=620, y=140, width=300, height=30)

        # Separator
        separator = ttk.Separator(self.account_details_frame, orient='horizontal')
        separator.place(x=520, y=205, width=500)

        # Account Number Entry
        self.account_number_label = Label(self.account_details_frame, text="Account Number: ",
                                          font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.account_number_label.place(x=620, y=218)
        self.account_number = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0',
                                    fg='grey', font=('Helvetica', 12, 'bold'))
        self.account_number.config(state=DISABLED)  # Set as read-only initially
        self.account_number.place(x=620, y=250, width=300, height=30)

        # Sort Code Entry
        self.sortcode_label = Label(self.account_details_frame, text="Sort Code: ", font=('Helvetica', 10, 'bold'),
                                    fg='black', bg='#f0f0f0')
        self.sortcode_label.place(x=620, y=318)
        self.sortcode = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'))
        self.sortcode.config(state=DISABLED)  # Set as read-only initially
        self.sortcode.place(x=620, y=350, width=300, height=30)

        # Add Money Button
        self.deposit_btn = Label(self.account_details_frame, highlightthickness=2, text='Add Money',
                                 font=('Helvetica', 13, 'bold'), fg='black', bg='white', bd=2, cursor='hand2')
        self.deposit_btn.bind("<Button-1>", self.add_money)
        self.deposit_btn.place(x=695, y=420)

    def populate_account_info(self, username):
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        try:
            # Get the customer_id from userPersonalDetails based on the username
            cursor.execute('''
                SELECT customer_id FROM userPersonalDetails WHERE username = ?;
            ''', (username,))
            customer_id = cursor.fetchone()

            if customer_id:
                customer_id = customer_id[0]
                print(f"Customer ID: {customer_id}")  # Debugging statement

                # Fetch account information
                cursor.execute('''
                    SELECT account_number, balance, sort_code 
                    FROM userAccountDetails 
                    WHERE customer_id = ?;
                ''', (customer_id,))
                account_details = cursor.fetchone()

                if account_details:
                    print(f"Account Details: {account_details}")  # Debugging statement

                    # Clear the current text in the entry fields before inserting new data
                    self.account_number.delete(0, 'end')  # Clear existing text
                    self.balance.delete(0, 'end')
                    self.sortcode.delete(0, 'end')

                    # Insert new account details into the textboxes
                    self.account_number.insert(0, account_details[0])
                    self.balance.insert(0, account_details[1])
                    self.sortcode.insert(0, account_details[2])
                else:
                    print("No account details found for this customer.")  # Debugging statement
                    messagebox.showerror("Error", "No account details found.")
            else:
                print("No customer ID found for the username.")  # Debugging statement
                messagebox.showerror("Error", "No customer found with that username.")
        except sqlite3.Error as e:
            print(f'Database Error: {e}')  # Error handling
            messagebox.showerror("Database Error", str(e))
        finally:
            db.close()

    def add_money(self, event):
        if self.logged_in_username:
            amount = simpledialog.askfloat("Deposit Amount", "Enter the amount to deposit:")
            if amount is not None and amount > 0:
                # Update account balance in the database
                db = sqlite3.connect(DB_PATH)
                cursor = db.cursor()
                try:
                    cursor.execute('''
                        UPDATE userAccountDetails 
                        SET balance = balance + ? 
                        WHERE customer_id = (SELECT customer_id FROM userPersonalDetails WHERE username = ?);
                    ''', (amount, self.logged_in_username))
                    db.commit()
                    messagebox.showinfo("Success", f"£{amount:.2f} has been deposited to your account.")
                    self.populate_account_info(self.logged_in_username)  # Refresh the displayed account info
                except sqlite3.Error as e:
                    print(f'Database Error: {e}')
                finally:
                    db.close()
            else:
                messagebox.showwarning("Invalid Amount", "Please enter a valid amount.")

    def on_entry_click(self, event):
        if self.username.get() == self.username_placeholder_text:
            self.username.delete(0, 'end')  # delete all the text in the entry
            self.username.config(fg='black')  # change text color to black

    def on_focus_out(self, event):
        if self.username.get() == '':
            self.username.insert(0, self.username_placeholder_text)
            self.username.config(fg='grey')

    def on_password_focus(self, event):
        if self.password.get() == self.password_placeholder_text:
            self.password.delete(0, 'end')  # delete all the text in the entry
            self.password.config(fg='black')  # change text color to black
            self.password.config(show='*')  # Show password as asterisks

    def on_password_focus_out(self, event):
        if self.password.get() == '':
            self.password.insert(0, self.password_placeholder_text)
            self.password.config(fg='grey')
            self.password.config(show='')  # Remove the asterisk

    def on_password_key(self, event):
        if self.password.get() != self.password_placeholder_text:
            self.password.config(fg='black')

    def toggle_password(self, event):
        if self.password.cget('show') == '':
            self.password.config(show='*')
        else:
            self.password.config(show='')


# Main code to run the app
if __name__ == '__main__':
    root = Tk()
    app = UserViewAccount(root)
    root.mainloop()
