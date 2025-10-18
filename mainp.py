import time
import datetime as dt
import mysql.connector as sql

print("\t\t\t", time.ctime())

conn = sql.connect(host="localhost", user="root", database="employees")

if conn.is_connected():
    print("===== WELCOME TO START EMPLOYEE MANAGEMENT SYSTEM =====")
    print(dt.datetime.now())

def welcome():
    print("""
    ========================================
            EMPLOYEE MANAGEMENT SYSTEM
    ========================================
    1. Register User
    2. Login
    ========================================
    """)
    n = int(input("Enter your choice: "))
    return n

n = welcome()

if n == 1:
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    name = input("Enter a Username: ")
    print()
    passwd = input("Enter a 4 DIGIT Password: ")
    print()
    v_SQLInsert = "INSERT INTO log VALUES('{}', '{}')".format(name, passwd)
    cur.execute(v_SQLInsert)
    conn.commit()
    print()
    print("USER created successfully")

elif n == 2:
    def login():
        conn = sql.connect(host="localhost", user="root", database="employees")
        cur = conn.cursor()
        user_id = input("Enter USER ID: ")
        pwd = input("Enter the password: ")
        tu = (user_id, pwd)
        cur.execute("SELECT * FROM log")
        mydata = cur.fetchall()
        if tu in mydata:
            print("WELCOME TO EMPLOYEE MANAGEMENT SYSTEM")
            menu()
        else:
            print("Invalid USER ID or PASSWORD")
            login()
    login()


def register():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    v_em_no = input("Enter your employee ID: ")
    v_em_name = input("Enter your name: ")
    v_em_dept = input("Enter department you want to join: ")
    v_em_salary = input("Enter your salary: ")
    v_em_age = int(input("Enter your age: "))
    v_sql_insert = "INSERT INTO office VALUES('{}','{}','{}',{}, {})".format(
        v_em_no, v_em_name, v_em_dept, v_em_salary, v_em_age
    )
    cur.execute(v_sql_insert)
    conn.commit()
    print("Congratulations {} for joining our company".format(v_em_name))
    menu()


def details():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    cur.execute("SELECT * FROM office")
    results = cur.fetchall()
    for x in results:
        print(x)
    conn.commit()
    menu()


def em_count():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT em_name) FROM office")
    count = cur.fetchall()
    for x in count:
        print("Number of employees:", x[0])
    conn.commit()
    menu()


def em_list():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    cur.execute("SELECT em_name, em_dept FROM office ORDER BY em_name ASC")
    list_data = cur.fetchall()
    a = cur.rowcount
    print("Total employees are:", a)
    for x in list_data:
        print(x)
    menu()


def em_salary():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    name = input("Enter the employee ID: ")
    cur.execute("SELECT em_name, em_salary FROM office WHERE em_no='{}'".format(name))
    salary = cur.fetchall()
    for x in salary:
        print(x[1], "is your current salary", x[0])
    conn.commit()
    menu()


def em_performance():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    v_em_no = input("Enter your employee ID: ")
    v_em_name = input("Enter your name: ")
    v_em_dept = input("Enter department you want to join: ")
    v_em_performance = input("Enter your performance (A+, A, B+, B, C+, C): ")
    v_em_work = input("Enter your experience (YEARS): ")
    v_sql_insert = "INSERT INTO em_performance VALUES('{}','{}','{}','{}','{}')".format(
        v_em_no, v_em_name, v_em_dept, v_em_performance, v_em_work
    )
    print(v_sql_insert)
    cur.execute(v_sql_insert)
    conn.commit()
    print("Performance added")
    menu()


def perform():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    cur.execute("SELECT * FROM em_performance")
    mydata = cur.fetchall()
    for i in mydata:
        print(i)
    conn.commit()
    menu()


def em_del():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    v_em_no = input("Enter your employee ID: ")
    cur.execute("DELETE FROM office WHERE em_no='{}'".format(v_em_no))
    conn.commit()
    cur.execute("DELETE FROM em_performance WHERE em_no='{}'".format(v_em_no))
    conn.commit()
    print("Employee record deleted successfully")
    menu()


def update_salary():
    conn = sql.connect(host="localhost", user="root", database="employees")
    cur = conn.cursor()
    name = input("Enter the employee ID: ")
    choice = input("Do you want to increase or decrease salary? (I/D): ")
    if choice.capitalize() == "I":
        s = int(input("How much percent value only: "))
        cur.execute("UPDATE office SET em_salary=em_salary + em_salary*{} /100 WHERE em_no='{}'".format(s, name))
        conn.commit()
        print("Salary updated successfully!")
        menu()
    elif choice.capitalize() == "D":
        s = int(input("How much percent value only: "))
        cur.execute("UPDATE office SET em_salary=em_salary - em_salary*{} /100 WHERE em_no='{}'".format(s, name))
        conn.commit()
        print("Salary updated successfully!")
        menu()
    else:
        print("Invalid choice")
        menu()


def menu():
    print("""
    ========================================
              EMPLOYEE MANAGEMENT
    ========================================
    1. Register New Employee
    2. View Employee Details
    3. Count Employees
    4. List Employees
    5. View Employee Salary
    6. Update Employee Salary
    7. Add Performance Record
    8. View All Performances
    9. Delete Employee
    10. Exit
    ========================================
    """)
    choice = input("Enter your choice: ")
    if choice == "1":
        register()
    elif choice == "2":
        details()
    elif choice == "3":
        em_count()
    elif choice == "4":
        em_list()
    elif choice == "5":
        em_salary()
    elif choice == "6":
        update_salary()
    elif choice == "7":
        em_performance()
    elif choice == "8":
        perform()
    elif choice == "9":
        em_del()
    elif choice == "10":
        print("Exiting the system. Thank you!")
        exit()
    else:
        print("Invalid choice, please try again.")
        menu()

menu()
