import tkinter as tk
from GUI.main_window import MainWindow
from GUI.User_window import UserWindow


class Guest(MainWindow):
    def __init__(self,master):
        super().__init__(master)


    def login_btn_click(self):
        self.username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if self.db.take_user_password(self.username) != password:
            self.wrong_data.place(relx=0.1, rely=0.57)
        else:
            global main_frame
            main_frame.destroy()
            main_frame = User(root,self.username)
            main_frame.pack(fill="both", expand=True)

            self.login_window.destroy()


class User(UserWindow):
    def __init__(self, master,username):
        super().__init__(master,username)

    def sign_out_click(self,event):
            global main_frame
            main_frame.destroy()
            main_frame = Guest(root)
            main_frame.pack(fill="both", expand=True)



if __name__ == '__main__':
    root = tk.Tk()

    # Define main window frame
    main_frame = Guest(root)
    main_frame.pack(fill="both", expand=True)

    # Set window parameters
    WINDOW_WIDTH = 1250
    WINDOW_HEIGHT = 700

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)


    root.title("Translate+")
    root.iconbitmap("assets/logo.ico")

    root.mainloop()