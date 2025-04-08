import tkinter as tk
from tkinter import messagebox, ttk
from src.services.user_service import UserService
from src.services.transaction_service import TransactionService
from src.repositories.user_repository import UserRepository
from src.repositories.transaction_repository import TransactionRepository
#below needs to be refined.

user_service = UserService(UserRepository())
transaction_service = TransactionService(TransactionRepository())

def open_storekeeper_dashboard(root, storekeeper):
    root.destroy()

    window = tk.Tk()
    window.title("Storekeeper Dashboard")
    window.geometry("200x200")

    tk.Label(window, text=f"Logged in as: {storekeeper.username}").pack()

    # Transactions overview
    tk.Label(window, text="Transactions Overview:").pack()
    transactions_box = tk.Text(window, height=10, width=70)
    transactions_box.pack()
    for transaction in transaction_service.get_transaction_history():
        transactions_box.insert(tk.END, f"{transaction.username} | {transaction.amount:.2f} | {transaction.payment_method}\n")

    # Load funds to customer
    tk.Label(window, text="Select customer to load funds:").pack()
    customers = [user.username for user in user_service.user_repository.users.values() if user.role == "customer"]
    selected_customer = tk.StringVar()
    customer_menu = ttk.Combobox(window, textvariable=selected_customer, values=customers)
    customer_menu.pack()

    tk.Label(window, text="Amount to load:").pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    def load_funds():
        username = selected_customer.get()
        amount = float(amount_entry.get())
        customer = user_service.user_repository.find_user_by_username(username)
        if customer:
            transaction_service.load_money_to_card(customer, amount)
            messagebox.showinfo("Success", f"Loaded €{amount:.2f} to {username}'s card.")

    tk.Button(window, text="Load Funds", command=load_funds).pack()

    # Revenue summary (mocked from transactions)
    revenue = sum(t.amount for t in transaction_service.get_transaction_history())
    tk.Label(window, text=f"Current total revenue: €{revenue:.2f}").pack()
    tk.Label(window, text=f"Current cash register balance: €{revenue:.2f}").pack()

    tk.Button(window, text="Logout", command=lambda: logout(window)).pack()
    window.mainloop()

def logout(window):
    window.destroy()
    import src.ui.main_login_view as login_view
    login_view.show_login_view()


