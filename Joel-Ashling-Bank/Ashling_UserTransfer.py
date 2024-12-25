from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from tkinter import font
from PIL import ImageTk, Image

class UserTransfer:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1024x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.configure(bg='#ffffff')

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
        self.check_btn.bind("<Button-1>", self.show_amount_frame)
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
        self.send_btn.bind("<Button-1>", self.hide_amount_frame)
        self.send_btn.place(x=165, y=170)



    def show_amount_frame(self, event):
        self.amount_frame.place(x=773, y=385, anchor=CENTER)

    def hide_amount_frame(self, event):
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

if __name__ == "__main__":
    window = Tk()
    UserTransfer(window)
    window.title("Ashling-User Transfer")
    window.mainloop()
