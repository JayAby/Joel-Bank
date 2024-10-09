from email.mime.base import MIMEBase
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os


class UserLogin:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

        # Create a frame for the signup section
        self.login_frame = Frame(self.window, width=1200, height=500, bg='#f0f0f0')
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Text
        self.txt = 'L o g i n'
        signup_font = font.Font(family="Verdana", size=30, weight="bold")
        self.heading = Label(self.login_frame, text=self.txt, font=signup_font, fg='#000000', bg='#f0f0f0')
        self.heading.place(x=46, y=290, width=400, height=60)

        # Logo
        self.side_logo = Image.open('Image/AshlingBankSmall.png')
        photo = ImageTk.PhotoImage(self.side_logo)
        self.side_logo_label = Label(self.login_frame, image=photo, bg='#f0f0f0')
        self.side_logo_label.image = photo
        self.side_logo_label.place(x=90, y=80)

        # Set Window Icon
        window_logo = Image.open('Image/AshlingBank.png')
        window_logo = ImageTk.PhotoImage(window_logo)
        window.iconphoto(False, window_logo)

        # Textboxes with placeholders
        self.email_placeholder_text = 'Email'
        self.password_placeholder_text = 'Password'

        # Email Entry
        self.email = Entry(self.login_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                           font=('Helvetica', 12, 'bold'))
        self.email.insert(0, self.email_placeholder_text)
        self.email.bind("<FocusIn>", self.on_entry_click)
        self.email.bind("<FocusOut>", self.on_focus_out)
        self.email.place(x=620, y=160, width=300, height=30)

        # Password Entry
        self.password = Entry(self.login_frame, highlightthickness=2, relief=FLAT, bg='#f0f0f0', fg='grey',
                              font=('Helvetica', 12, 'bold'), show='')  # Initially show nothing
        self.password.insert(0, self.password_placeholder_text)  # Use the placeholder
        self.password.bind("<FocusIn>", self.on_password_focus)
        self.password.bind("<FocusOut>", self.on_password_focus_out)
        self.password.bind("<Key>", self.on_password_key)  # Bind key event to manage input
        self.password.place(x=620, y=220, width=192, height=30)


        # Buttons/Labels
        # Using Labels because of the border around the button
        self.login_btn = Label(self.login_frame, highlightthickness=2, text='Login',
                               font=('Helvetica', 13, 'bold'), fg='black', bg='white',
                               bd=2, cursor='hand2')
        self.login_btn.bind("<Button-1>", self.login)
        self.login_btn.place(x=705, y=300)

        self.show_password_btn = Label(self.login_frame, highlightthickness=2, text='Show password',
                                       font=('Helvetica', 12, 'bold'), fg='black', bg='white',
                                       bd=2, cursor='dot')
        self.show_password_btn.bind("<Button-1>", self.toggle_password)
        self.show_password_btn.place(x=820, y=220, width=100, height=30)


    # Functions

    def login(self, event):
        # get the current day
        today = datetime.today()
        today_str = today.strftime("%Y-%m-%d")

        entered_email = self.email.get()
        entered_password = self.password.get()

        # Connect the DB
        db = sqlite3.connect('Ashling-UserRecords.db')

        if entered_email == self.email_placeholder_text or entered_password == self.password_placeholder_text:
            messagebox.showerror("AshlingBank- Error", "Invalid Details")
        else:
            try:
                cursor = db.cursor()
                # use parameterized query to avoid SQL injection
                cursor.execute("SELECT firstname, email, password FROM userPersonalDetails WHERE email=? AND password=?", (entered_email, entered_password))
                record = cursor.fetchone()

                if record:
                    firstname = record[0]
                    messagebox.showinfo("AshlingBank- Confirmation", f"Login Successful! Welcome, {firstname}.")
                    self.send_notification_email(firstname,entered_email,today_str)

                else:
                    messagebox.showerror("AshlingBank- Error", "Invalid Login Details")

            except Exception as e:
                print(f'Error: {e}')
                messagebox.showerror("AshlingBank- Error", "Unable to process query")
                db.rollback()
            finally:
                db.close()

    def send_notification_email(self, firstname, email_address, today_str):
        # Email setup
        sender_email = "jay.aby.codes@gmail.com"
        sender_password = "jwcabxkjbjjoqbck"
        subject = "Ashling Bank- Sign-In Notification"

        # Create the username content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email_address
        message['Subject'] = subject

        # Email body
        body = f"""
        Dear {firstname} ,

        You are receiving this username because you have signed in using your account details on this day: {today_str}
        
        If you didn't sign in, please do well to let us know

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

    def on_entry_click(self, event):
        # Remove placeholder text when entry is clicked
        widget = event.widget
        placeholder_text = None

        if widget == self.email:
            placeholder_text = self.email_placeholder_text

        if placeholder_text and widget.get() == placeholder_text:
            widget.delete(0, "end")
            widget.config(fg='black')

    def on_focus_out(self, event):
        # Add placeholder when focus is lost and field is empty
        widget = event.widget
        placeholder_text = None

        if widget == self.email:
            placeholder_text = self.email_placeholder_text

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
    UserLogin(window)
    window.title("Ashling-User Login")
    window.mainloop()
