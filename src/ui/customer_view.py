import tkinter as tk
from tkinter import messagebox
from src.services.user_service import UserService
from src.services.transaction_service import TransactionService
from src.repositories.user_repository import UserRepository
from src.repositories.transaction_repository import TransactionRepository


def open_customer_dashboard(user):
    """Customer Dashboard View Module

    Provides the graphical user interface for customers in the membership card application.
    Allows customers to manage their account, view transactions, and check their balance,etc.

    The dashboard provides the following functionality:
    - Password change
    - Balance display
    - Transaction history viewing
    - Account logout
    - Account deletion
    """
    service = UserService(UserRepository())
    transaction = TransactionService(TransactionRepository())

    def logout():
        """customer can logout"""
        from src.ui.main_login_view import open_login_view
        window.destroy()
        open_login_view()

    def delete_account():
        """customer can delete account"""
        from src.ui.main_login_view import open_login_view
        if messagebox.askyesno("Confirm", "Are you sure you want to delete your user account?"):
            service.delete_account(user.username)
            messagebox.showinfo("Deleted", "Account deleted successfully!")
            window.destroy()
            open_login_view()
    
    def change_password():
        """customer can change password"""
        new_password = password_entry.get()
        if new_password:
            service.change_password(user.username, new_password)
            messagebox.showinfo("Updated", "Password changed successfully!")
    
    """creat the customer view screen"""
    window = tk.Tk()
    window.geometry("600x500")
    window.title("Customer Dashboard")

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    """add welcome message"""
    tk.Label(window, text=f"Welcome, {user.username}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

    """allow change password"""
    tk.Label(window, text="Change Password", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=(5, 0))
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=2, column=0, padx=(30, 10), pady=5, sticky="e")

    tk.Button(window, text="Update Password", command=change_password).grid(row=2, column=1, padx=(10, 30), pady=5, sticky="w")

    """show balance"""
    balance = service.get_balance(user.username)
    tk.Label(window, text=f"Current Balance: euros {balance:.2f}", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=15)


    """show transaction history"""
    tk.Label(window, text="Transaction History (Discount applied to card payment)", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=10)
    transactions = transaction.get_customer_transactions(user.username)
    if transactions:
        for idx, tx in enumerate(transactions):
            label = f"{tx['date']} - {tx['amount']} euros - {tx['method']}"
            tk.Label(window, text=label, font=("Arial", 10)).grid(row=5 + idx, column=0, columnspan=2, sticky="w", padx=40)
    else:
        tk.Label(window, text="No transactions found.").grid(row=5, column=0, columnspan=2)

    final_row = 5 + len(transactions) if transactions else 6
    
    """add buttons for logout and delete"""
    tk.Button(window, text="Log Out", command=logout, width=15).grid(row=final_row + 1, column=0, pady=30)
    tk.Button(window, text="Delete Account", command=delete_account, width=15).grid(row=final_row + 1, column=1, pady=30)

    window.mainloop()
