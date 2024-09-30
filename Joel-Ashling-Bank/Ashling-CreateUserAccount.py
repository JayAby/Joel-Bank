import random
from email.mime.base import MIMEBase
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
import re  # Import regular expression suport
from datetime import datetime
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os
import customtkinter


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

        # Set Window Icon
        window_logo = Image.open('Image/AshlingBank.png')
        window_logo = ImageTk.PhotoImage(window_logo)
        window.iconphoto(False, window_logo)

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

    # Functions

    def toggle_password(self, event):
        if self.password.cget('show') == '•':
            self.password.config(show='')
            self.show_password_btn.config(text='Hide password')
        else:
            self.password.config(show='•')
            self.show_password_btn.config(text='Show password')

    def create_account(self, event):
        firstname = self.firstname.get()
        lastname = self.lastname.get()
        email_address = self.email.get()
        date_of_birth = self.date_of_birth.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()

        # Check for placeholder text, if any return error
        if firstname == self.firstname_placeholder_text or lastname == self.lastname_placeholder_text or email_address == self.email_placeholder_text or date_of_birth == self.date_of_birth_placeholder_text or password == self.password_placeholder_text or confirm_password == self.confirm_password_placeholder_text:
            messagebox.showerror("AshlingBank- Error Message", "Blank Spaces cannot be saved!")
            return

        # Check if passwords match
        if confirm_password != password:
            messagebox.showerror("AshlingBank - Error Message", "Passwords do not match!")
            return

        # Email validation
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z{2,}$]', email_address)
        if valid_email:
            pass
        else:
            messagebox.showerror("AshlingBank- Error Message", "Invalid username format")
            return

        # Validate the date of birth format
        date_register = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(date_register, date_of_birth):
            messagebox.showerror("AshlingBank- Error Message", "Date of Birth Format must be in dd/mm/yyyy")
            return

        try:
            # Convert to a datetime object
            dob = datetime.strptime(date_of_birth, "%d/%m/%Y")

            # Get the current date
            today = datetime.today()

            # Calculate the user's age
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Check if the user is atleast 16 years old
            if age < 16:
                messagebox.showerror("AshlingBank- Error Message", "You must be atleast 16 years to create an account")
                return

            # Check for invalid days based on the month
            day = dob.day
            month = dob.month
            if month == 2:  # February Leap Year Checker
                if day > 29 or (day == 29 and not (dob.year % 4 == 0 and (dob.year % 100 != 0 or dob.year % 400 == 0))):
                    messagebox.showerror("AshlingBank- Error Message",
                                         "Invalid day for February")
                    return
            elif month in [4, 6, 9, 11]:  # Month with 30 days
                if day > 30:
                    messagebox.showerror("AshlingBank- Error Message", "This month only has 30 days")
                    return

            sort_code, account_number = self.generate_account_details()
            username = self.generate_username(firstname,lastname)

            # Format the dates to a string format for the db
            dob_str = dob.strftime("%Y-%m-%d")
            today_str = today.strftime("%Y-%m-%d")

            # Default pin
            default_pin = self.get_user_pin(account_number, sort_code)

            if default_pin is None:
                messagebox.showerror("AshlingBank- Error", "Account creation cancelled due to PIN setup cancellation")
                return

            # If all Validations pass including PIN validation
            # Connect to DB
            db = sqlite3.connect('Ashling-UserRecords.db')
            insert_query1 = (
                "insert into userRecords(firstname, lastname, username, dob, password, sortcode, accountnumber, pin, username, datecreated) values (?,?,?,?,?,?,?,?,?,?);")

            try:
                cursor = db.cursor()
                cursor.execute(insert_query1, (
                    firstname, lastname, email_address, dob_str, password, sort_code, account_number, default_pin, username, today_str))
                db.commit()

                messagebox.showinfo("AshlingBank- Confirmation",
                                    "Details Saved! Your Account Number is: " + account_number + "\nYour sort code is: " + sort_code)



                # Send confirmation mail
                self.send_confirmation_email(firstname, lastname, email_address, username, account_number, sort_code, today_str)
                self.clear_all()

            except Exception as e:
                print(f'Error: {e}')
                messagebox.showerror("AshlingBank- Error", "Data can't be saved")
                db.rollback()
            db.close()

        except ValueError:
            # if date conversion fails, it means the date is invalid
            messagebox.showerror("AshlingBank- Error",
                                 "Invalid date. Please enter a valid date in dd/mm/yyyy format.")

    def generate_username(self, firstname, lastname):
        get_firstname = firstname[:3]
        get_lastname = lastname[:3]

        value_length = 3
        value_string = "0123456789"
        username = get_firstname + get_lastname + "".join(random.sample(value_string, k=value_length))

        return(username)

    def save_pin(self, account_number, user_pin):
        db = sqlite3.connect('Ashling-UserRecords.db')
        update_query = "UPDATE userRecords SET pin = ? WHERE accountnumber = ?"

        try:
            cursor = db.cursor()
            cursor.execute(update_query, (user_pin, account_number))
            db.commit()
            print("PIN updated successfully")
        except Exception as e:
            print(f"Error: {e}")
            db.rollback()
        finally:
            db.close()

    def get_user_pin(self, account_number, sort_code):
        while True:
            # Display the input dialog for the user to enter their PIN
            user_pin_dialog = customtkinter.CTkInputDialog(
                text="Details Saved! Your Account Number is: " + account_number +
                     "\nYour Sort Code is: " + sort_code +
                     "\n\nPlease enter a 4-digit PIN:",
                title="AshlingBank - PIN Setup"
            )

            # Retrieve the user's input
            user_pin = user_pin_dialog.get_input()

            # If the user cancels the PIN setup (user_pin is None)
            if user_pin is None:
                messagebox.showerror("AshlingBank - Error", "PIN setup was canceled.")
                return None  # Return None to indicate the cancellation

            # PIN validation: check if the input is a 4-digit number
            if user_pin.isdigit() and len(user_pin) == 4:
                messagebox.showinfo("AshlingBank - Confirmation", "Your 4-digit PIN has been saved successfully.")
                return user_pin  # Return the valid PIN
            else:
                # If the PIN is invalid, show an error and keep the dialog open
                messagebox.showerror("AshlingBank - Error", "Invalid PIN. Please enter a 4-digit PIN.")
                # Loop continues to show the input dialog again

    def clear_all(self):
        self.firstname.delete(0,"end")
        self.lastname.delete(0,"end")
        self.email.delete(0,"end")
        self.date_of_birth.delete(0,"end")
        self.password.delete(0,"end")
        self.confirm_password.delete(0,"end")

    def send_confirmation_email(self, firstname, lastname, email_address, username, account_number, sort_code, today_str):
        # Email setup
        sender_email = "jay.aby.codes@gmail.com"
        sender_password = "jwcabxkjbjjoqbck"
        subject = "Welcome to Ashling Bank - Your Account Details"

        # Create the username content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_address
        message['Subject'] = subject

        # Email body
        body = f"""
        Dear {firstname} {lastname},
        
        Thank you for creating an account with Ashling Bank.
        Here are your account details:
        
        Username : {username}
        Account Number: {account_number}
        Sort Code: {sort_code}
        Date Created: {today_str}
        
        Please keep these details safe.
        
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

    def generate_account_details(self):
        # Generate the account number
        account_length = 10
        account_string = "0123456789"
        account_number = "".join(random.sample(account_string, k=account_length))

        # Generate the sort code
        part1 = random.randint(10, 99)
        part2 = random.randint(10, 99)
        part3 = random.randint(10, 99)

        # Format as a sort code
        sort_code = f"{part1:02d}-{part2:02d}-{part3:02d}"

        return sort_code, account_number

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
