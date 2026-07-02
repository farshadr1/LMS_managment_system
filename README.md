# LMS Management System

A desktop-based Learning Management System (LMS) designed for educational institutions, developed in Python using the Tkinter GUI library. The system provides an intuitive and organized interface for performing CRUD operations on key entities including students, teachers, employees, and courses.

## 📋 Features

- **User Authentication**: Secure login system with admin and regular user roles
- **Student Management**: Add, update, delete, and view student information
  - National code, name, date of birth, contact information
  - Education level tracking
  - Student photo management
  
- **Teacher Management**: Manage teacher profiles and information
- **Employee Management**: Handle institutional employee records
- **Course Management**: Create and manage course information
- **Search & Filter**: Search through records by various criteria
- **User-Friendly Interface**: Clean and intuitive Tkinter-based GUI
- **Database Integration**: SQL Server backend for persistent data storage

## 🏗️ Architecture

The project follows a **three-layer architecture pattern**:

### 1. **User Interface Layer** (`UserInterfaceLayer/`)
- `LoginFormModule.py` - User authentication interface
- `MainFormModule.py` - Main dashboard with navigation
- `StudentFormModule.py` - Student management interface
- `BaseFormModule.py` - Base class for all management forms

### 2. **Business Logic Layer** (`Model/`)
- `userModule.py` - User model with authentication properties

### 3. **Data Access Layer** (`DataAccessLayer/`)
- `PersonRepository.py` - Database operations for person-related entities
- `db_access_settings.py` - Database connection configuration

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework
- **pyodbc** - SQL Server database connector
- **Pillow (PIL)** - Image processing
- **tkcalendar** - Date picker widget

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- SQL Server (local or remote)
- Required Python packages

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/farshadr1/LMS_managment_system.git
   cd LMS_managment_system
   ```

2. **Install dependencies**
   ```bash
   pip install pyodbc pillow tkcalendar
   ```

3. **Configure Database Connection**
   - Edit `DataAccessLayer/db_access_settings.py`
   - Update the connection string with your SQL Server credentials:
   ```python
   connection_string_sql_server = 'Driver={ODBC Driver 17 for SQL Server};Server=YOUR_SERVER;Database=YOUR_DATABASE;UID=YOUR_USER;PWD=YOUR_PASSWORD'
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## 📝 Usage

### Login
- Default credentials:
  - Username: `admin`
  - Password: `admin`

### Main Features
1. **Students**: Manage student records including personal information and academic details
2. **Teachers**: Maintain teacher profiles and information
3. **Employees**: Handle institutional staff records
4. **Courses**: Create and organize course information

## 📁 Project Structure

```
LMS_managment_system/
├── UserInterfaceLayer/
│   ├── LoginFormModule.py
│   ├── MainFormModule.py
│   ├── StudentFormModule.py
│   ├── BaseFormModule.py
│   └── ...
├── Model/
│   └── userModule.py
├── DataAccessLayer/
│   ├── PersonRepository.py
│   └── db_access_settings.py
├── images/
│   ├── students.png
│   ├── teachers.png
│   └── ...
└── README.md
```

## 🔐 Security Considerations

- Store database credentials securely (consider using environment variables)
- Implement proper input validation
- Use parameterized queries to prevent SQL injection (already implemented in PersonRepository)
- Consider implementing role-based access control enhancements

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

**Farshad Ravaee**

## 📄 License

This project is provided as-is for educational purposes.

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

---

*Last Updated: 2026*
