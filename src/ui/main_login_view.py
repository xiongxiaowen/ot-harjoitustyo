import tkinter as tk
from tkinter import messagebox
from src.services.user_service import UserService
from src.ui.customer_view import open_customer_dashboard
from src.ui.storekeeper_view import open_storekeeper_dashboard
from src.repositories.user_repository import UserRepository

def open_login_view():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get().lower()

        try:
            user = user_service.login(username, password)
            if user and user.role == role:
                root.destroy()
                if role == "customer":
                    open_customer_dashboard(user)
                else:
                    open_storekeeper_dashboard(user)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials or role")
        except InvalidCredentialsError as e:
            messagebox.showerror("Login Failed", str(e))

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get().lower()

        if user_service.create_user(username, password, role):
            messagebox.showinfo("Registration", "User registered successfully!")
        else:
            messagebox.showerror("Error", "User already exists")

    user_service = UserService(UserRepository())
    root = tk.Tk()
    root.title("Membership Card Login")

    tk.Label(root, text="Welcome to the XX store membership card", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Select Role").pack()
    role_var = tk.StringVar(value="Customer")
    tk.Radiobutton(root, text="Customer", variable=role_var, value="Customer").pack()
    tk.Radiobutton(root, text="Storekeeper", variable=role_var, value="Storekeeper").pack()

    tk.Button(root, text="Login", command=handle_login).pack(pady=5)
    tk.Button(root, text="Register", command=handle_register).pack()

    root.mainloop()
