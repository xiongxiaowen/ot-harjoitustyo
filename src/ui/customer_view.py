import tkinter as tk
from tkinter import messagebox
from src.services.user_service import UserService
from src.services.transaction_service import TransactionService
from src.repositories.user_repository import UserRepository
from src.repositories.transaction_repository import TransactionRepository


def open_customer_dashboard(user):
    service = UserService(UserRepository())
    transaction = TransactionService(TransactionRepository())

    #customer can logout
    def logout():
        from src.ui.main_login_view import open_login_view
        window.destroy()
        open_login_view()

    #customer can delete account
    def delete_account():
        from src.ui.main_login_view import open_login_view
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your user account?"):
            service.delete_account(user.username)
            messagebox.showinfo("Deleted", "Account deleted successfully!")
            window.destroy()
            open_login_view()
    
    #customer can change password
    def change_password():
        new_password = password_entry.get()
        if new_password:
            service.change_password(user.username, new_password)
            messagebox.showinfo("Updated", "Password changed successfully!")
    
    #creat the customer view screen
    window = tk.Tk()
    window.geometry("600x500")
    window.title("Customer Dashboard")

    # add welcome message
    tk.Label(window, text=f"Welcome, {user.username}", font=("Arial", 14)).pack(pady=10)

    #allow change password
    tk.Label(window, text="Change Password").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()
    tk.Button(window, text="Update Password", command=change_password).pack(pady=5)

    #show balance
    balance = service.get_balance(user.username)
    tk.Label(window, text=f"Current Balance: euros {balance:.2f}", font=("Arial", 12)).pack(pady=10)

    #show transaction history
    tk.Label(window, text="Transaction History", font=("Arial", 12)).pack(pady=10)
    transactions = transaction.get_customer_transactions(user.username)
    if transactions:
        for tx in transactions:
            label = f"{tx['date']} - {tx['amount']} euros - {tx['method']}"
            tk.Label(window, text=label).pack()
    else:
        tk.Label(window, text="No transactions found.").pack()

    #add buttons for logout and delete
    tk.Button(window, text="Log Out", command=logout).pack(side=tk.LEFT, padx=10, pady=20)
    tk.Button(window, text="Delete Account", command=delete_account).pack(side=tk.RIGHT, padx=10, pady=20)

    window.mainloop()
