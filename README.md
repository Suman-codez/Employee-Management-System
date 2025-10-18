# 🧠 Employee Management System (Python + MySQL + Tkinter GUI)

A complete Employee Management System built using Python and MySQL, featuring both a manually developed console version and an AI-assisted GUI version. This project demonstrates how traditional programming logic can be transformed into a modern graphical interface using AI tools like ChatGPT, without requiring deep knowledge of Tkinter.

---

## 🚀 Project Overview

This project was developed in two phases:

### 🧩 Phase 1 — Console-based System (`mainp.py`)
The first version of this project was created entirely by hand as a menu-driven, console-based system. It allowed user registration and login, employee record management, salary updates, performance tracking, and record deletion. This version demonstrates manual control over logic, loops, conditionals, and MySQL queries using the `mysql-connector-python` library.

### 🤖 Phase 2 — AI-Assisted GUI (`employee_gui_final.py`)
The second version of the system was created with the help of AI tools such as ChatGPT. The entire console logic was used as a base, and the AI transformed it into a complete GUI built with Tkinter. This shows how AI can be leveraged to enhance developer productivity, generate graphical interfaces, and modernize existing software without needing to hand-code every UI element.

This approach represents **AI-assisted software engineering** — combining a developer’s logic, database design, and coding fundamentals with artificial intelligence to produce a fully functional desktop application.

---

## 🧰 Features

- ✅ User Registration & Login  
- ✅ Add, View, List, Update, and Delete Employees  
- ✅ Manage Employee Salary (absolute or percentage update)  
- ✅ Track Employee Performance and Experience  
- ✅ Integrated MySQL database using `mysql-connector-python`  
- ✅ Graphical interface built with Tkinter (AI-generated from CLI logic)

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| Programming Language | Python 3.x |
| GUI Framework | Tkinter |
| Database | MySQL (via XAMPP) |
| Libraries | `mysql-connector-python`, `tkinter`, `ttk` |

---

## ⚙️ Setup Instructions

### 1️⃣ Database Setup
1. Open **phpMyAdmin** or **MySQL CLI**.  
2. Create a new database named `employees`.  
3. Run the SQL commands provided in `database.sql` (included in this repository).  
   Example command:
   ```sql
   SOURCE database.sql;
   ```
   This will create three tables:
   - `log` — for user registration and login  
   - `office` — for employee information  
   - `em_performance` — for performance and experience tracking

---

### 2️⃣ Install Dependencies
Make sure Python 3.x is installed, then install the required connector:
```bash
pip install mysql-connector-python
```

---

### 3️⃣ Start MySQL Server
Start MySQL from **XAMPP Control Panel** or your preferred environment.

---

### 4️⃣ Run the Applications
**Run the AI-assisted GUI version:**
```bash
python employee_gui_final.py
```

**Run the original console version:**
```bash
python mainp.py
```

---

## 🗄️ Database Schema (Reference)

### Table: `log`
| Column | Type | Description |
|---------|------|-------------|
| username | VARCHAR(50) | Primary key (login username) |
| password | VARCHAR(100) | User password |

### Table: `office`
| Column | Type | Description |
|---------|------|-------------|
| em_no | VARCHAR(20) | Primary key (manual Employee ID entered by user) |
| em_name | VARCHAR(100) | Employee name |
| em_dept | VARCHAR(100) | Department |
| em_salary | FLOAT | Salary amount |
| em_age | INT | Age of the employee |

### Table: `em_performance`
| Column | Type | Description |
|---------|------|-------------|
| id | INT AUTO_INCREMENT | Primary key |
| em_no | VARCHAR(20) | Foreign key (references office.em_no) |
| em_name | VARCHAR(100) | Employee name |
| em_dept | VARCHAR(100) | Department |
| performance | VARCHAR(10) | Performance rating (A+, A, B, etc.) |
| experience | VARCHAR(100) | Experience details |

---

## 🏗️ Folder Structure

```
employee-management-system/
│
├── mainp.py                  ← Original console-based version (manual logic)
├── employee_gui_final.py     ← Tkinter GUI version (AI-assisted)
├── database.sql              ← MySQL database schema
└── README.md                 ← Project documentation
```

---

## 🧠 What This Project Demonstrates

This project highlights how AI tools can significantly accelerate development and enable developers to produce professional applications without having to write every line of GUI code themselves.

### Key Skills Demonstrated:
- Logical program design and flow control in Python  
- MySQL database integration and query handling  
- Transformation of console logic into a GUI application  
- Efficient use of AI-assisted programming for rapid UI generation  
- Understanding of CRUD operations (Create, Read, Update, Delete)

By maintaining both versions — the manual CLI (`mainp.py`) and the AI-assisted GUI (`employee_gui_final.py`) — this project shows both programming capability and modern AI fluency.

---

## 💡 Why AI-Assisted Development Matters

Modern developers are not just coders — they are problem solvers.  
This project demonstrates how using AI as a development partner can:
- Reduce repetitive UI coding  
- Speed up prototyping  
- Allow focus on core logic and database structure  
- Bridge the gap between conceptual design and production-ready software  

---

## 👨‍💻 Author

**Suman-codez**  
💼 AI-Assisted Python Developer  
🌐 [GitHub Profile](https://github.com/Suman-codez)

---

## 🏁 Acknowledgment

The GUI version of this project (`employee_gui_final.py`) was developed with the assistance of ChatGPT (OpenAI), based on the logic and database design from the original `mainp.py`.  
This demonstrates how developers can effectively collaborate with AI tools to build complete, real-world applications faster, more efficiently, and with professional results.
