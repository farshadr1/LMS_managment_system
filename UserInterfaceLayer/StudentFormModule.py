import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from Model.userModule import UserModel
from UserInterfaceLayer.MainFormModule import MainForm
from UserInterfaceLayer.BaseFormModule import BaseForm
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import pyodbc
from tkinter import filedialog
# ---------------------------------------------------------

class StudentForm(BaseForm):
    def __init__(self, userparam: UserModel):
        self.entryList = [('NationalCode', 0, 0), ('FirstName', 1, 0), ('LastName', 2, 0),
                          ('StudentCode', 3, 0), ('Mobile', 4, 0), ('Address', 5, 0),
                          ('Gender', 0, 2),
                          ('Education', 1, 2, ('دیپلم', 'فوق دیپلم', 'لیسانس', 'فوق لیسانس', 'دکترا')),
                          ('BirthDate', 2, 2), ('Job', 3, 2), ('Courses', 4, 2)]
        self.treeview_columns = ['FirstName', 'LastName', 'Gender', 'NationalCode', 'BirthDate',
                                 'Mobile', 'Education', 'Address', 'PersonId', 'Photo']
        super().__init__(userparam)
        self.root.geometry("640x500")
        self.root.title("Student Form")
        self.root.iconbitmap('./images/students.ico')
