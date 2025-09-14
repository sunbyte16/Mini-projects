# 🎓 Student Record Manager

<div align="center">

![Python](https://img.shields.io/badge/Python-3.6+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)

**A comprehensive Python-based CRUD system for managing student records with support for both CSV and JSON file formats.**

[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-black?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20My%20Work-purple?style=for-the-badge&logo=netlify)](https://lively-dodol-cc397c.netlify.app)

</div>

## ✨ Features

<div align="center">

### 🚀 **Core Functionality**

| Feature | Description | Status |
|---------|-------------|--------|
| 🔧 **Complete CRUD Operations** | Add, view, search, update, and delete student records | ✅ |
| 📁 **Dual Format Support** | Works with both CSV and JSON file formats | ✅ |
| 🛡️ **Data Validation** | Ensures data integrity with proper validation | ✅ |
| ⚠️ **Error Handling** | Comprehensive error handling for edge cases | ✅ |
| 🎯 **Menu-Driven Interface** | User-friendly command-line interface | ✅ |

</div>

### 📋 **Student Record Fields**

<div align="center">

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| 🆔 **Student ID** | String | Unique, Required | Unique identifier for each student |
| 👤 **Name** | String | Required | Full name of the student |
| 🎂 **Age** | Integer | 1-150 | Student's age with range validation |
| 📚 **Grade/Class** | String | Required | Student's current grade or class |
| 📧 **Email** | String | Format Validated | Student's email address |

</div>

### 🚀 **Advanced Features**

<div align="center">

| Feature | Icon | Description |
|---------|------|-------------|
| 🔍 **Search Functionality** | | Search students by ID or name (partial matching) |
| 📊 **Sorting Options** | | Sort records by name, age, or grade |
| 📤 **Export/Import** | | Convert between CSV and JSON formats |
| 🔄 **Format Switching** | | Change file format without data loss |
| 🚫 **Duplicate Prevention** | | Prevents duplicate student IDs |
| 💾 **Data Persistence** | | Automatic saving after each operation |

</div>

## 🚀 Quick Start

<div align="center">

### 📋 **Prerequisites**

![Python](https://img.shields.io/badge/Python-3.6+-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-None-green?style=flat-square)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

</div>

### 🔧 **Installation**

<div align="center">

| Step | Action | Command |
|------|--------|---------|
| 1️⃣ | **Clone Repository** | `git clone https://github.com/sunbyte16/student-record-manager.git` |
| 2️⃣ | **Navigate to Directory** | `cd student-record-manager` |
| 3️⃣ | **Verify Python Version** | `python --version` |
| 4️⃣ | **Ready to Run!** | No additional setup required |

</div>

### 🎯 **Running the Program**

<div align="center">

```bash
# Main Application
python student_manager.py

# Simple Interactive Version
python simple_student_manager.py

# Quick Demo
python quick_demo.py

# Generate Demo Data
python demo_data.py
```

</div>

## 📋 Usage Guide

<div align="center">

### 🎯 **Main Menu Options**

| Option | Icon | Action | Description |
|--------|------|--------|-------------|
| **1** | ➕ | Add New Student | Create a new student record |
| **2** | 👥 | View All Students | Display all student records in a formatted table |
| **3** | 🔍 | Search Student | Find students by ID or name |
| **4** | ✏️ | Update Student | Modify existing student information |
| **5** | 🗑️ | Delete Student | Remove a student record (with confirmation) |
| **6** | 📊 | Sort Students | Sort records by name, age, or grade |
| **7** | 📤 | Export Data | Export data to different format |
| **8** | 📥 | Import Data | Import data from external files |
| **9** | 🔄 | Change File Format | Switch between CSV and JSON formats |
| **0** | 🚪 | Exit | Close the program |

</div>

### 📁 **File Formats**

<div align="center">

#### 📄 **JSON Format (Default)**
```json
[
  {
    "student_id": "S001",
    "name": "Sunil Sharma",
    "age": 20,
    "grade": "A",
    "email": "sunil.sharma@email.com"
  }
]
```

#### 📊 **CSV Format**
```csv
student_id,name,age,grade,email
S001,Sunil Sharma,20,A,sunil.sharma@email.com
```

</div>

## 🔧 Technical Details

<div align="center">

### 🏗️ **Class Structure**

| Component | Description | Features |
|-----------|-------------|----------|
| 🎯 **StudentRecordManager** | Main class handling all CRUD operations | Modular design, Type hints |
| 🛡️ **Data Validation** | Comprehensive input validation | Real-time validation, Error messages |
| 📁 **File Operations** | CSV/JSON file handling | Auto-load, Auto-save, Format detection |
| ⚠️ **Error Handling** | Exception management | Graceful failures, User feedback |

</div>

### 🔍 **Data Validation Rules**

<div align="center">

| Field | Rule | Validation Type |
|-------|------|----------------|
| 🆔 **Student ID** | Unique, Non-empty | Duplicate check, Required |
| 👤 **Name** | Non-empty string | Required field |
| 🎂 **Age** | Integer 1-150 | Range validation |
| 📚 **Grade** | Non-empty string | Required field |
| 📧 **Email** | Valid email format | Format validation |

</div>

### 💾 **File Operations**

<div align="center">

| Operation | Description | Status |
|-----------|-------------|--------|
| 🔄 **Automatic Loading** | Data loads on startup | ✅ |
| 💾 **Auto-Save** | Changes saved immediately | ✅ |
| 🔍 **Format Detection** | Based on file extension | ✅ |
| 🛡️ **Backup Safety** | Original data preserved | ✅ |

</div>

## 📁 Project Structure

<div align="center">

```
Student Record Manager/
├── 📄 student_manager.py          # Main application file
├── 🎯 simple_student_manager.py   # Interactive version
├── 🚀 quick_demo.py              # Demo version
├── 🎲 demo_data.py               # Data generator
├── 📋 requirements.txt           # Project dependencies
├── 📖 README.md                  # This documentation
├── 💾 students.json              # JSON data file (created on first run)
└── 📊 students.csv               # CSV data file (if using CSV format)
```

</div>

## 🛠️ Customization

### Adding New Fields
To add new fields to student records:
1. Update the `add_student` method parameters
2. Modify the fieldnames in CSV operations
3. Update the display methods
4. Add validation as needed

### Changing File Location
Modify the `data_file` parameter in the `StudentRecordManager` constructor:
```python
manager = StudentRecordManager("custom_path/students.json", "json")
```

## 🐛 Troubleshooting

### Common Issues
1. **File Permission Errors**: Ensure write permissions in the directory
2. **Invalid Data Format**: Check file format matches expected structure
3. **Duplicate IDs**: System prevents duplicate student IDs automatically
4. **Empty Fields**: All fields except optional ones are validated

### Error Messages
- `❌ Error: Student ID 'X' already exists!` - Duplicate ID prevention
- `❌ Error: Invalid email format!` - Email validation failed
- `❌ Student with ID 'X' not found!` - Record not found for update/delete
- `❌ Error loading data: X` - File loading issue

## 📊 Example Usage

### Adding a Student
```
Enter your choice (0-9): 1
Student ID: S001
Full Name: Sunil Sharma
Age: 20
Grade/Class: A
Email: john.doe@email.com
✓ Student 'Sunil Sharma' added successfully!
```

### Searching Students
```
Enter your choice (0-9): 3
Enter Student ID or Name to search: Sunil
🔍 Search Results for 'Sunil' (1 found):
================================================================================
ID         Name                 Age  Grade     Email                    
--------------------------------------------------------------------------------
S001       Sunil Sharma          20   A         sunil.sharma@email.com       
================================================================================
```

## 🤝 Contributing

This is a standalone project, but suggestions for improvements are welcome:
- Additional data validation
- GUI interface
- Database integration
- Advanced search features
- Report generation

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

Potential features for future versions:
- GUI interface using tkinter or PyQt
- Database integration (SQLite, PostgreSQL)
- Advanced reporting and analytics
- Bulk import/export operations
- Student photo management
- Grade calculation and tracking
- Attendance management integration

---

<div align="center">

## 💖 **Created By 𝕊𝕦𝕟𝕚𝕝 𝕊𝕙𝕒𝕣𝕞𝕒**

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20My%20Work-purple?style=for-the-badge&logo=netlify&logoColor=white)](https://lively-dodol-cc397c.netlify.app)

</div>

---

### 🌟 **Connect with Me**

<div align="center">

| Platform | Link | Description |
|----------|------|-------------|
| 🐙 **GitHub** | [@sunbyte16](https://github.com/sunbyte16) | View my repositories and contributions |
| 💼 **LinkedIn** | [Sunil Kumar](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/) | Connect with me professionally |
| 🌐 **Portfolio** | [My Portfolio](https://lively-dodol-cc397c.netlify.app) | Check out my projects and skills |

</div>

---

<div align="center">

### 🎯 **Project Stats**

![GitHub stars](https://img.shields.io/github/stars/sunbyte16/student-record-manager?style=social)
![GitHub forks](https://img.shields.io/github/forks/sunbyte16/student-record-manager?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/sunbyte16/student-record-manager?style=social)

</div>

---

<div align="center">

**Happy Student Management! 🎓**

*If you found this project helpful, please give it a ⭐ star!*

</div>

</div>
