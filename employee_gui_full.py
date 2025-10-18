import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector as sql
import sys

# ---------------- Configuration ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "employees"
}

# ---------------- Database helpers ----------------
def get_connection():
    try:
        conn = sql.connect(**DB_CONFIG)
        return conn
    except sql.Error as e:
        messagebox.showerror("DB Connection Error", f"Could not connect to database:\n{e}")
        sys.exit(1)

def ensure_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS log (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(100)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS office (
            em_no VARCHAR(20) PRIMARY KEY,
            em_name VARCHAR(100),
            em_dept VARCHAR(100),
            em_salary FLOAT,
            em_age INT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS em_performance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            em_no VARCHAR(20),
            em_name VARCHAR(100),
            em_dept VARCHAR(100),
            performance VARCHAR(10),
            experience VARCHAR(100),
            FOREIGN KEY (em_no) REFERENCES office(em_no) ON DELETE CASCADE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

ensure_tables()

# ---------------- Auth ----------------
class AuthWindow:
    def __init__(self, root):
        self.root = root
        root.title("Employee Management System - Login")
        root.geometry("420x260")
        root.resizable(False, False)

        frm = ttk.Frame(root, padding=12)
        frm.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frm, text="EMPLOYEE MANAGEMENT SYSTEM", font=("Helvetica", 14, "bold")).pack(pady=(0,10))
        ttk.Label(frm, text="Choose an action:").pack(anchor=tk.W, pady=(0,4))
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, padx=8)
        ttk.Button(btn_frame, text="1. Register User", command=self.register).grid(row=0, column=0, padx=6, pady=6)
        ttk.Button(btn_frame, text="2. Login", command=self.login).grid(row=0, column=1, padx=6, pady=6)

    def register(self):
        RegisterDialog(self.root)

    def login(self):
        LoginDialog(self.root, self.open_main_menu)

    def open_main_menu(self, username):
        self.root.destroy()
        new_root = tk.Tk()
        MainMenuWindow(new_root, username)
        new_root.mainloop()

class RegisterDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Register New User")
        ttk.Label(master, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=6)
        self.e_user = ttk.Entry(master)
        self.e_user.grid(row=0, column=1)
        ttk.Label(master, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.e_pass = ttk.Entry(master, show="*")
        self.e_pass.grid(row=1, column=1)
        return self.e_user

    def validate(self):
        if not self.e_user.get().strip() or not self.e_pass.get().strip():
            messagebox.showwarning("Input Error", "Both fields required")
            return False
        return True

    def apply(self):
        u, p = self.e_user.get().strip(), self.e_pass.get().strip()
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO log (username,password) VALUES (%s,%s)", (u,p))
            conn.commit()
            messagebox.showinfo("Success","User registered.")
        except sql.IntegrityError:
            messagebox.showerror("Error","Username already exists.")
        finally:
            cur.close()
            conn.close()

class LoginDialog(simpledialog.Dialog):
    def __init__(self, parent, callback):
        self.callback = callback
        super().__init__(parent, title="Login")

    def body(self, master):
        ttk.Label(master, text="Username:").grid(row=0,column=0,pady=6)
        self.e_user = ttk.Entry(master); self.e_user.grid(row=0,column=1)
        ttk.Label(master, text="Password:").grid(row=1,column=0,pady=6)
        self.e_pass = ttk.Entry(master, show="*"); self.e_pass.grid(row=1,column=1)
        return self.e_user

    def validate(self):
        u, p = self.e_user.get().strip(), self.e_pass.get().strip()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM log WHERE username=%s AND password=%s",(u,p))
        ok = cur.fetchone()
        cur.close(); conn.close()
        if ok: 
            self.username = u
            return True
        messagebox.showerror("Failed","Invalid username or password.")
        return False

    def apply(self):
        self.callback(self.username)

# ---------------- Main Menu ----------------
class MainMenuWindow:
    def __init__(self, root, username):
        self.root = root
        root.title(f"Employee Management System - User: {username}")
        root.geometry("950x600")
        ttk.Label(root, text="EMPLOYEE MANAGEMENT SYSTEM", font=("Helvetica",16,"bold")).pack(pady=10)

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=5)
        buttons = [
            ("Register New Employee", self.register_employee),
            ("View Employee Details", self.view_employee_details),
            ("Count Employees", self.count_employees),
            ("List Employees", self.list_employees),
            ("View Salary", self.view_salary),
            ("Update Salary", self.update_salary_menu),
            ("Add Performance Record", self.add_performance),
            ("View All Performances", self.view_performances),
            ("Delete Employee", self.delete_employee),
            ("Exit", self.exit_program)

        ]
        for i, (text, cmd) in enumerate(buttons):
            ttk.Button(btn_frame, text=text, width=30, command=cmd).grid(row=i//2, column=i%2, padx=6, pady=6)

        ttk.Separator(root).pack(fill=tk.X, pady=10)

        # Treeview with separate columns
        cols = ("ID", "Name", "Department", "Salary", "Age", "Performance", "Experience")
        self.tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # ---------- Functions ----------
    def register_employee(self):
        d = RegisterEmployeeDialog(self.root)
        if d.result:
            self.list_employees()

    def list_employees(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.em_no, o.em_name, o.em_dept, o.em_salary, o.em_age,
                p.performance, p.experience
            FROM office o
            LEFT JOIN em_performance p ON o.em_no = p.em_no
            ORDER BY o.em_no
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Clear and insert rows
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", tk.END, values=r)



    def view_employee_details(self):
        em_no = simpledialog.askstring("Employee Details", "Enter employee ID:")
        if not em_no:
            return

        conn = get_connection()
        cur = conn.cursor()

        # Join employee + performance (if available)
        cur.execute("""
            SELECT o.em_no, o.em_name, o.em_dept, o.em_salary, o.em_age,
                p.performance, p.experience
            FROM office o
            LEFT JOIN em_performance p ON o.em_no = p.em_no
            WHERE o.em_no = %s
        """, (em_no,))

        rows = cur.fetchall()
        self.tree.delete(*self.tree.get_children())

        if not rows:
            messagebox.showinfo("Not Found", "Employee not found.")
        else:
            # Show only one row (or multiple if different perf records)
            for r in rows:
                self.tree.insert("", tk.END, values=r)

        cur.close()
        conn.close()


    def count_employees(self):
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM office")
        cnt = cur.fetchone()[0]
        cur.close(); conn.close()
        messagebox.showinfo("Total Employees", f"Total employees: {cnt}")

    def view_salary(self):
        em_no = simpledialog.askstring("View Salary","Enter employee ID:")
        if not em_no: return
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT em_name, em_salary FROM office WHERE em_no=%s",(em_no,))
        row = cur.fetchone()
        cur.close(); conn.close()
        if row:
            messagebox.showinfo("Salary", f"{row[0]}'s Salary: {row[1]}")
        else:
            messagebox.showinfo("Not Found","Employee not found.")

    def update_salary_menu(self):
        choice = messagebox.askquestion("Update Salary","Update by percent? (Yes=Percent / No=Absolute)")
        if choice=="yes": self.update_salary_percent()
        else: self.update_salary_absolute()

    def update_salary_percent(self):
        em_no = simpledialog.askstring("Employee ID","Enter employee ID:")
        if not em_no: return
        percent = simpledialog.askfloat("Percent","Enter percent (+/-):")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("UPDATE office SET em_salary = em_salary + em_salary * %s/100 WHERE em_no=%s",(percent, em_no))
        conn.commit(); cur.close(); conn.close()
        messagebox.showinfo("Updated","Salary updated successfully.")
        self.list_employees()

    def update_salary_absolute(self):
        em_no = simpledialog.askstring("Employee ID","Enter employee ID:")
        if not em_no: return
        new_sal = simpledialog.askfloat("Salary","Enter new salary:")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("UPDATE office SET em_salary=%s WHERE em_no=%s",(new_sal, em_no))
        conn.commit(); cur.close(); conn.close()
        messagebox.showinfo("Updated","Salary updated successfully.")
        self.list_employees()

    def add_performance(self):
        d = AddPerformanceDialog(self.root)
        if d.result: self.view_performances()

    def view_performances(self):
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT em_no, em_name, em_dept, performance, experience FROM em_performance")
        rows = cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", tk.END, values=(r[0], r[1], r[2], "", "", r[3], r[4]))
        cur.close(); conn.close()

    def delete_employee(self):
        em_no = simpledialog.askstring("Delete Employee","Enter employee ID:")
        if not em_no: return
        conn = get_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM em_performance WHERE em_no=%s",(em_no,))
        cur.execute("DELETE FROM office WHERE em_no=%s",(em_no,))
        conn.commit(); cur.close(); conn.close()
        messagebox.showinfo("Deleted","Employee deleted.")
        self.list_employees()
    
    def exit_program(self):
        """Confirm and close the application."""
        answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if answer:
            self.root.destroy()


# ---------------- Dialogs ----------------
class RegisterEmployeeDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Register Employee")
        fields = ["ID", "Name", "Department", "Salary", "Age"]
        self.entries = {}
        for i, f in enumerate(fields):
            ttk.Label(master, text=f + ":").grid(row=i, column=0, sticky=tk.W, pady=4)
            e = ttk.Entry(master)
            e.grid(row=i, column=1, pady=4)
            self.entries[f] = e
        return self.entries["ID"]

    def validate(self):
        try:
            if self.entries["Salary"].get().strip():
                float(self.entries["Salary"].get())
        except ValueError:
            messagebox.showwarning("Error", "Salary must be numeric.")
            return False
        if not self.entries["ID"].get().strip():
            messagebox.showwarning("Error", "Employee ID is required.")
            return False
        return True

    def apply(self):
        vals = [self.entries[f].get().strip() for f in ["ID", "Name", "Department", "Salary", "Age"]]
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO office (em_no, em_name, em_dept, em_salary, em_age) VALUES (%s,%s,%s,%s,%s)",
                tuple(vals)
            )
            conn.commit()
            messagebox.showinfo("Added", "Employee added successfully.")
            self.result = True
        except sql.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists.")
            self.result = False
        finally:
            cur.close()
            conn.close()


class AddPerformanceDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Add Performance")
        labels = ["Employee ID","Name","Department","Performance","Experience"]
        self.entries={}
        for i,l in enumerate(labels):
            ttk.Label(master, text=l+":").grid(row=i,column=0,sticky=tk.W,pady=4)
            e=ttk.Entry(master); e.grid(row=i,column=1,pady=4)
            self.entries[l]=e
        return self.entries["Employee ID"]

    def apply(self):
        data = [self.entries[l].get().strip() for l in ["Employee ID","Name","Department","Performance","Experience"]]
        conn = get_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO em_performance (em_no,em_name,em_dept,performance,experience) VALUES (%s,%s,%s,%s,%s)",tuple(data))
        conn.commit(); cur.close(); conn.close()
        messagebox.showinfo("Added","Performance record added.")
        self.result=True

# ---------------- Run ----------------
if __name__=="__main__":
    root=tk.Tk()
    AuthWindow(root)
    root.mainloop()
