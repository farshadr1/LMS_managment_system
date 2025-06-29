import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from Model.userModule import UserModel
from UserInterfaceLayer.MainFormModule import MainForm
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import pyodbc
from tkinter import filedialog
from DataAccessLayer.db_access_settings import connection_string_sql_server
from DataAccessLayer.PersonRepository import PersonRepository

# ------------------------------------------------------------------------------
class PersonForm:
    def __init__(self, userparam: UserModel):
        self.root = tk.Tk()
        # self.entryList = []
        self.treeview_columns = ['FirstName', 'LastName', 'Gender', 'NationalCode', 'BirthDate',
                                 'Mobile', 'Education', 'Address', 'PersonId', 'Photo']
        self.userparam = userparam
        self.setup_main_window()
        self.create_widgets()
        self.person_repo = PersonRepository()

    def setup_main_window(self):
        self.root.title("Persons Information")
        self.root.geometry("640x470")
        self.root.resizable(False, False)
        x = int(self.root.winfo_screenwidth() / 2 - 640 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 470 / 2)
        self.root.geometry(f'+{x}+{y}')
        self.root.iconbitmap('./images/persons.ico')
        self.style = ttk.Style()
        # self.style.configure('TButton', font=('Arial', 10))
        self.style.map('TButton',
                       background=[('active', '#4CAF50'), ('!active', 'SystemButtonFace')],
                       foreground=[('active', 'black'), ('!active', 'black')]
                       )
        self.connection_string_sql_server = connection_string_sql_server
        self.PersonID = ''

    def create_widgets(self):
        # Photo Frame:
        self.photo_frame = tk.Frame(self.root, relief='groove', bd=2)
        self.photo_frame.grid(row=0, column=0, padx=5, pady=10, sticky='nsew')
        self.create_photoFrame_widgets()
        # Form Frame:
        self.entry_vars = dict()
        self.form_frame = tk.Frame(self.root, relief='groove')
        self.form_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.create_form_widgets()
        # crud Buttons Frame:
        self.btns_frame = tk.Frame(self.root, relief='groove', bd=2)
        self.btns_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky='nsew')
        self.create_crud_buttons()

        # Table Frame:
        self.table_frame = tk.Frame(self.root, relief='groove', width=600, height=200)
        self.table_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.table_frame.grid_propagate(False)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.create_treeview_widgets()

    def create_photoFrame_widgets(self):
        self.default_image_path = './images/profile_pic.png'
        self.current_image_path = self.default_image_path
        image_profile = Image.open(self.default_image_path)

        image_profile = image_profile.resize((96, 96), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image_profile)
        self.lbl_photo = tk.Label(self.photo_frame, image=self.photo, bg='white')
        self.lbl_photo.grid(row=0, column=0, padx=10, pady=10)

        self.btn_change_photo = ttk.Button(self.photo_frame, text='Change Photo', command=self.open_photo_file_dialog,
                                           style='TButton')
        self.btn_change_photo.grid(row=1, column=0, padx=5, pady=5, sticky='s')
        self.btn_remove_photo = ttk.Button(self.photo_frame, text='Remove Photo', command=self.set_default_image,
                                           style='TButton')
        self.btn_remove_photo.grid(row=2, column=0, padx=5, pady=5, sticky='s')
        self.photo_frame.grid_rowconfigure(0, weight=1)
        self.photo_frame.grid_columnconfigure(0, weight=1)

    def create_form_widgets(self):
        for item in self.entryList:
            var = tk.StringVar()
            lbl = tk.Label(self.form_frame, text=item[0])
            lbl.grid(row=item[1], column=item[2] + 1, padx=5, pady=5, sticky='w')
            if item[0] == 'Gender':
                self.gender_frame = tk.Frame(self.form_frame)
                self.gender_frame.grid(row=item[1], column=item[2] + 2, sticky='w')
                radio_male = ttk.Radiobutton(self.gender_frame, text="Male", variable=var, value="آقا")
                radio_female = ttk.Radiobutton(self.gender_frame, text="Female", variable=var, value="خانم")
                radio_male.grid(row=0, column=0, padx=2, pady=5, sticky='w')
                radio_female.grid(row=0, column=1, padx=2, pady=5, sticky='w')
            elif item[0] == 'BirthDate':
                ent = DateEntry(self.form_frame, textvariable=var, date_pattern='yyyy-mm-dd', width=22)
                ent.grid(row=item[1], column=item[2] + 2, padx=5, pady=5, sticky='w')
            elif item[0] == 'Address':
                ent = ttk.Entry(self.form_frame, textvariable=var, width=25)
                ent.grid(row=item[1], column=item[2] + 2, columnspan=3, padx=5, pady=5, sticky='we')
            elif item[0] == 'Education':
                ent = ttk.Combobox(self.form_frame, textvariable=var, width=22)
                ent['values'] = ('دیپلم', 'فوق دیپلم', 'لیسانس', 'فوق لیسانس', 'دکترا')
                ent['state'] = 'readonly'
                ent.grid(row=item[1], column=item[2] + 2, padx=5, pady=5, sticky='w')
            elif item[0] == 'Courses':
                self.courses_frame = tk.Frame(self.form_frame)
                self.courses_frame.grid(row=item[1], column=item[2] + 2, sticky='w')
                ent = ttk.Combobox(self.courses_frame, textvariable=var, width=15)
                ent['values'] = ()
                ent['state'] = 'readonly'
                ent.grid(row=0, column=0, padx=5, pady=5, sticky='w')
                btn_remove = ttk.Button(self.courses_frame, text='-', width=2, command=self.remove_course)
                btn_remove.grid(row=0, column=1, padx=0, pady=5, sticky='w')
                btn_add = ttk.Button(self.courses_frame, text='+', width=2, command=self.add_course)
                btn_add.grid(row=0, column=2, padx=0, pady=5, sticky='w')
            else:
                ent = ttk.Entry(self.form_frame, textvariable=var, width=25)
                ent.grid(row=item[1], column=item[2] + 2, padx=5, pady=5, sticky='w')
            self.entry_vars[item[0]] = var
            # copy-paste-cut ability:
            if isinstance(ent, ttk.Entry):  # Only bind to Entry widgets
                ent.bind('&lt;Control-c&gt;', self.copy)
                ent.bind('&lt;Control-v&gt;', self.paste)
                ent.bind('&lt;Control-x&gt;', self.cut)

        self.btn_clear = ttk.Button(self.form_frame, text='Clear', width=10, command=self.clear_form)
        self.btn_clear.grid(row=6, column=4, padx=5, pady=5, sticky='w')
        self.btn_backToMainForm = ttk.Button(self.form_frame, text='Back', width=10, command=self.backToMainForm)
        self.btn_backToMainForm.grid(row=6, column=4, padx=5, pady=5, sticky='e')

    def create_crud_buttons(self):
        buttons = [('Select All', 0, 0), ('Search', 0, 1), ('Insert', 0, 2), ('Update', 0, 3), ('Delete', 0, 4)]
        for button in buttons:
            btn = ttk.Button(self.btns_frame, text=button[0], width=15,
                             command=lambda t=button[0]: self.crud_btn_clicked(t), style='TButton')
            btn.grid(row=button[1], column=button[2], padx=11, pady=5, sticky='w')

    def create_treeview_widgets(self):
        self.treeview = ttk.Treeview(self.table_frame, columns=self.treeview_columns, show="headings")
        for col in self.treeview_columns:
            self.treeview.heading(col, text=col)
            if (col == 'PersonId'):  # Hide the 'PersonId' column
                self.treeview.column(col, width=0, stretch=tk.NO)
            else:
                self.treeview.column(col, width=85, anchor='center')

        scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.treeview.yview)
        scrollbar_x = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.treeview.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)

    def on_treeview_select(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            values = self.treeview.item(selected_item[0])['values']
            self.PersonID = values[-2]  # PersonId
            for i, key in enumerate(self.treeview_columns):
                if key in self.entry_vars:
                    self.entry_vars[key].set(values[i])
    
            # Update photo if available
            if values[-1] != 'None':
                command_text_sql_server = '''
                    SELECT [Photo] FROM Person
                    WHERE ID=?;    
                '''
                try:
                    with pyodbc.connect(self.connection_string_sql_server) as connection_sql_server:
                        cursor = connection_sql_server.cursor()
                        cursor.execute(command_text_sql_server, self.PersonID)
                        photo_data = cursor.fetchone()[0]
    
                    if photo_data:
                        # Convert the binary data to an image
                        from io import BytesIO
                        image = Image.open(BytesIO(photo_data))
                        image = image.resize((96, 96), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.lbl_photo.configure(image=photo)
                        self.lbl_photo.image = photo
                    else:
                        self.set_default_image()
                except Exception as e:
                    print(f"Error loading image: {e}")
                    self.set_default_image()
            else:
                self.set_default_image()
    
    def set_default_image(self):
        image = Image.open(self.default_image_path)
        image = image.resize((96, 96), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.lbl_photo.configure(image=photo)
        self.lbl_photo.image = photo

    def copy(self, event):
        self.root.clipboard_clear()
        if event.widget.selection_get():
            self.root.clipboard_append(event.widget.selection_get())

    def paste(self, event):
        try:
            event.widget.insert("insert", self.root.clipboard_get())
        except tk.TclError:
            pass  # nothing to paste

    def cut(self, event):
        self.copy(event)
        event.widget.delete("sel.first", "sel.last")

    def read_form(self):
        result = dict()
        for key, value in self.entry_vars.items():
            if key == 'Education':
                if value.get() == 'دیپلم':
                    result[key] = 1
                elif value.get() == 'فوق دیپلم':
                    result[key] = 2
                elif value.get() == 'لیسانس':
                    result[key] = 3
                elif value.get() == 'فوق لیسانس':
                    result[key] = 4
                elif value.get() == 'دکترا':
                    result[key] = 5
                else:
                    result[key] = None
            else:
                result[key] = value.get()
        return result

    def read_picture(self):
        if self.current_image_path != self.default_image_path:
            with Image.open(self.current_image_path) as image:
                resized_image = image.resize((96, 96), Image.LANCZOS)
                # Save the resized image to a bytes buffer
                from io import BytesIO
                image_buffer = BytesIO()
                resized_image.save(image_buffer, format='PNG')
                result = image_buffer.getvalue()
        else:
            result = None
        return result

    def backToMainForm(self):
        self.root.destroy()
        MainForm(self.userparam)

    def clear_form(self):
        for key, value in self.entry_vars.items():
            value.set("")

    def open_photo_file_dialog(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            try:
                # Load and resize the selected image
                image_profile = Image.open(file_path)
                image_profile = image_profile.resize((96, 96), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(image_profile)
                self.lbl_photo.configure(image=self.photo)
                self.current_image_path = file_path
            except Exception as e:
                print(f"Error loading selected image: {e}")

    def crud_btn_clicked(self, t: str):
        if t == 'Select All':
            self.treeview.delete(*self.treeview.get_children())
            rows = self.person_repo.select_all()
            for row in rows:
                isPhoto = (True,) if row[-1] else (None,)
                self.treeview.insert("", "end", values=list(row[:-1]+isPhoto))

        elif t == 'Search':
            vals = self.read_form()
            self.treeview.delete(*self.treeview.get_children())
            values = (
                    vals['FirstName'], vals['LastName'], vals['Gender'], vals['NationalCode'], vals['BirthDate'],
                    vals['Mobile'], vals['Education'], vals['Address'], self.PersonID
                )
            rows = self.person_repo.search(values)
            for row in rows:
                self.treeview.insert("", "end", values=list(row))

        elif t == 'Insert':
            vals = self.read_form()
            photo = self.read_picture()
            values = (
                vals['FirstName'], vals['LastName'], vals['BirthDate'], vals['NationalCode'],
                vals['Gender'], vals['Address'], vals['Mobile'], vals['Education'], photo
            )
            try:
                self.person_repo.insert(values)
                msg.showinfo("Success", "Record inserted successfully.")
            except Exception as e:
                msg.showerror("Error", f"An error occurred: {str(e)}")

        elif t == 'Update':
            if self.PersonID != '':
                vals = self.read_form()
                photo = self.read_picture()
                confirm = msg.askyesno("Confirm Update",
                                       f"Are you sure want to Update {vals['FirstName']} {vals['LastName']} record?")
                if confirm:
                    values = (
                        vals['FirstName'], vals['LastName'], vals['BirthDate'], vals['NationalCode'],
                        vals['Gender'], vals['Address'], vals['Mobile'], vals['Education'], photo, self.PersonID
                    )
                    try:
                        self.person_repo.update(values)
                        msg.showinfo("Success", f"Record Updated successfully.")
                    except pyodbc.Error as e:
                        msg.showerror("Error", f"An error occurred: {str(e)}")
                else:
                    pass

        elif t == 'Delete':
            if self.PersonID != '':
                vals = self.read_form()
                confirm = msg.askyesno("Confirm Delete",
                                       f"Are you sure want to delete {vals['FirstName']} {vals['LastName']} record?")
                if confirm:
                    try:
                        self.person_repo.delete(self.PersonID)
                        msg.showinfo("Success", "Record deleted successfully.")
                        self.clear_form()
                        self.crud_btn_clicked('Select All')
                    except pyodbc.Error as e:
                        msg.showerror("Error", f"An error occurred: {str(e)}")
            else:
                msg.showwarning("Not Allowed", "Please select a record to delete.")

    def add_course(self):
        pass

    def remove_course(self):
        pass
