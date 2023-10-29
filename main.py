
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class EmployeeManagementApp:
    def __init__(self, master):
        self.master = master  # Создание переменной, которая будет содержать главное окно приложения
        self.master.title("Список сотрудников компании")  # Задание заголовка окна  

        self.conn = sqlite3.connect("employees.db")
        self.create_table()

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="ФИО")
        self.tree.heading("Phone", text="Номер телефона")
        self.tree.heading("Email", text="E-mail")
        self.tree.heading("Salary", text="Зарплата")
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            salary INTEGER
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="Добавить сотрудника", command=self.add_employee, compound=tk.LEFT)  # Создание кнопки "Добавить сотрудника"
        self.add_button.pack(pady=10)  # Размещение кнопки на форме
        self.add_button_image = tk.PhotoImage(file="img/add.png")
        self.add_button.config(image=self.add_button_image)
        self.update_button = tk.Button(self.master, text="Изменить", command=self.update_employee, compound=tk.LEFT)  # Создание кнопки "Изменить"
        self.update_button.pack(pady=10)  # Размещение кнопки на форме
        self.update_button_image = tk.PhotoImage(file="img/update.png")
        self.update_button.config(image=self.update_button_image)
        self.delete_button = tk.Button(self.master, text="Удалить сотрудника", command=self.delete_employee, compound=tk.LEFT)  # Создание кнопки "Удалить сотрудника"
        self.delete_button.pack(pady=10)  # Размещение кнопки на форме
        self.delete_button_image = tk.PhotoImage(file="img/delete.png")
        self.delete_button.config(image=self.delete_button_image)
        self.search_button = tk.Button(self.master, text="Найти сотрудника", command=self.search_employee, compound=tk.LEFT)  # Создание кнопки "Найти сотрудника"
        self.search_button.pack(pady=10)  # Размещение кнопки на форме
        self.search_button_image = tk.PhotoImage(file="img/search.png")
        self.search_button.config(image=self.search_button_image)
        self.refresh_button = tk.Button(self.master, text="Обновить", command=self.refresh_action, compound=tk.LEFT)  # Создание кнопки "Обновить"
        self.refresh_button.pack(pady=10)  # Размещение кнопки на форме
        self.refresh_button_image = tk.PhotoImage(file="img/refresh.png")
        self.refresh_button.config(image=self.refresh_button_image)
        
        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None 

    def add_employee(self):
        name = simpledialog.askstring("Input", "Введите имя сотрудника:")  # Ввод имени с помощью диалогового окна
        phone = simpledialog.askstring("Input", "Введите номер телефона сотрудника:")  # Ввод номера телефона с помощью диалогового окна
        email = simpledialog.askstring("Input", "Введите E-mail сотрудника:")  # Ввод E-mail с помощью диалогового окна
        salary = simpledialog.askinteger("Input", "Введите зарплату сотрудника:")  # Ввод зарплаты с помощью диалогового окна

        cursor = self.conn.cursor()  # Создание курсора для выполнения SQL-запросов

        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))  # Выполнение SQL-запроса на добавление нового сотрудника в таблицу employees
        self.conn.commit()  # Сохранение изменений в базе данных

        self.update_treeview()  # Обновление отображения treeview, чтобы в нем отобразился новый сотрудник

        self.last_action = "add"  # Запоминание последнего выполненного действия (в данном случае, добавление сотрудника)

    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")  # Ввод ID сотрудника, информацию о котором нужно обновить

        cursor = self.conn.cursor()  # Создание курсора для выполнения SQL-запросов
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))  # Получение данных о сотруднике из базы данных по указанному ID
        employee = cursor.fetchone()

        if employee:  # Если сотрудник найден
            name = simpledialog.askstring("Input", "Введите обновленное имя сотрудника:", initialvalue=employee[1]) # Ввод обновленного имени с помощью диалогового окна
            phone = simpledialog.askstring("Input", "Введите обновленный номер телефона сотрудника:", initialvalue=employee[2]) # Ввод обновленного номера телефона с помощью диалогового окна
            email = simpledialog.askstring("Input", "Введите обновленный E-mail сотрудника:", initialvalue=employee[3]) # Ввод обновленного E-mail с помощью диалогового окна
            salary = simpledialog.askinteger("Input", "Введите обновленную зарплату сотрудника:", initialvalue=employee[4]) # Ввод обновленной зарплаты с помощью диалогового окна

            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()

            self.update_treeview()

            self.last_action = "update"
        else:
            messagebox.showerror("Error", "Сотрудник не найден")

    def delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            confirm = messagebox.askyesno("Confirmation", "Вы уверены то что хотите удалить этого сотрудника?")
            if confirm:
                cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
                self.conn.commit()

                self.update_treeview()

                self.last_action = "delete"
        else:
            messagebox.showerror("Error", "Сотрудник не найден")

    def search_employee(self):
        search_term = simpledialog.askstring("Input", "Введите ФИО сотрдуника:")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?", (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        employees = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())

        for employee in employees:
            self.tree.insert("", tk.END, values=employee)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee = self.tree.item(item)["values"]

        self.update_employee()

    def refresh_action(self):
        if self.last_action == "add":
            self.undo_add_employee()
        elif self.last_action == "update":
            self.undo_update_employee()
        elif self.last_action == "delete":
            self.undo_delete_employee()

    def undo_add_employee(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM employees")
        emp_id = cursor.fetchone()[0]

        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()

        self.update_treeview()

    def undo_update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?", tuple(employee[1:] + (emp_id,)))
            self.conn.commit()

            self.update_treeview()

    def undo_delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")
        name = simpledialog.askstring("Input", "Введите имя сотрудника:")
        phone = simpledialog.askstring("Input", "Введите номер телефона сотрудника:")
        email = simpledialog.askstring("Input", "Введите E-mail сотрудника:")
        salary = simpledialog.askinteger("Input", "Введите зарплату сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO employees (id, name, phone, email, salary) VALUES (?, ?, ?, ?, ?)", (emp_id, name, phone, email, salary))
        self.conn.commit()

        self.update_treeview()

    def update_treeview(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())

        for employee in employees:
            self.tree.insert("", tk.END, values=employee)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
