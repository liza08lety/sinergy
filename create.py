import tkinter as tk
from tkinter import ttk
import sqlite3

BD = 3
COLUMNS = ("id", "name", "phone", "email", "salary")
WIDTHS = (45, 200, 150, 150, 100)
TEXTS = ("ID", "Name", "Phone number", "E-MAIL", "SALARY")


# main window
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # all widget initialization
    def init_main(self):
        toolbar = tk.Frame(bd=BD)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # add buttom
        btn_add = tk.Button(
            toolbar,
            text="Добавить",
            relief=tk.RIDGE,
            bd=BD,
            command=self.open_child,
        )
        btn_add.pack(side=tk.LEFT)

        # update button
        btn_upd = tk.Button(
            toolbar,
            text="Изменить",
            bd=BD,
            command=self.open_update_child,
            relief=tk.RIDGE,
        )
        btn_upd.pack(side=tk.LEFT)

        # delete button
        btn_del = tk.Button(
            toolbar,
            text="Удалить",
            bd=BD,
            command=self.delete_records,
            relief=tk.RIDGE,
        )
        btn_del.pack(side=tk.LEFT)

        # search button
        btn_search = tk.Button(
            toolbar,
            text="Поиск",
            bd=BD,
            command=self.open_search,
            relief=tk.RIDGE,
        )
        btn_search.pack(side=tk.LEFT)

        # update button
        btn_refrech = tk.Button(
            toolbar,
            text="Обновление",
            bd=BD,
            command=self.view_records,
            relief=tk.RIDGE,
        )
        btn_refrech.pack(side=tk.LEFT)
        self.tree = ttk.Treeview(
            self,
            columns=COLUMNS,
            height=50,
            show="headings",
        )
        for name, width in zip(COLUMNS, WIDTHS):
            self.tree.column(name, width=width, anchor=tk.CENTER)

        for name, text in zip(COLUMNS, TEXTS):
            self.tree.heading(name, text=text)

        self.tree.pack(side=tk.LEFT)

        # scrollbar
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # record access
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # records view
    def view_records(self):
        self.db.cur.execute("SELECT * FROM users")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # search on records
    def search_records(self, name):
        self.db.cur.execute(
            "SELECT * FROM users WHERE name LIKE ?", ("%" + name + "%",)
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # records update method
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute(
            """
            UPDATE users
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        """,
            (name, phone, email, salary, id),
        )
        self.db.conn.commit()
        self.view_records()

    # rows deletion method
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(
                "DELETE FROM users WHERE id = ?", (self.tree.set(row, "#1"),)
            )
        self.db.conn.commit()
        self.view_records()

    # call of child window
    def open_child(self):
        Child()

    # call of update window
    def open_update_child(self):
        Update()

    # call of search window
    def open_search(self):
        Search()


# child window class
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # child window initialization
    def init_child(self):
        self.title("Добавление контакта")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text="Name")
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text="Phone number")
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text="E-MAIL")
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text="SALARY")
        label_salary.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=140)
        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.bind(
            "<Button-1>",
            lambda _: self.view.records(
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                self.entry_salary.get(),
            ),
        )
        self.btn_add.place(x=265, y=170)


# update window class
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    # window update init
    def init_update(self):
        self.title("Обновление контакта")
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text="Обновить")
        self.btn_upd.bind(
            "<Button-1>",
            lambda _: self.view.update_record(
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                self.entry_salary.get(),
            ),
        )
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_upd.place(x=265, y=170)

    # fill table with default data
    def default_data(self):
        try:
            id = self.view.tree.set(self.view.tree.selection()[0], "#1")
            self.db.cur.execute("SELECT * from users WHERE id = ?", (id,))
            row = self.db.cur.fetchone()
            self.entry_name.insert(0, row[1])
            self.entry_phone.insert(0, row[2])
            self.entry_email.insert(0, row[3])
            self.entry_salary.insert(0, row[4])
        except Exception as e:
            print("Choose row!!!", e)


# class of search window
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # search widget init
    def init_child(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text="NAME")
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)
        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=70)
        self.btn_add = tk.Button(self, text="Найти")
        self.btn_add.bind(
            "<Button-1>", lambda ev: self.view.search_records(self.entry_name.get())
        )
        self.btn_add.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_add.place(x=225, y=70)


# db class
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("employees.db")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        # If the previous execution return tuple, then table exists
        if self.cur.fetchone():
            print("Table exist")
        else:
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary INTEGER
                    )"""
            )
            self.conn.commit()
            self.default_data()

    # insertion
    def insert_data(self, name, phone, email, salary):
        self.cur.execute(
            """
                INSERT INTO users (name,phone,email,salary)
                VALUES (?, ?, ?, ?)""",
            (name, phone, email, salary),
        )
        self.conn.commit()

    # first db init (if db is empty)
    def default_data(self):
        usr = [
            (
                1,
                "Иванов Никита Сергеевич",
                "+7123456789",
                "ivannikitsergeev@mail.ru",
                1e5,
            ),
            (
                2,
                "Сергеев Иван Никитович",
                "+7223456789",
                "sergeevivannikitvich@mail.ru",
                2e5,
            ),
            (
                3,
                "Иванов Сергей Никитович",
                "+7323456789",
                "ivanovsergeinikitovick@mail.ru",
                3e5,
            ),
            (
                4,
                "Сергеев Иван Никитович",
                "+7423456789",
                "sergeevivanikitovik@mail.ru",
                4e5,
            ),
            (
                5,
                "Никитов Дмитрий Сергеевич",
                "+7523456789",
                "nikitovdmitriisergeevich@mail.ru",
                5e5,
            ),
        ]
        query_insert = """
        INSERT INTO users (id,name,phone,email,salary)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cur.executemany(query_insert, usr)
        self.conn.commit()


# app run
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников")
    root.geometry("768x768")
    root.resizable(False, False)
    root.configure(bg="lightblue")
    root.mainloop()
