import os
import smtplib
import sqlite3
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import font

import customtkinter
from PIL import ImageTk, Image
from datetime import datetime

DB_PATH = 'Ashling_UserRecords.db'


class UserTransfer:
    def __init__(self, window, logged_in_user):
        self.window = window
        self.window.configure(bg='#ffffff')

        self.logged_in_user = logged_in_user

        # Create a frame for the signup section
        self.main_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Text
        self.txt = 'P a y  S o m e o n e'
        signup_font = font.Font(family="Verdana", size=30, weight="bold")
        self.heading = Label(self.main_frame, text=self.txt, font=signup_font, fg='#000000', bg='#f0f0f0')
        self.heading.place(x=46, y=290, width=400, height=60)

        # Logo
        self.side_logo = Image.open('Image/AshlingBankSmall.png')
        photo = ImageTk.PhotoImage(self.side_logo)
        self.side_logo_label = Label(self.main_frame, image=photo, bg='#f0f0f0')
        self.side_logo_label.image = photo
        self.side_logo_label.place(x=90, y=80)

        # Set Window Icon
        window_logo = Image.open('Image/AshlingBank.png')
        window_logo = ImageTk.PhotoImage(window_logo)
        window.iconphoto(False, window_logo)

        # Textboxes with Placeholders
        self.sort_code_placeholder_text = 'Enter recipient sort-code'
        self.account_number_placeholder_text = 'Enter recipient account number'
        self.account_name_placeholder_text = 'Name of recipient'
        self.send_date_placeholder_text = 'DD/MM/YYYY'

        #
        self.sort_code = Entry(self.main_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                               font=('Helvetica', 12, 'bold'))
        self.sort_code.insert(0, self.sort_code_placeholder_text)  # Placeholder text
        self.sort_code.bind("<FocusIn>", self.on_entry_click)
        self.sort_code.bind("<FocusOut>", self.on_focus_out)
        self.sort_code.place(x=620, y=80, width=300, height=30)

        #
        self.account_number = Entry(self.main_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                                    font=('Helvetica', 12, 'bold'))
        self.account_number.insert(0, self.account_number_placeholder_text)  # Placeholder text
        self.account_number.bind("<FocusIn>", self.on_entry_click)
        self.account_number.bind("<FocusOut>", self.on_focus_out)
        self.account_number.place(x=620, y=140, width=300, height=30)

        #
        self.account_name = Entry(self.main_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                                  font=('Helvetica', 12, 'bold'))
        self.account_name.insert(0, self.account_name_placeholder_text)  # Placeholder text
        self.account_name.bind("<FocusIn>", self.on_entry_click)
        self.account_name.bind("<FocusOut>", self.on_focus_out)
        self.account_name.place(x=620, y=200, width=300, height=30)

        # Check Button
        self.check_btn = Label(self.main_frame, highlightthickness=2, text='Check Details',
                               font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                               bd=2, cursor='hand1')
        self.check_btn.bind("<Button-1>", self.check_account_exists)
        self.check_btn.place(x=715, y=240)

        # Separator
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.place(x=520, y=275, width=500)

        # Fame for the Amount section
        self.amount_frame = Frame(self.main_frame, width=400, height=200, bg='#f0f0f0')

        # Amount Frame Labels
        self.amount_label = Label(self.amount_frame, text="Amount (£): ",
                                  font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.amount_label.place(x=45, y=20)

        #
        self.reference_label = Label(self.amount_frame, text="Reference: ",
                                     font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.reference_label.place(x=45, y=70)

        #
        self.send_date_label = Label(self.amount_frame, text="Schedule Send: ",
                                     font=('Helvetica', 10, 'bold'), fg='black', bg='#f0f0f0')
        self.send_date_label.place(x=45, y=120)

        # Amount Frame Entries
        self.amount = Entry(self.amount_frame, highlightthickness=3, relief=FLAT, bg='#f0f0f0',
                            fg='black', font=('Helvetica', 12, 'bold'))
        self.amount.place(x=150, y=20, width=200, height=20)

        #
        self.reference = Entry(self.amount_frame, highlightthickness=3, relief=FLAT, bg='#f0f0f0',
                               fg='black', font=('Helvetica', 12, 'bold'))
        self.reference.place(x=150, y=70, width=200, height=20)

        #
        self.send_date = Entry(self.amount_frame, highlightthickness=3, relief=FLAT, bg='#f0f0f0',
                               fg='grey', font=('Helvetica', 12, 'bold'))
        self.send_date.insert(0, self.send_date_placeholder_text)
        self.send_date.bind("<FocusIn>", self.on_entry_click)
        self.send_date.bind("<FocusOut>", self.on_focus_out)
        self.send_date.place(x=150, y=120, width=200, height=20)

        # Send Button
        self.send_btn = Label(self.amount_frame, highlightthickness=2, text='Send',
                              font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                              bd=2, cursor='hand1')
        self.send_btn.bind("<Button-1>", self.transfer_money)
        self.send_btn.place(x=165, y=170)

    def send_receipient_notification_email(self, firstname, email_address, amount_received, sender_full_name):
        # Email setup
        sender_email = "jay.aby.codes@gmail.com"
        sender_password = "jwcabxkjbjjoqbck"
        subject = "Ashling Bank- Credit Notification"

        # Create the username content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_address
        message['Subject'] = subject

        # Email body
        body = f"""
        Dear {firstname} ,

        You have received {amount_received} from {sender_full_name}.
        
        Please check your account for more details.

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
            print(f"Error sending email: {e}")


    def send_sender_notification_email(self, firstname, email_address, amount_sent, receiver_name):
        # Email setup
        sender_email = "jay.aby.codes@gmail.com"
        sender_password = "jwcabxkjbjjoqbck"
        subject = "Ashling Bank- Transfer Notification"

        # Create the username content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_address
        message['Subject'] = subject

        # Email body
        body = f"""
        Dear {firstname} ,

        Your transfer of £{amount_sent} to {receiver_name} was successful.

        If you do not authorize this transaction, please contact us immediately.

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

    def transfer_money(self, event):
        self.show_amount_frame()

        entered_amount = self.amount.get().strip()
        entered_reference = self.reference.get().strip()
        entered_date = self.date.get().strip() if hasattr(self, 'date') else None

        print(f"Entered Amount: {entered_amount}")
        print(f"Entered Reference: {entered_reference}")
        print(f"Entered Date: {entered_date}")

        # Initialize scheduled date
        scheduled_date = None

        #
        db = sqlite3.connect(DB_PATH)

        try:
            cursor = db.cursor()

            # Retrieve sender details
            sender_id = self.logged_in_user['customer_id']
            retrieve_sender_account_query = '''SELECT u.firstname, u.lastname, u.email, a.balance, a.pin 
                                               FROM UserAccountDetails a 
                                               JOIN userPersonalDetails u 
                                               ON a.customer_id = u.customer_id
                                               WHERE a.customer_id = ?'''
            cursor.execute(retrieve_sender_account_query, (sender_id,))
            sender_data = cursor.fetchone()

            if not sender_data:
                messagebox.showerror("AshlingBank- Error", "Sender account not found!")
                return

            sender_firstname, sender_lastname, sender_email, sender_balance, sender_pin = sender_data
            sender_full_name = f"{sender_firstname} {sender_lastname}"
            messagebox.showinfo(f"AshlingBank- Info", f"Current Account Balance: {sender_balance}")

            # Retrieve recipient details
            if not hasattr(self, 'recipient_details') or not self.recipient_details:
                messagebox.showerror("AshlingBank- Error",
                                     "Recipient account not available. Please verify recipients account.")
                return

            # Access recipient details
            recipient_sort_code = self.recipient_details['sort_code']
            recipient_account_number = self.recipient_details['account_number']
            recipient_email = self.recipient_details['retrieved_email']
            recipient_name = self.recipient_details['entered_name']
            recipient_customer_id = self.recipient_details['customer_id']

            # Validate amount entered
            if not entered_amount or float(entered_amount) <= 0:
                messagebox.showerror("AshlingBank- Error", "Please enter a valid amount.")
                return

            if float(entered_amount) > sender_balance:
                messagebox.showerror("AshlingBank- Error", "Insufficient funds.")
                return

            # Parse and validate scheduled date
            if entered_date:
                try:
                    scheduled_date = datetime.strptime(entered_date, '%d-%m-%Y')
                    if scheduled_date < datetime.now():
                        messagebox.showerror("AshlingBank- Error", "Scheduled date cannot be in the past")
                        return
                except ValueError:
                    messagebox.showerror("AshlingBank- Error", "Invalid Date Format. Use DD-MM-YYYY")
                    return

            # Pin Validation - Needs to be Masked
            user_pin_dialog = customtkinter.CTkInputDialog(text="Enter your 4 digits Pin.", title="AshlingBank- Transfer")
            entered_pin = user_pin_dialog.get_input()

            if not entered_pin:
                messagebox.showerror("AshlingBank- Error", "Transaction Cancelled.")
                return

            if str(entered_pin) != str(sender_pin):
                messagebox.showerror("AshlingBank- Error", "Incorrect Pin.")
                return

            # Deduct from sender account - Update UserAccountDetails DB
            deduct_query = "UPDATE userAccountDetails SET balance = balance - ? WHERE customer_id = ? AND balance >= ?"
            cursor.execute(deduct_query, (float(entered_amount), sender_id, float(entered_amount)))

            # Add to recipient account if no scheduled date
            if not scheduled_date:
                add_query = "UPDATE userAccountDetails SET balance = balance + ? WHERE customer_id = ?"
                cursor.execute(add_query, (float(entered_amount), recipient_customer_id))

            # Update Transaction details
            transaction_query = '''
                        INSERT INTO transactionDetails (sender_account_id, recipient_account_id, amount_out, transaction_date, transaction_status, transaction_type, transaction_reference, recipient_name)
                        VALUES (?,?,?,?,?,?,?,?)           
                        '''
            cursor.execute(transaction_query, (sender_id, recipient_customer_id, float(entered_amount),
                                               scheduled_date if scheduled_date else datetime.now(),
                                               "Scheduled" if scheduled_date else "Success", "transfer",
                                               entered_reference, recipient_name))

            db.commit()
            messagebox.showinfo("AshlingBank- Success",
                                f"{entered_amount} to {recipient_name} {'Scheduled' if scheduled_date else 'Sent'} successfully.")
            print(f"Recipient Name: {recipient_name}, Recipient Email: {recipient_email}")
            try:
                self.send_sender_notification_email(sender_firstname, sender_email, entered_amount, recipient_name)
                self.send_receipient_notification_email(recipient_name, recipient_email, entered_amount, sender_full_name)
                self.reset_text_fields()
            except Exception as e:
                print(f"Error sending email: {e}")

        except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("AshlingBank- Error", "Unable to process transaction")
        finally:
            db.close()

    def check_account_exists(self, event):
        entered_sort_code = self.sort_code.get().strip()
        entered_account_number = self.account_number.get().strip()
        entered_name = self.account_name.get().strip()

        print(f"Entered sort-code : {entered_sort_code}")
        print(f"Entered account number: {entered_account_number}")
        print(f"Entered account name: {entered_name}")

        # Connect to the database
        db = sqlite3.connect(DB_PATH)

        if entered_sort_code == self.sort_code_placeholder_text or entered_account_number == self.account_number_placeholder_text or entered_name == self.account_name_placeholder_text:
            messagebox.showerror("AshlingBank- Error", "Please fill in all fields.")
            return
        else:
            try:
                cursor = db.cursor()

                # Check if account exists
                query = '''
                SELECT u.firstname, u.lastname, u.email, a.customer_id
                FROM userAccountDetails a
                JOIN userPersonalDetails u ON a.customer_id = u.customer_id
                WHERE a.sort_code = ? AND a.account_number = ? 
                '''
                print(
                    f"(Executing Query: {query} with parameters sort-code: {entered_sort_code} account number: {entered_account_number}")
                cursor.execute(query, (entered_sort_code, entered_account_number))
                record = cursor.fetchone()

                print(f"Query Result {record}")  # Debugging the result

                if record:
                    retrieved_firstname, retrieved_lastname, retrieved_email, retrieved_customer_id = record
                    full_name = f"{retrieved_firstname} {retrieved_lastname}".strip()

                    if self.logged_in_user['customer_id'] == retrieved_customer_id:
                            messagebox.showerror("AshlingBank- Error", "You cannot transfer money to your own account!")
                            return
                    else:
                        if entered_name.lower() == full_name.lower():
                            # Store recipient details
                            self.recipient_details = {
                                "sort_code": entered_sort_code,
                                "account_number": entered_account_number,
                                "entered_name": entered_name,
                                "retrieved_email": retrieved_email,
                                "customer_id": retrieved_customer_id,
                            }
                            # Check if sender's account is the same as recipient's account
                            if self.logged_in_user['customer_id'] == retrieved_customer_id:
                                messagebox.showerror("AshlingBank- Error", "You cannot transfer money to your own account!")
                                return
                            else:
                                messagebox.showinfo("AshlingBank- Confirmation", "Account Found")
                                self.show_amount_frame()
                        else:
                            response = messagebox.askyesno("AshlingBank- Confirmation",
                                                        "The account details doesn't match. Do you want to Proceed?")
                            #
                            if response:
                                # Store recipient details
                                self.recipient_details = {
                                    "sort_code": entered_sort_code,
                                    "account_number": entered_account_number,
                                    "entered_name": entered_name,
                                    "retrieved_email": retrieved_email,
                                    "customer_id": retrieved_customer_id,
                                }
                                self.show_amount_frame()
                            else:
                                return
                else:
                    messagebox.showerror("AshlingBank- Error", "Account not found")

            except Exception as e:
                print(f"Error {e}")
                messagebox.showerror("AshlingBank- Error", "Unable to process query.")
            finally:
                db.close()

    def reset_text_fields(self):
        self.hide_amount_frame()

        fields = [
            (self.sort_code, self.sort_code_placeholder_text),
            (self.account_number, self.account_number_placeholder_text),
            (self.account_name, self.account_name_placeholder_text),
            (self.amount, ""),
            (self.reference, ""),
            (self.send_date, self.send_date_placeholder_text)
        ]

        for field, placeholder in fields:
            field.delete(0, "end")
            field.insert(0, placeholder)
            field.config(fg='grey')

    def show_amount_frame(self):
        self.amount_frame.place(x=773, y=385, anchor=CENTER)

    def hide_amount_frame(self):
        self.amount_frame.place_forget()

    def on_entry_click(self, event):
        # Remove placeholder text when entry is clicked
        widget = event.widget
        placeholder_text = None

        if widget == self.sort_code:
            placeholder_text = self.sort_code_placeholder_text
        elif widget == self.account_number:
            placeholder_text = self.account_number_placeholder_text
        elif widget == self.account_name:
            placeholder_text = self.account_name_placeholder_text
        elif widget == self.send_date:
            placeholder_text = self.send_date_placeholder_text

        if placeholder_text and widget.get() == placeholder_text:
            widget.delete(0, "end")
            widget.config(fg='black')

    def on_focus_out(self, event):
        # Add placeholder when focus is lost and field is empty
        widget = event.widget
        placeholder_text = None

        if widget == self.sort_code:
            placeholder_text = self.sort_code_placeholder_text
        elif widget == self.account_number:
            placeholder_text = self.account_number_placeholder_text
        elif widget == self.account_name:
            placeholder_text = self.account_name_placeholder_text
        elif widget == self.send_date:
            placeholder_text = self.send_date_placeholder_text

        if placeholder_text and widget.get().strip() == '':
            widget.insert(0, placeholder_text)
            widget.config(fg='grey')

