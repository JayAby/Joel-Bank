from email.mime.base import MIMEBase
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import customtkinter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os
from datetime import datetime



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
    def save_money(self, deposit_amount, account_number, customer_id):
        db = sqlite3.connect('Ashling-UserRecords.db')
        update_query = "UPDATE userAccountDetails SET balance = balance + ? WHERE account_number = ?"
        log_deposit_query = "INSERT INTO dailyDeposits (customer_id, amount) VALUES (?,?)"
        transaction_query = '''
            INSERT INTO transactionDetails(sender_account_id, recipient_account_id, amount_out, transaction_status)
            VALUES (?,?,?,?)
        '''

        try:
            cursor = db.cursor()
            # Update user's account
            cursor.execute(update_query, (deposit_amount, account_number))
            # Log deposit in daily deposits
            cursor.execute(log_deposit_query, (customer_id, deposit_amount))
            # Log the transaction into transaction details
            # Assuming sender and recipient are the same
            cursor.execute(transaction_query, (customer_id, customer_id, deposit_amount, "Self-Deposit"))
            db.commit()
            print("Amount added & Transaction Logged!")

            # Retrieve user's firstname and email
            firtsname, email_address = self.get_user_firstname_and_email(customer_id)

            # Send the email notification
            if firtsname and email_address:
                today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.send_notification_email(firtsname, email_address, deposit_amount, today_str)
                print("Notification email sent.")

        except Exception as e:
            print(f"Error: {e}")
            db.rollback()
        finally:
            db.close()

    def get_customer_id(self, username):
        try:
            db = sqlite3.connect('Ashling-UserRecords.db')
            cursor = db.cursor()
            # Retrieve customer ID based on username
            cursor.execute("SELECT customer_id FROM userPersonalDetails WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the customer_id
            else:
                print("Customer ID not found for this username.")
                return None
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return None
        finally:
            db.close()

    def get_user_firtsname_and_email(self, customer_id):
        try:
            db = sqlite3.connect('Ashling-UserRecords.db')
            cursor = db.cursor()
            # Retreive firstname and email based on customer ID
            cursor.execute("SELECT firstname, email FROM userPersonalDetails WHERE customer_id =?", (customer_id,))
            result = cursor.fetchone()
            if result:
                return result # returns firstname and email
            else:
                return None, None

        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return  None, None
        finally:
            db.close()

    def add_money(self, event):
        # Check if self.username exists
        if hasattr(self, 'username') and self.username.winfo_exists():
            entered_username = self.username.get()
        else:
            messagebox.showerror("AshlingBank - Error", "Username entry no longer exists.")
            return

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
                    # Get customerID based on the username provided
                    customer_id = self.get_customer_id(self.username.get())
                    daily_total = self.get_daily_deposit_total(customer_id)

                    if daily_total + deposit_amount > 15000:
                        messagebox.showerror("AshlingBank- Error", "You've hit the maximum daily deposit of £15,000.")
                    else:
                        account_number = self.account_number.get()
                        self.save_money(deposit_amount, account_number, customer_id)
                        messagebox.showinfo("AshlingBank - Confirmation",
                                            f"£{deposit_amount} has been added to your balance.")
                        # Update displayed balance
                        new_balance = float(self.account_balance.get()) + deposit_amount
                        self.account_balance.config(state=NORMAL)
                        self.account_balance.delete(0, END)
                        self.account_balance.insert(0, new_balance)
                        self.account_balance.config(state=DISABLED)
                        return

            except ValueError:
                messagebox.showerror("AshlingBank- Error", "Invalid input. Please enter a valid amount. ")

    def send_notification_email(self, firstname, email_address, deposit_amount, today_str):
        # Email setup
        sender_email = "jay.aby.codes@gmail.com"
        sender_password = "jwcabxkjbjjoqbck"
        subject = "Ashling Bank- Deposit Notification"

        # Create the username content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_address
        message['Subject'] = subject

        # Email body
        body = f"""
        Dear {firstname} ,

        You are receiving this message because you have deposited £ {deposit_amount} into your account on this day: {today_str}
        
        Your new account balance can be seen in the app.
        
        If you didn't make this deposit, please do well to let us know

        Best regards,
        Ashling Bank Team
        """

        message.attach(MIMEText(body, 'plain'))

        # Attaching an image
        image_path = "Image/AshlingBank.png"
        try:
            with open(image_path, "rb") as image_file:
                # Set the MIMEBase object
                image = MIMEBase('application', 'octet-stream')
                image.set_payload(image_file.read())

                # Encode the image in base64 and attach it to the username
                encoders.encode_base64(image)

                # Add the necessary headers for the image
                image.add_header('Content-Disposition', f"attachment; filename = {os.path.basename(image_path)}")

                # Attach the image to the message
                message.attach(image)

        except Exception as e:
            print(f"Error attaching image: {e}")

        # Sending the username
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, email_address, text)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending username: {e}")

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
    # Update the reset_entry method
    def reset_entry(self):
        entered_username = self.username.get()
        entered_password = self.password.get()

        # Destroy the previous widgets before creating new ones
        self.username.destroy()
        self.password.destroy()
        self.show_password_btn.destroy()
        self.reveal_btn.destroy()

        # Create new widgets for account balance, account number, and sort code entries
        self.account_balance_label = Label(self.account_details_frame, text="Personal (£): ",
                                           font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.account_balance_label.place(x=620, y=100)
        self.account_balance = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0',
                                     fg='grey', font=('Helvetica', 12, 'bold'))
        self.account_balance.place(x=620, y=140, width=300, height=30)

        # Put a separator
        separator = ttk.Separator(self.account_details_frame, orient='horizontal')
        separator.place(x=520, y=205, width=500)

        # Account Number & Entry
        self.account_number_label = Label(self.account_details_frame, text="Account Number: ",
                                          font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.account_number_label.place(x=620, y=218)
        self.account_number = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0',
                                    fg='grey', font=('Helvetica', 12, 'bold'))
        self.account_number.place(x=620, y=250, width=300, height=30)

        # Sort code & Entry
        self.sortcode_label = Label(self.account_details_frame, text="Sort Code: ", font=('Helvetica', 10, 'bold'),
                                    fg='black', bg='#f0f0f0')
        self.sortcode_label.place(x=620, y=318)
        self.sortcode = Entry(self.account_details_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'))
        self.sortcode.place(x=620, y=350, width=300, height=30)

        # Add Money Button
        self.deposit_btn = Label(self.account_details_frame, highlightthickness=2, text='Add Money',
                                 font=('Helvetica', 13, 'bold'), fg='black', bg='white', bd=2, cursor='hand2')
        self.deposit_btn.bind("<Button-1>", self.add_money)
        self.deposit_btn.place(x=730, y=420)

        # Fetch user details from the database
        db = sqlite3.connect('Ashling-UserRecords.db')
        cursor = db.cursor()
        cursor.execute('''
        SELECT userAccountDetails.balance, userAccountDetails.account_number, userAccountDetails.sort_code
        FROM userAccountDetails
        JOIN userPersonalDetails ON userAccountDetails.customer_id = userPersonalDetails.customer_id
        WHERE userPersonalDetails.username = ? AND userPersonalDetails.password = ?;
        ''', (entered_username, entered_password))

        result = cursor.fetchone()

        # Update the fields if the result is found
        if result:
            balance, account_number, sort_code = result
            self.account_balance.delete(0, END)
            self.account_balance.insert(0, balance)
            self.account_balance.config(state=DISABLED)

            self.account_number.delete(0, END)
            self.account_number.insert(0, account_number)
            self.account_number.config(state=DISABLED)

            self.sortcode.delete(0, END)
            self.sortcode.insert(0, sort_code)
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
