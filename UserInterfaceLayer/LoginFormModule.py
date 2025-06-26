import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from Model.userModule import UserModel
from UserInterfaceLayer.MainFormModule import MainForm
from DataAccessLayer.db_access_settings import connection_string_sql_server
import pyodbc


class LoginForm:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_widgets()

    def setup_main_window(self):
        self.root.title('Login...')
        self.root.geometry('275x180')
        self.root.resizable(False, False)
        x = int(self.root.winfo_screenwidth() / 2 - 270 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 180 / 2)
        self.root.geometry(f'+{x}+{y}')
        self.root.iconbitmap(self, './images/login.ico')
        self.style = ttk.Style()
        # self.style.configure('TButton', font=('Arial', 10))
        self.style.map('TButton',
                       background=[('active', '#4CAF50'), ('!active', 'SystemButtonFace')],
                       foreground=[('active', 'black'), ('!active', 'black')]
                       )

    def create_widgets(self):
        self.welcome_text = "Welcome to Learning Management System(LMS)! writen by Farshad Ravaee. "
        self.lbl_welcome = tk.Label(self.root, text="", font=("Courier", 9), bg="black", fg="lime",
                                width=35, anchor='w')  # Reduced width to 40 characters
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        self.lbl_welcome.grid_propagate(False)

        self.lbl_user_name = tk.Label(self.root, text='UserName: ')
        self.lbl_user_name.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.txt_user_name = tk.StringVar()
        self.txt_user_name.set('admin')
        self.ent_user_name = ttk.Entry(self.root, textvariable=self.txt_user_name, width=25)
        self.ent_user_name.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        self.lbl_password = tk.Label(self.root, text='Password: ')
        self.lbl_password.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.txt_password = tk.StringVar()
        self.txt_password.set('admin')
        self.ent_password = ttk.Entry(self.root, textvariable=self.txt_password, width=20, show='*')
        self.ent_password.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.show_password = False
        self.btn_toggle = ttk.Button(self.root, text="Show", width=6, command=self.toggle_password, takefocus=0,
                                     style='TButton')
        self.btn_toggle.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        self.btn_login = ttk.Button(self.root, text='Login ...', width=10, command=self.login_function_sql_server,
                                    style='TButton')
        self.btn_login.grid(row=3, column=1, padx=5, pady=20, sticky='e')

        self.ent_user_name.focus()
        self.rotation_index = 0
        self.rotate_welcome_text()  # Start animation

    def rotate_welcome_text(self):
        display_width = 35  # This should match the width set for the label
        rotated_text = self.welcome_text[self.rotation_index:] + self.welcome_text[:self.rotation_index]
        truncated_text = rotated_text[:display_width]  # Only display the first 40 characters
        self.lbl_welcome.config(text=truncated_text)
        self.rotation_index = (self.rotation_index + 1) % len(self.welcome_text)
        self.root.after(150, self.rotate_welcome_text)

    def toggle_password(self):
        if self.show_password:
            self.ent_password.config(show='*')
            self.btn_toggle.config(text='Show')
        else:
            self.ent_password.config(show='')
            self.btn_toggle.config(text='Hide')
        self.show_password = not self.show_password

    def run(self):
        self.root.mainloop()

    def login_function_sql_server(self):
        user_name = self.txt_user_name.get().lower()
        password = self.txt_password.get()

        command_text_sql_server = 'EXEC [dbo].[login_check] ?, ?'
        try:
            with pyodbc.connect(connection_string_sql_server) as connection_sql_server:
                cursor = connection_sql_server.cursor()
                cursor.execute(command_text_sql_server, (user_name, password))
                rows = cursor.fetchall()
            if len(rows) > 0:
                user_object = UserModel(user_name=rows[0][0],
                                        password=rows[0][1],
                                        firstname=rows[0][2],
                                        lastname=rows[0][3],
                                        isadmin=rows[0][4]
                                        )
                # msg.showinfo('login', f'Welcome {user_object.FirstName} {user_object.LastName}')
                self.root.destroy()
                MainForm(user_object)
            else:
                msg.showerror('Error!!!', 'Username or Password is incorrect!!! ')
        except:
            msg.showerror('Error!!!', 'SQL Server does not exist or access denied!!! ')


