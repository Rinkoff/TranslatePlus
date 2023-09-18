from GUI.main_window import MainWindow
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class UserWindow(MainWindow):
    def __init__(self, master, username):
        super().__init__(master)

        self.username = username

        self.login_lbl.destroy()
        self.register_lbl.destroy()

        self.username_lbl = ttk.Label(self, text=f"{self.username}⮟", font=14)
        self.username_lbl.pack(side="right",anchor="ne",padx=10)

        self.username_lbl.bind("<Button-1>", self.username_on_click)
        self.username_lbl.bind(
            "<Enter>",
            lambda event: self.label_hover(event, self.username_lbl, 12, "#4d4d4d"),
        )
        self.username_lbl.bind(
            "<Leave>",
            lambda event: self.label_hover_off(event, self.username_lbl, 12, "black"),
        )

        # Save text images
        star_border = Image.open("assets/star_border.png").resize((35, 35))
        star_full = Image.open("assets/star_full.png").resize((35, 35))
        self.star_border = ImageTk.PhotoImage(star_border)
        self.star_full = ImageTk.PhotoImage(star_full)

        # Save labels
        self.entry_save_lbl = ttk.Label(
            self.entry_frame, image=self.star_border, background="white"
        )
        self.entry_save_lbl.place(relx=0.02, rely=0.86, relwidth=0.075, relheight=0.12)
        self.entry_save_lbl.bind(
            "<Button-1>",
            lambda event: self.check_text_for_unsaved(
                event, self.entry_text, self.entry_save_lbl
            ),
        )

        translated_save_lbl = ttk.Label(
            self.translated_frame, image=self.star_border, background="white"
        )
        translated_save_lbl.place(relx=0.91, rely=0.85, relwidth=0.075, relheight=0.12)
        translated_save_lbl.bind(
            "<Button-1>",
            lambda event: self.check_text_for_unsaved(
                event, self.translated_text, translated_save_lbl
            ),
        )

        # List from saved texts
        self.saved = tk.Listbox(self, selectmode="SINGLE")
        self.saved.place(relx=0.02, rely=0.7, relwidth=0.43, relheight=0.26)
        self.show_saved_texts()

        self.scrollbar = ttk.Scrollbar(self.saved, orient=tk.VERTICAL)
        self.scrollbar.pack(side="right", fill="y")
        self.saved.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.saved.yview)

        self.saved.bind("<<ListboxSelect>>", self.insert_saved_text)

        self.entry_text.bind(
            "<<Modified>>",
            lambda event: self.on_modified(event, self.entry_text, self.entry_save_lbl),
        )
        self.translated_text.bind(
            "<<Modified>>",
            lambda event: self.on_modified(
                event, self.translated_text, translated_save_lbl
            ),
        )

        self.sign_out_lbl = ttk.Label(
            self, text="Sign Out", foreground="#4d4d4d", font=("Helvetica", 10)
        )

    def username_on_click(self, event):
        if self.username_lbl.cget("text") == f"{self.username}⮟":
            self.username_lbl.config(text=f"{self.username}⮝")

            self.sign_out_lbl = ttk.Label(
                self, text="Sign Out", foreground="#4d4d4d", font=("Helvetica", 10)
            )
            self.sign_out_lbl.place(relx=0.95, rely=0.05)
            self.sign_out_lbl.bind("<Button-1>", self.sign_out_click)
            self.sign_out_lbl.bind(
                "<Enter>",
                lambda event: self.label_hover(event, self.sign_out_lbl, 10, "black"),
            )
            self.sign_out_lbl.bind(
                "<Leave>",
                lambda event: self.label_hover_off(
                    event, self.sign_out_lbl, 10, "#4d4d4d"
                ),
            )
        else:
            self.username_lbl.config(text=f"{self.username}⮟")
            self.sign_out_lbl.destroy()

    def sign_out_click(self, event):
        pass

    def label_hover(self, event, lbl, font_size, color):
        font = tk.font.Font(family="Helvetica", size=font_size, underline=True)
        lbl.config(foreground=color, font=font)

    def label_hover_off(self, event, lbl, font_size, color):
        font = tk.font.Font(family="Helvetica", size=font_size, underline=False)
        lbl.config(foreground=color, font=font)

    def on_modified(self, event, entry_label, lbl):
        if entry_label.edit_modified():
            self.translate()
            self.check_words(entry_label, lbl)
        entry_label.edit_modified(False)

    def check_words(self, entry_lbl, lbl):
        texts = self.db.select_texts(username=self.username)

        for text in texts:
            text = str(text)
            text = text[2:-5]
            if entry_lbl.get("1.0", "end").strip().lower() == text.strip().lower():
                lbl.config(image=self.star_full)
                break
            else:
                lbl.config(image=self.star_border)

    def show_saved_texts(self):
        texts = self.db.select_texts(username=self.username)

        self.saved.delete(0, "end")
        num = 0
        for text in texts:
            text = str(text)
            text = text[2:-5]
            self.saved.insert(num, text)
            num += 1

    def insert_saved_text(self, event):
        text = event.widget.get(event.widget.curselection())
        self.entry_text.delete("1.0", "end")
        self.translated_text.delete("1.0", "end")
        self.entry_text.insert("1.0", text)

    def check_text_for_unsaved(self, event, entry_lbl, lbl):
        texts = self.db.select_texts(username=self.username)
        text_list = []

        for text in texts:
            text = str(text)
            text = text[2:-5]
            text.strip().lower()
            text_list.append(text)

        if entry_lbl.get("1.0", "end").strip().lower() in text_list:
            self.unsaved_text(entry_lbl, lbl)
        else:
            self.save_text(entry_lbl, lbl)

    def save_text(self, entry_lbl, lbl):
        lbl.config(image=self.star_full)
        self.db.add_text(self.username, entry_lbl.get("1.0", "end"))
        self.show_saved_texts()

    def unsaved_text(self, entry_lbl, lbl):
        lbl.config(image=self.star_border)
        text = entry_lbl.get("1.0", "end")
        self.db.remove_saved_text(self.username, text)
        self.show_saved_texts()
