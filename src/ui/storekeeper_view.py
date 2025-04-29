import tkinter as tk
from tkinter import messagebox, ttk
from src.services.user_service import UserService
from src.services.transaction_service import TransactionService
from src.repositories.user_repository import UserRepository
from src.repositories.transaction_repository import TransactionRepository


def open_storekeeper_dashboard(user):
    """This is for building the storekeeper's UI where storekeeper all operations happen on this page

    Args:
        user (storekeeper): Admin role being able to process transactions and loading cards

    Raises:
        ValueError: _description_
        ValueError: _description_
    """
    user_service = UserService(UserRepository())
    transaction_service = TransactionService(TransactionRepository())
    user_repository = UserRepository()
    window = tk.Tk()
    window.geometry("600x500")
    window.title("Storekeeper Dashboard")

    tk.Label(window, text=f"Welcome to Storekeeper Dashboard!\nLogged in as admin: {user.username}", font=("Arial", 16, "bold")).pack(pady=10, fill="x")

    def logout():
        from src.ui.main_login_view import open_login_view
        window.destroy()
        open_login_view()

    def show_all_transactions():
        """Transactions overview"""
        transactions = transaction_service.get_transaction_history()
        if not transactions:
            messagebox.showinfo("Transactions", "No transactions recorded.")
            return
        history_window = tk.Toplevel(window)
        history_window.geometry("400x300")
        history_window.title("All Transactions")
        for tx in transactions:
            label = f"{tx['date']} - User ID {tx['user_id']} - User Name {tx['username']} - {tx['amount']} euros - {tx['payment_method']}"
            tk.Label(history_window, text=label).pack()
  
    def load_card_balance():
        """Load funds to customer"""
        def submit_load():
            username = username_entry.get()
            amount_str = amount_entry.get()
            if not username or not amount_str:
                messagebox.showerror("Error", "Please enter both username and amount.")
                return
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount.")
                return
            customer = user_repository.find_user_by_username(username)
            if not customer:
                messagebox.showerror("Error", "Customer not found.")
                return
            success = transaction_service.load_money_to_card(username, amount)
            if success:
                messagebox.showinfo("Success", f"{amount:.2f} euros loaded to {username}'s card.")
                load_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to load money to card.")

        """loading operation window on top of the Dashboard"""
        load_window = tk.Toplevel(window)
        load_window.geometry("400x300")
        load_window.title("Load Money to Card")

        tk.Label(load_window, text="Customer Username:").pack()
        username_entry = tk.Entry(load_window)
        username_entry.pack()

        tk.Label(load_window, text="Amount to Load:").pack()
        amount_entry = tk.Entry(load_window)
        amount_entry.pack()

        tk.Button(load_window, text="Submit", command=submit_load).pack(pady=5)

    def show_total_revenue():
        """Display total revenue, incl. both card and cash payment"""
        total = transaction_service.get_total_revenue()
        messagebox.showinfo("Total Revenue", f"Total Revenue: {total:.2f} euros")

    def show_cash_register_balance():
        """Display total income by cash"""
        total = transaction_service.get_cash_register_balance()
        messagebox.showinfo("Cash Register Balance", f"Cash Register Balance: {total:.2f} euros")

    def process_payment():
        """define the logic for processing payment"""
        def submit_payment():
            username = username_entry.get()
            amount_str = amount_entry.get()
            method = payment_method.get()

            if not username or not amount_str or not method:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount.")
                return
            customer = user_repository.find_user_by_username(username)
            if not customer:
                messagebox.showerror("Error", "Customer not found.")
                return

            success = transaction_service.process_payment(username, amount, method)
            if success:
                messagebox.showinfo("Success", f"{amount:.2f} euros processed via {method}.")
                payment_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to execute the payment.")

        payment_window = tk.Toplevel(window)
        payment_window.title("Process Customer Payment")
        payment_window.geometry("400x300")

        tk.Label(payment_window, text="Customer Username:").pack(pady=5)
        username_entry = tk.Entry(payment_window)
        username_entry.pack()

        tk.Label(payment_window, text="Payment Amount (Euros):").pack(pady=5)
        amount_entry = tk.Entry(payment_window)
        amount_entry.pack()

        tk.Label(payment_window, text="Payment Method:").pack(pady=5)
        payment_method = tk.StringVar(value="cash")
        tk.Radiobutton(payment_window, text="Cash", variable=payment_method, value="cash").pack()
        tk.Radiobutton(payment_window, text="Card", variable=payment_method, value="card").pack()

        tk.Button(payment_window, text="Submit Payment", command=submit_payment).pack(pady=10)

    """Revenue summary and cash summary"""
    tk.Button(window, text="Process Payment", command=process_payment).pack(anchor="w", padx=20, pady=5)
    tk.Button(window, text="Load Money to Customer Card", command=load_card_balance).pack(anchor="w", padx=20, pady=5)
    tk.Button(window, text="View Total Revenue", command=show_total_revenue).pack(anchor="w", padx=20, pady=5)
    tk.Button(window, text="View Cash Register Balance", command=show_cash_register_balance).pack(anchor="w", padx=20, pady=5)
    tk.Button(window, text="View All Transactions", command=show_all_transactions).pack(anchor="w", padx=20, pady=5)

    tk.Button(window, text="Log Out", command=logout).pack(anchor="w", padx=20, pady=5)

    """Display all registered customers with current balances upon admin login."""
    customer_frame = tk.Frame(window)
    customer_frame.pack(padx=10, pady=10, anchor="w")

    tk.Label(customer_frame, text="Registered Customers & Current Balance:", font=("Arial", 12, "bold")).pack(anchor="w")

    customers = user_repository.get_all_customers()
    for cust in customers:
        info = f"Username: {cust.username} | Balance: €{cust.balance:.2f}"
        tk.Label(customer_frame, text=info, anchor="w", justify="left").pack(anchor="w")

    window.mainloop()
