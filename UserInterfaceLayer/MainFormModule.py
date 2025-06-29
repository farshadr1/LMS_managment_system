import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from Model.userModule import UserModel
from PIL import Image, ImageTk


class MainForm:
    def __init__(self, userparam: UserModel):
        self.root = tk.Tk()
        self.userparam = userparam
        self.setup_main_window()
        self.create_widgets()

    def setup_main_window(self):
        self.root.title('MainForm...')
        self.root.geometry('360x290')
        self.root.resizable(False, False)
        x = int(self.root.winfo_screenwidth() / 2 - 360 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 290 / 2)
        self.root.geometry(f'+{x}+{y}')
        self.root.iconbitmap('./images/home.ico')
        self.style = ttk.Style()
        # self.style.configure('TButton', font=('Arial', 10))
        self.style.map('TButton',
                       background=[('active', '#4CAF50'), ('!active', 'SystemButtonFace')],
                       foreground=[('active', 'black'), ('!active', 'black')]
                       )

    def create_widgets(self):
        img_lego = Image.open('./images/LMS_lego.png')
        img_lego = img_lego.resize((40, 40), Image.LANCZOS)
        self.img_lego = ImageTk.PhotoImage(img_lego)
        self.lbl_lego = tk.Label(self.root, image=self.img_lego)
        self.lbl_lego.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='nsew')

        welcome_text = f'Welcome, {self.userparam.FirstName} {self.userparam.LastName}!'
        self.lbl_welcome = tk.Label(self.root, text=welcome_text, font=("Arial", 10, "bold"))
        self.lbl_welcome.grid(row=0, column=1, padx=10, pady=(10, 0), sticky='ns')

        self.frame = tk.Frame(self.root, relief='groove', bd=2, padx=5, pady=10)
        self.frame.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        # Create a label to display images
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=1, column=1, padx=0, pady=0, sticky='nsew')

        # Load and resize images
        self.images = {
            # 'Persons': self.load_and_resize_image('./images/persons.png'),
            'Students': self.load_and_resize_image('./images/students.png'),
            'Teachers': self.load_and_resize_image('./images/teachers.png'),
            'Employees': self.load_and_resize_image('./images/employees.png'),
            'Courses': self.load_and_resize_image('./images/courses.png')
        }

        self.buttons = [
            # ('Persons', self.open_persons_form),
            ('Students', self.open_students_form),
            ('Teachers', self.open_teachers_form),
            ('Employees', self.open_employees_form),
            ('Courses', self.open_courses_form),
            ('Logout', self.logout)
        ]

        for idx, (text, command) in enumerate(self.buttons):
            if text == 'Logout':
                btn = ttk.Button(self.root, text=text, command=command, width=15, style='TButton')
                btn.grid(row=2, column=0, padx=5, pady=5, sticky='n')
            else:
                btn = ttk.Button(self.frame, text=text, command=command, width=15, style='TButton')
                btn.grid(row=idx, column=0, padx=5, pady=5, sticky='n')
                btn.bind("<Enter>", lambda e, t=text: self.on_hover(t))
                btn.bind("<Leave>", self.on_leave)

    def load_and_resize_image(self, path, size=(180, 180)):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def on_hover(self, button_text):
        self.image_label.config(image=self.images[button_text])

    def on_leave(self, event):
        self.image_label.config(image='')

    def open_persons_form(self):
        from UserInterfaceLayer.PersonFormModule import PersonForm
        self.root.destroy()
        PersonForm(self.userparam)

    def open_students_form(self):
        from UserInterfaceLayer.StudentFormModule import StudentForm
        self.root.destroy()
        StudentForm(self.userparam)

    def open_teachers_form(self):
        pass

    def open_employees_form(self):
        pass

    def open_courses_form(self):
        pass

    def logout(self):
        self.root.destroy()
