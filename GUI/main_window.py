import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
import smtplib
from email.mime import text, multipart
import pyttsx4
import speech_recognition as sr
import googletrans
import time
import re

from Verifications.Register import register_verification
from DB.db import DB


class MainWindow(ttk.Frame):
    """
    This class represents the main frame of the GUI.
    """
    def __init__(self, master):
        super().__init__(master)

        self.username = ""
        self.abbreviation = ""

        self.db = DB()
        self.db.create_user_data_table()
        self.db.create_table_for_saved_text()

        # Logo
        logo_img = Image.open("assets/logo_translate.png").resize((400, 230))
        self.tk_logo_img = ImageTk.PhotoImage(logo_img)
        ttk.Label(self, image=self.tk_logo_img).place(
            relx=0.36, rely=-0.06, relwidth=0.4, relheight=0.23
        )

        # Login and Register references
        form_font = font.Font(family="Helvetica", size=14, underline=True)
        self.login_lbl = ttk.Label(
            self, text="Log In", foreground="#3881f5", font=form_font
        )
        self.login_lbl.place(relx=0.88, rely=0.02)
        self.register_lbl = ttk.Label(
            self, text="Register", foreground="#3881f5", font=form_font
        )
        self.register_lbl.place(relx=0.93, rely=0.02)

        self.login_lbl.bind("<Button-1>", self.login_click)
        self.login_lbl.bind(
            "<Enter>", lambda event: self.form_lbl_hover(event, self.login_lbl)
        )
        self.login_lbl.bind(
            "<Leave>", lambda event: self.form_lbl_hover_off(event, self.login_lbl)
        )

        self.register_lbl.bind("<Button-1>", self.register_click)
        self.register_lbl.bind(
            "<Enter>", lambda event: self.form_lbl_hover(event, self.register_lbl)
        )
        self.register_lbl.bind(
            "<Leave>", lambda event: self.form_lbl_hover_off(event, self.register_lbl)
        )

        # First Language selection
        self.first_lang = ttk.Combobox(self, state="readonly")
        self.first_lang.place(relx=0.02, rely=0.2, relwidth=0.23, relheight=0.04)
        self.first_lang.set("English")
        self.first_lang.bind("<<ComboboxSelected>>", self.check_left_lang)

        # Second Language selection
        self.second_lang = ttk.Combobox(self, state="readonly")
        self.second_lang.place(relx=0.75, rely=0.2, relwidth=0.23, relheight=0.04)
        self.second_lang.set("Bulgarian")
        self.second_lang.bind("<<ComboboxSelected>>", self.check_right_lang)

        self.insert_languages()

        # User entry frame
        self.entry_frame = tk.Frame(self, background="white")
        self.entry_frame.place(relx=0.02, rely=0.27, relwidth=0.43, relheight=0.4)

        entry_font = font.Font(family="Helvetica", size=14)
        self.entry_text = tk.Text(self.entry_frame, font=entry_font,wrap="word")
        self.entry_text.place(relwidth=1, relheight=0.85)

        self.entry_text.bind("<<Modified>>",self.on_modified_translate)

        mic_img = Image.open("assets/mic.png").resize((45, 25))
        self.mic_img = ImageTk.PhotoImage(mic_img)
        self.mic_lbl = ttk.Label(
            self.entry_frame, image=self.mic_img, background="white"
        )
        self.mic_lbl.place(relx=0.91, rely=0.87, relwidth=0.075, relheight=0.12)
        self.mic_lbl.bind("<Button-1>", self.enter_voice)

        speaker_img = Image.open("assets/speaker.png").resize((38, 27))
        self.speaker_img = ImageTk.PhotoImage(speaker_img)

        self.left_speaker_lbl = ttk.Label(
            self.entry_frame, image=self.speaker_img, background="white"
        )
        self.left_speaker_lbl.place(relx=0.83, rely=0.87, relwidth=0.07, relheight=0.12)
        self.left_speaker_lbl.bind(
            "<Button-1>", lambda event: self.say_text(self.entry_text.get("1.0", "end"))
        )

        # Translated text frame
        self.translated_frame = tk.Frame(self, background="white")
        self.translated_frame.place(relx=0.55, rely=0.27, relwidth=0.43, relheight=0.4)

        translated_text_font = font.Font(family="Helvetica", size=12)
        self.translated_text = tk.Text(self.translated_frame, font=translated_text_font,wrap="word")
        self.translated_text.place(relwidth=1, relheight=0.85)

        self.right_speaker_lbl = ttk.Label(
            self.translated_frame, image=self.speaker_img, background="white"
        )

        # Send feedback label
        self.feedback_font = font.Font(family="Helvetica", size=10, underline=False)
        self.feedback_lbl = ttk.Label(
            self, text="Send feedback", font=self.feedback_font, foreground="grey"
        )
        self.feedback_lbl.place(relx=0.9, rely=0.68)

        self.feedback_lbl.bind("<Button-1>", self.feedback_on_click)
        self.feedback_lbl.bind("<Enter>", self.feedback_lbl_hover)
        self.feedback_lbl.bind("<Leave>", self.feedback_lbl_hover_off)

        # Feedback widgets
        self.user_mail = ttk.Entry(self)
        self.user_feedback = tk.Text(self)
        self.incorrect_email = ttk.Label(self, foreground="red")
        self.feedback_button = ttk.Button(self, text="Send", command=self.send_mail)

    def login_click(self, event):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Login")
        self.login_window.iconbitmap("assets/logo.ico")

        self.login_window.geometry("500x400")

        login_img = Image.open("assets/login.png").resize((300,150))
        self.login_img = ImageTk.PhotoImage(login_img)
        ttk.Label(
            self.login_window,
            image = self.login_img,
        ).place(relx=0.2,rely=-0.05)

        self.login_username_entry = ttk.Entry(self.login_window, foreground="#808080")
        self.login_username_entry.place(
            relx=0.1, rely=0.25, relwidth=0.8, relheight=0.1
        )
        self.login_username_entry.insert(0, "Enter your username")
        self.login_username_entry.bind(
            "<FocusIn>",
            lambda event: self.entry_focus_in(
                event, self.login_username_entry, "Enter your username"
            ),
        )
        self.login_username_entry.bind(
            "<FocusOut>",
            lambda event: self.entry_focus_out(
                event, self.login_username_entry, "Enter your username"
            ),
        )

        self.login_password_entry = ttk.Entry(self.login_window, foreground="#808080")
        self.login_password_entry.place(
            relx=0.1, rely=0.43, relwidth=0.8, relheight=0.1
        )
        self.login_password_entry.insert(0, "Enter your password")
        self.login_password_entry.bind(
            "<FocusIn>",
            lambda event: self.password_entry_focus_in(
                event, self.login_password_entry, "Enter your password"
            ),
        )
        self.login_password_entry.bind(
            "<FocusOut>",
            lambda event: self.password_entry_focus_out(
                event, self.login_password_entry, "Enter your password"
            ),
        )
        self.wrong_data = ttk.Label(
            self.login_window, text="Enter valid username or password", foreground="red"
        )

        ttk.Button(self.login_window, text="Login", command=self.login_btn_click).place(
            relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1
        )

    def login_btn_click(self):
        pass

    def register_click(self, event):
        self.register_window = tk.Toplevel(self)
        self.register_window.title("Register")

        self.register_window.iconbitmap("assets/logo.ico")

        self.register_window.geometry("500x400")

        register_img = Image.open("assets/register.png").resize((300, 150))
        self.register_img = ImageTk.PhotoImage(register_img)
        ttk.Label(
            self.register_window,
            image=self.register_img
        ).place(relx=0.2,rely=-0.05)

        self.username_entry = ttk.Entry(self.register_window, foreground="#808080")
        self.username_entry.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.1)
        self.username_entry.insert(0, "Enter your username")
        self.username_entry.bind(
            "<FocusIn>",
            lambda event: self.entry_focus_in(
                event, self.username_entry, "Enter your username"
            ),
        )
        self.username_entry.bind(
            "<FocusOut>",
            lambda event: self.entry_focus_out(
                event, self.username_entry, "Enter your username"
            ),
        )

        self.wrong_username = ttk.Label(
            self.register_window, text="username already exist", foreground="red"
        )

        self.password_entry = ttk.Entry(self.register_window, foreground="#808080")
        self.password_entry.place(relx=0.1, rely=0.43, relwidth=0.8, relheight=0.1)
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind(
            "<FocusIn>",
            lambda event: self.password_entry_focus_in(
                event, self.password_entry, "Enter your password"
            ),
        )
        self.password_entry.bind(
            "<FocusOut>",
            lambda event: self.password_entry_focus_out(
                event, self.password_entry, "Enter your password"
            ),
        )

        self.wrong_password = ttk.Label(
            self.register_window,
            text="password must be longer than seven chars",
            foreground="red",
        )

        self.email_entry = ttk.Entry(self.register_window, foreground="#808080")
        self.email_entry.place(relx=0.1, rely=0.61, relwidth=0.8, relheight=0.1)
        self.email_entry.insert(0, "Enter your E-mail")
        self.email_entry.bind(
            "<FocusIn>",
            lambda event: self.entry_focus_in(
                event, self.email_entry, "Enter your E-mail"
            ),
        )
        self.email_entry.bind(
            "<FocusOut>",
            lambda event: self.entry_focus_out(
                event, self.email_entry, "Enter your E-mail"
            ),
        )

        self.wrong_email = ttk.Label(
            self.register_window, text="enter a valid E-mail", foreground="red"
        )

        ttk.Button(
            self.register_window, text="Register", command=self.register_btn_click
        ).place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    def register_btn_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        data = register_verification(username, password, email)

        if data == "username":
            self.wrong_username.place(relx=0.1, rely=0.37)

        elif data == "password":
            self.wrong_password.place(relx=0.1, rely=0.55)

        elif data == "email":
            self.wrong_email.place(relx=0.1, rely=0.73)

        else:
            if len(data) == 3:
                self.db.add_new_user(data)
                self.register_window.destroy()

    def form_lbl_hover(self, event, lbl):
        lbl.config(foreground="#053e99")

    def form_lbl_hover_off(self, event, lbl):
        lbl.config(foreground="#3881f5")

    def feedback_lbl_hover(self, event):
        self.feedback_font = font.Font(family="Helvetica", size=10, underline=True)
        self.feedback_lbl.config(foreground="#323333", font=self.feedback_font)

    def feedback_lbl_hover_off(self, event):
        self.feedback_font = font.Font(family="Helvetica", size=10, underline=False)
        self.feedback_lbl.config(foreground="grey", font=self.feedback_font)

    def on_modified_translate(self,event):
        if self.entry_text.edit_modified():
            self.translate()
        self.entry_text.edit_modified(False)

    def translate(self):
        """
        Translates text from the input language to the output language using the Google Translator API.

        Returns:
        None
        """
        text = self.entry_text.get("1.0", "end")

        self.translated_text.delete("1.0","end")

        input_lang = self.first_lang.get().lower()
        output_lang = self.second_lang.get().lower()

        translated_text = GoogleTranslator(
            source=input_lang, target=output_lang
        ).translate(text)

        self.translated_text.insert("1.0", translated_text)

    def insert_languages(self):
        """
        Inserts supported languages into the language selection dropdown menus.

        Returns:
        None
        """
        self.translator = GoogleTranslator()
        self.languages = self.translator.get_supported_languages()
        lang_values = []
        for value in self.languages:
            value = value.capitalize()
            lang_values.append(value)

        self.first_lang.config(values=lang_values)
        self.second_lang.config(values=lang_values)

    def feedback_on_click(self, event):
        lbl_name = self.feedback_lbl.cget("text")

        if lbl_name == "Send feedback":
            self.feedback_lbl.config(text="Send feedback ⮝")

            self.user_mail = ttk.Entry(self, foreground="#808080")
            self.user_mail.place(relx=0.7, rely=0.73, relwidth=0.28, relheight=0.04)
            self.user_mail.insert(0, "Enter your E-mail")
            self.user_mail.bind(
                "<FocusIn>",
                lambda event: self.entry_focus_in(
                    event, self.user_mail, "Enter your E-mail"
                ),
            )
            self.user_mail.bind(
                "<FocusOut>",
                lambda event: self.entry_focus_out(
                    event, self.user_mail, "Enter your E-mail"
                ),
            )

            self.user_feedback = tk.Text(self)
            self.user_feedback.place(relx=0.7, rely=0.78, relwidth=0.28, relheight=0.15)

            self.feedback_button = ttk.Button(self, text="Send", command=self.send_mail)
            self.feedback_button.place(relx=0.82, rely=0.95)
        else:
            self.feedback_lbl.config(text="Send feedback")
            self.user_mail.destroy()
            self.user_feedback.destroy()
            self.feedback_button.destroy()

    def entry_focus_in(self, event, widget, text):
        if widget.get() == text:
            widget.delete(0, "end")
            widget.insert(0, "")
            widget.config(foreground="#000000")

    def entry_focus_out(self, event, widget, text):
        if widget.get() == "":
            widget.insert(0, text)
            widget.config(foreground="#808080")

    def password_entry_focus_in(self, event, widget, text):
        if widget.get() == text:
            widget.delete(0, "end")
            widget.insert(0, "")
            widget.config(foreground="#000000", show="*")

    def password_entry_focus_out(self, event, widget, text):
        if widget.get() == text:
            widget.delete(0, "end")
            widget.insert(0, "")
            widget.config(foreground="#000000", show="")

    def send_mail(self):
        """
        Sends an email with the user's feedback to a designated email address.
        Uses the user's entered email address and feedback message.
        If the email address is invalid, displays an error message.

        Return:
        None
        """
        smtp_server, smtp_port = "smtp.gmail.com", 587

        send_to = "translateplustest@gmail.com"

        send_from = self.user_mail.get()

        username = "translateplustest@gmail.com"
        password = "mpqvtiewqbnrzrvu"

        messege = multipart.MIMEMultipart()
        messege["From"] = send_from
        messege["To"] = send_to
        messege["subject"] = "Translate+ feedback"

        msg = self.user_feedback.get("1.0", "end")
        msg = f"{str(send_from)} \n {msg}"
        messege.attach(text.MIMEText(msg, "plain"))

        if re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", send_from
        ):
            self.user_mail.delete(0, "end")
            self.user_feedback.delete("1.0", "end")
            self.incorrect_email.destroy()

            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(send_from, send_to, messege.as_string())
                smtp.quit()
        else:
            self.incorrect_email = ttk.Label(
                self, text="Enter a valid E-mail", foreground="red"
            )
            self.incorrect_email.place(relx=0.7, rely=0.93)

    def say_text(self, text):
        """
        Uses the pyttsx4 library to speak the provided text out loud.

        Args:
        text (str): The text to be spoken.

        Returns:
        None
        """
        engine = pyttsx4.init()
        engine.say(text)
        engine.runAndWait()

    def check_left_lang(self, event):
        """
        Checks the current value of the 'first_lang' attribute and displays a speaker icon
        if the selected language is English. Clicking the icon will cause the text in the
        'entry_text' field to be spoken aloud.

        Args:
        event: A tkinter event object.

        Returns:
        None
        """
        lang = self.first_lang.get()

        languages = googletrans.LANGUAGES
        language = self.first_lang.get().lower()

        for k, v in languages.items():
            if v == language:
                self.abbreviation = k

        if lang == "English":
            self.left_speaker_lbl = ttk.Label(
                self.entry_frame, image=self.speaker_img, background="white"
            )
            self.left_speaker_lbl.place(
                relx=0.83, rely=0.87, relwidth=0.07, relheight=0.12
            )
            self.left_speaker_lbl.bind(
                "<Button-1>",
                lambda event: self.say_text(self.entry_text.get("1.0", "end")),
            )

        else:
            self.left_speaker_lbl.destroy()

    def check_right_lang(self, event):
        """
        Checks the current value of the 'second_lang' attribute and displays a speaker icon
        if the selected language is English. Clicking the icon will cause the text in the
        'translated_text' field to be spoken aloud.

        Args:
        event: A tkinter event object.

        Returns:
        None
        """
        lang = self.second_lang.get()

        self.translate()

        if lang == "English":
            self.right_speaker_lbl.place(
                relx=0.02, rely=0.87, relwidth=0.07, relheight=0.12
            )
            self.right_speaker_lbl.bind(
                "<Button-1>",
                lambda event: self.say_text(self.translated_text.cget("text")),
            )

    def enter_voice(self, event):
        """
        This function is called when the user clicks the 'Microphone'.
        It uses the speech recognition library to capture audio from the user's microphone and
        translates the speech into text using the Google Translate API. The translated text
        is then displayed in the entry_text widget.

        Args:
        event: A tkinter event object.

        Return:
        None
        """

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            self.entry_text.delete("1.0", "end")
            self.translated_text.delete("1.0", "end")
            self.entry_text.insert(
                "1.0", recognizer.recognize_google(audio, language=self.abbreviation)
            )
        except:
            self.entry_text.delete("1.0", "end")
            self.entry_text.insert("1.0", "Unknown command")
            time.sleep(5)
            self.entry_text.delete("1.0", "end")
