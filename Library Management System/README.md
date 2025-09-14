# 📚 Library Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Command%20Line-green?style=for-the-badge&logo=terminal&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

*A comprehensive command-line interface (CLI) application for managing books and users in a library. Built with Python and featuring data persistence, late fee tracking, and detailed reporting.*

[![GitHub](https://img.shields.io/badge/GitHub-View%20on%20GitHub-black?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20My%20Site-purple?style=for-the-badge&logo=netlify)](https://lively-dodol-cc397c.netlify.app)

---

**❤️This Crafted By [Sunil Sharma](https://github.com/sunbyte16)**

</div>

## ✨ Features

<div align="center">

| 🏗️ **Core Features** | 📊 **Advanced Features** | 🛡️ **Data & Security** |
|:---:|:---:|:---:|
| Book Management | Reporting & Analytics | Data Persistence |
| User Management | Late Fee Tracking | Input Validation |
| Borrowing System | Search & Filter | Error Handling |

</div>

### 📖 Book Management
- ➕ **Add New Books** - Librarians can add books with title, author, genre, and availability status
- 👁️ **View All Books** - Display all books with their current availability status
- 🔍 **Search Books** - Search by title, author, or genre with fuzzy matching
- 🗑️ **Delete Books** - Remove books from the library (with confirmation)

### 👥 User Management
- 👤 **Register Users** - Create new library member accounts with unique IDs
- 🗑️ **Delete Users** - Remove user accounts (only if no borrowed books)
- ✅ **User Validation** - Prevent deletion of users with active borrowings
- 📋 **User Tracking** - Monitor user borrowing history

### 🔄 Borrowing System
- 📚 **Borrow Books** - Users can borrow available books with due date tracking
- ↩️ **Return Books** - Return borrowed books with automatic late fee calculation
- 📅 **Due Date Tracking** - 14-day borrowing period with automatic tracking
- 💰 **Late Fee System** - ₹10 per day penalty for overdue books

### 📊 Reporting & Analytics
- 📈 **Library Statistics** - Total books, available books, borrowed books, user count
- 🏆 **Borrowing Activity** - Top borrowed books and borrowing frequency analysis
- ⚠️ **Overdue Tracking** - Identify overdue books and calculate total late fees
- 📋 **Real-time Reports** - Generate comprehensive library reports instantly

### 🛡️ Data Management
- 💾 **JSON Persistence** - All data stored in JSON files for reliability and portability
- ⚡ **Auto-save** - Changes saved immediately after each operation
- ✅ **Data Validation** - Comprehensive input validation and error handling
- 🔒 **Backup Safety** - Multiple data files prevent complete data loss

## 🚀 Quick Start

### 📋 Prerequisites
- 🐍 **Python 3.7+** - Download from [python.org](https://python.org)
- 📦 **No External Dependencies** - Uses only Python standard library
- 💻 **Any Operating System** - Windows, macOS, or Linux

### ⚡ Installation & Setup

<div align="center">

| Method | Command | Description |
|:---:|:---:|:---|
| 🚀 **Quick Setup** | `python setup.py` | Initialize with sample data |
| 🎯 **Direct Start** | `python library_management.py` | Start with empty system |
| 🪟 **Windows** | `run_library.bat` | Double-click to run |
| 🧪 **Test** | `python test_library.py` | Verify functionality |

</div>

#### 🔧 Step-by-Step Installation

```bash
# 1️⃣ Clone or download the project
git clone https://github.com/sunbyte16/library-management-system.git
cd library-management-system

# 2️⃣ Initialize with sample data (recommended)
python setup.py

# 3️⃣ Start the application
python library_management.py
```

### 📁 First Run
The system will automatically create the necessary data files:
- 📚 `books.json` - Stores all book records
- 👥 `users.json` - Stores all user records  
- 📋 `borrowed_books.json` - Stores borrowing history and due dates

## 📋 Usage Guide

### 🎛️ Main Menu Options

<div align="center">

| # | Option | Icon | Description |
|:---:|:---|:---:|:---|
| 1️⃣ | Add New Book | 📚 | Add books to the library catalog |
| 2️⃣ | View All Books | 👁️ | See all books with availability status |
| 3️⃣ | Search Books | 🔍 | Find books by title, author, or genre |
| 4️⃣ | Register User | 👤 | Create new library member accounts |
| 5️⃣ | Borrow Book | 📖 | Check out books to users |
| 6️⃣ | Return Book | ↩️ | Return books and calculate any late fees |
| 7️⃣ | Delete Book | 🗑️ | Remove books from the library |
| 8️⃣ | Delete User | 👥 | Remove user accounts |
| 9️⃣ | View Borrowed Books | 📋 | See all currently borrowed books |
| 🔟 | Generate Report | 📊 | View library statistics and analytics |
| 1️⃣1️⃣ | Exit Program | 🚪 | Save data and exit |

</div>

### 🔄 Sample Workflow

#### 🏗️ **Setup Library**
```bash
1️⃣ Add some books using option 1
4️⃣ Register users using option 4
```

#### 📅 **Daily Operations**
```bash
5️⃣ Borrow books using option 5
6️⃣ Return books using option 6
3️⃣ Search for books using option 3
```

#### 📊 **Management Tasks**
```bash
🔟 View reports using option 10
9️⃣ Check borrowed books using option 9
1️⃣2️⃣7️⃣ Manage inventory using options 1, 2, 7
```

## 📁 File Structure

```
📚 Library Management System/
├── 🐍 library_management.py    # Main application file
├── ⚙️ setup.py                 # Setup script with sample data
├── 🧪 test_library.py          # Test script for verification
├── 🪟 run_library.bat          # Windows batch file
├── 📋 requirements.txt         # Python dependencies
├── 📖 README.md                # This documentation
├── 📚 books.json               # Book data (auto-created)
├── 👥 users.json               # User data (auto-created)
└── 📋 borrowed_books.json      # Borrowing records (auto-created)
```

## 🔧 Technical Details

### 📊 Data Models

#### 📖 **Book Record**
```json
{
  "book_id": "1",
  "title": "Python Programming",
  "author": "John Doe", 
  "genre": "Programming",
  "availability": true
}
```

#### 👤 **User Record**
```json
{
  "user_id": "1",
  "name": "Jane Smith",
  "borrowed_books": ["1", "3"]
}
```

#### 📋 **Borrowing Record**
```json
{
  "book_id": "1",
  "user_id": "1",
  "borrow_date": "2024-01-15T10:30:00",
  "due_date": "2024-01-29T10:30:00",
  "returned": false
}
```

### ⚡ Key Features Implementation

<div align="center">

| 🏗️ **Architecture** | 🛡️ **Quality** | 🎯 **User Experience** |
|:---:|:---:|:---:|
| Modular Design | Error Handling | Clear Menus |
| Type Hints | Input Validation | Status Messages |
| Data Persistence | Exception Handling | Progress Indicators |

</div>

## 🎯 Advanced Features

### 💰 Late Fee System
- ⚡ **Automatic Calculation** - Based on due dates and current time
- 💸 **₹10 per Day Penalty** - For overdue books
- 🔄 **Real-time Calculation** - Instant fee calculation on return

### 🔍 Search Functionality
- 🔤 **Case-insensitive Search** - Across multiple fields
- 🎯 **Partial Matching** - Flexible searching capabilities
- 📊 **Results Display** - With availability status and details

### 📊 Reporting System
- ⚡ **Real-time Statistics** - Instant generation of library metrics
- 🏆 **Top Borrowed Books** - Analysis of popular books
- ⚠️ **Overdue Tracking** - Identify and manage overdue books
- 💰 **Financial Summary** - Late fees and revenue tracking

### 🛡️ Data Safety
- 💾 **Immediate Save** - After each operation
- 📁 **Separate Files** - For different data types
- 🛠️ **Graceful Error Handling** - For file operations
- ✅ **Data Validation** - Before saving any changes

## 🐛 Troubleshooting

### ⚠️ Common Issues

<div align="center">

| Issue | Solution | Icon |
|:---|:---|:---:|
| **File Permission Errors** | Ensure write permissions in directory | 🔒 |
| **JSON Corruption** | Delete corrupted files to start fresh | 📄 |
| **Input Errors** | Follow prompts and use valid formats | ⌨️ |

</div>

### 🚨 Error Messages
- ❌ **Errors** - Issues that need attention
- ✅ **Success** - Successful operations
- ⚠️ **Warnings** - Important information

## 🔮 Future Enhancements

<div align="center">

| 🎨 **UI/UX** | 🗄️ **Backend** | 🌐 **Web Features** |
|:---:|:---:|:---:|
| GUI Interface | Database Integration | Web Interface |
| Barcode Scanning | Email Notifications | Remote Access |
| Mobile App | Advanced Analytics | Multi-library Support |

</div>

## 📝 License

<div align="center">

![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

This project is open source and available under the **MIT License**.

</div>

## 🤝 Contributing

<div align="center">

[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](https://github.com/sunbyte16)

**Contributions are welcome!** Please feel free to submit:
- 🐛 **Issues** - Bug reports and feature requests
- 🔧 **Pull Requests** - Code improvements and new features
- 📖 **Documentation** - Help improve the docs

</div>

## 📞 Support

<div align="center">

| Platform | Link | Description |
|:---:|:---|:---|
| 🐙 **GitHub** | [Create Issue](https://github.com/sunbyte16) | Bug reports & feature requests |
| 💼 **LinkedIn** | [Connect](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/) | Professional networking |
| 🌐 **Portfolio** | [Visit](https://lively-dodol-cc397c.netlify.app) | View my other projects |

</div>

---

<div align="center">

##  ✨**Thank You for Visiting!** ✨

<div style="background: linear-gradient(45deg,rgb(238, 107, 183),rgb(15, 1, 1)); padding: 20px; border-radius: 10px; margin: 20px 0;">

### 🌟 **Your Support Means Everything!**

Thank you for taking the time to explore this **Library Management System** project. Your interest and support are greatly appreciated! 

If you found this project helpful or interesting, please consider:
- ⭐ **Starring** this repository
- 🍴 **Forking** for your own use
- 🐛 **Reporting** any issues you encounter
- 💡 **Suggesting** new features or improvements

---

### 🤝 **Let's Connect!**

I'd love to connect with fellow developers and hear your feedback!

</div>

## 🎉 **Happy Library Managing!** 📚✨

**Created By [❤️Sunil Sharma❤️](https://github.com/sunbyte16)**

[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-black?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20My%20Site-purple?style=for-the-badge&logo=netlify)](https://lively-dodol-cc397c.netlify.app)

---

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin: 30px 0; color: white; text-align: center;">

## 🚀 **Ready to Get Started?**

<div style="margin: 20px 0;">

### 🎯 **Quick Commands**
```bash
# Clone the repository
git clone https://github.com/sunbyte16/library-management-system.git

# Navigate to project directory
cd library-management-system

# Install and run
python setup.py && python library_management.py
```

</div>

---

<div style="margin: 30px 0;">

### 📈 **Project Stats**
![GitHub stars](https://img.shields.io/github/stars/sunbyte16?style=social)
![GitHub followers](https://img.shields.io/github/followers/sunbyte16?style=social)
![GitHub forks](https://img.shields.io/github/forks/sunbyte16/library-management-system?style=social)

</div>

---

<div style="margin: 30px 0;">

### 🌟 **Final Words**

This **Library Management System** represents my passion for creating practical, user-friendly software solutions. Every line of code was written with care, and every feature was designed with the end-user in mind.

**Thank you for being part of this journey!** 🙏

*Keep coding, keep learning, and keep building amazing things!* 💻✨

</div>

---

<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">

### 📧 **Get in Touch**

**Email:** [sunil.sharma@example.com](mailto:sunil.sharma@example.com)  
**GitHub:** [@sunbyte16](https://github.com/sunbyte16)  
**LinkedIn:** [Sunil Kumar](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)  
**Portfolio:** [lively-dodol-cc397c.netlify.app](https://lively-dodol-cc397c.netlify.app)

</div>

---

<div style="text-align: center; margin: 30px 0; font-size: 18px; font-weight: bold;">

**🎉 Happy Coding! 🎉**

*Made with ❤️ and lots of ☕*

</div>

</div>

</div>
