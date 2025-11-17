import tkinter as tk
from tkinter import messagebox, simpledialog

# Data storage for users: list of dicts with username and password
users = [
    {"username": "admin", "password": "password"}
]

def login_screen():
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("300x220")

    tk.Label(root, text="Username").pack(pady=(20, 5))
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack(pady=(10, 5))
    password_entry = tk.Entry(root, show='*')
    password_entry.pack()

    def open_crud_screen():
        root.destroy()  # close login window
        crud_screen()

    def create_account():
        def save_account():
            new_username = new_username_entry.get().strip()
            new_password = new_password_entry.get().strip()
            if not new_username or not new_password:
                messagebox.showwarning("Input Error", "Both fields are required.")
                return
            # Check if username exists
            if any(user['username'] == new_username for user in users):
                messagebox.showerror("Error", "Username already exists.")
                return
            users.append({"username": new_username, "password": new_password})
            messagebox.showinfo("Success", "Account created successfully!")
            create_account_window.destroy()

        create_account_window = tk.Toplevel(root)
        create_account_window.title("Create New Account")
        create_account_window.geometry("300x180")

        tk.Label(create_account_window, text="New Username").pack(pady=(20, 5))
        new_username_entry = tk.Entry(create_account_window)
        new_username_entry.pack()

        tk.Label(create_account_window, text="New Password").pack(pady=(10, 5))
        new_password_entry = tk.Entry(create_account_window, show='*')
        new_password_entry.pack()

        save_btn = tk.Button(create_account_window, text="Save", command=save_account)
        save_btn.pack(pady=20)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if any(user['username'] == username and user['password'] == password for user in users):
            messagebox.showinfo("Login Info", f"Welcome {username}!")
            open_crud_screen()
        else:
            messagebox.showerror("Login Info", "Invalid Username or Password")

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack(pady=(10, 5))

    create_account_link = tk.Label(root, text="Create New Account", fg="blue", cursor="hand2")
    create_account_link.pack()
    create_account_link.bind("<Button-1>", lambda e: create_account())

    root.mainloop()

def crud_screen():
    crud_root = tk.Tk()
    crud_root.title("User Management (CRUD)")
    crud_root.geometry("400x300")

    listbox = tk.Listbox(crud_root)
    listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_list():
        listbox.delete(0, tk.END)
        for user in users:
            listbox.insert(tk.END, f"Username: {user['username']} Password: {user['password']}")

    def add_user():
        username = simpledialog.askstring("Input", "Enter username:")
        if not username:
            return
        password = simpledialog.askstring("Input", "Enter password:", show='*')
        if not password:
            return
        if any(u['username'] == username for u in users):
            messagebox.showerror("Error", "Username already exists.")
            return
        users.append({"username": username, "password": password})
        refresh_list()

    def update_user():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select a user to update.")
            return
        index = selected[0]
        user = users[index]
        new_username = simpledialog.askstring("Input", "Enter new username:", initialvalue=user['username'])
        if not new_username:
            return
        new_password = simpledialog.askstring("Input", "Enter new password:", initialvalue=user['password'], show='*')
        if not new_password:
            return
        # Check for username conflicts except current user
        if any(u['username'] == new_username and u != user for u in users):
            messagebox.showerror("Error", "Username already exists.")
            return
        users[index] = {"username": new_username, "password": new_password}
        refresh_list()

    def delete_user():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select a user to delete.")
            return
        index = selected[0]
        del users[index]
        refresh_list()

    btn_frame = tk.Frame(crud_root)
    btn_frame.pack(fill=tk.X)

    add_btn = tk.Button(btn_frame, text="Add", command=add_user)
    add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    update_btn = tk.Button(btn_frame, text="Update", command=update_user)
    update_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    delete_btn = tk.Button(btn_frame, text="Delete", command=delete_user)
    delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    refresh_list()
    crud_root.mainloop()

login_screen()
