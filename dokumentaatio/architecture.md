
# Architecture Description

## Structure

The program structure follows a three-tier layered architecture, and the code packaging structure is as follows:<br>
/ membership_card_system<br>
&ensp;/ui (User Interface components)<br>
&ensp;/ services       (Application logic to complete operations)<br>
&ensp;/ repositories   (Data storage)<br>
&ensp;/ entities       (Core domain class)<br>
    
![package structure](./pic/package_structure.png)


The ui package contains the user interface logic, services handle business operation logic, and repositories manage data storage. The entities package defines core data structures used throughout the application.

## User Interface
The UI consists of separate views for customers and storekeepers:
- Customer UI:
    - View profile
    - Check payment balance
    - View transaction history

- Storekeeper UI:
    - View profile
    - Check cash register balance
    - View transaction history and sales revenue


The UI interacts with services module's classes to handle business logic.

## Application Logic
Class diagram below illustrates the application logic.
```mermaid
classDiagram
    class User {
        +username: str
        +password: str
        +create_user(): void
        +login(): void
        +logout(): void
        +delete_account(): void
    }

    class UI {
        +show_dashboard(): void
        +redirect_process_payment_(): void
        +redirect_load_money_to_card(): void
        +show_updated_balance(): void
        +display_transactions(): void
        +display_revenue_info(): void
        +redirect_to_home(): void
    }

    class UserService {
        +login(username: str, password: str): User
        +create_user(username: str, password: str): User
        +delete_user(username: str): void
        +change_password(username: str, password: str): void
        +get_balance(username: str): void
        +logout(): void
    }

    class TransactionService {
        +process_payment(username: str, amount: float, payment_method: str): void
        +load_money_to_card(username: str, amount: float): void
        +get_Customer_transaction_history(): List<Transaction>
        +get_All_transaction_history(): List<Transaction>
        +get_sales_revenue(): float
        +get_cash_register_balance():float
    }

    class UserRepository {
        +find_user_by_username(username: str): User
        +check_if_username_exists(username: str): bool
        +create_user(username: str, password: str): void
        +delete_user(username: str): void
        +update_password(username: str, password: str): void
        +get_balance(username: str): void
        +update_customer_balance(customer: str, amount: float): void
        +get_all_customers(): void
    }

    class TransactionRepository {
        +save_transaction(transaction: Transaction): void
        +get_transactions_by_username(): void
        +fetch_transaction_data(): List<Transaction>
        +calculate_total_revenue(): float
        +calculate_total_cashregister(): float
    }

    class Transaction {
        +id: int
        +amount: float
        +payment_method: str
        +date: Date
    }

    User --> UI : interacts with
    UI --> UserService : calls for user actions
    UI --> TransactionService : calls for transaction actions
    UserService --> UserRepository : queries and updates user data
    TransactionService --> TransactionRepository : queries and updates transaction data
    TransactionRepository --> Transaction : manages transactions
```

Sequence diagram below illustrates the core functionalities


```mermaid
sequenceDiagram
  participant User
  participant UI
  participant UserService
  participant TransactionService
  participant UserRepository
  participant TransactionRepository


  %% Login Process
  User->>UI: customer click "Login" button 
  UI->>UserService: login("user", "password")
  UserService->>UserRepository: find_user_by_username("user")
  UserRepository-->>UserService: user data
  UserService-->>UI: user details
  UI->>UI: show user dashboard


  %% Create New User Process
  User->>UI: customer click "Create User" button
  UI->>UserService: create_user("new_user", "password")
  UserService->>UserRepository: check_if_username_exists("new_user")
  UserRepository-->>UserService: No existing user
  UserService->>UserRepository: create_user("new_user", "password123")
  UserRepository-->>UserService: user created
  UserService-->>UI: user created successfully
  UI->>UI: show user dashboard


  %% Transaction Process
  User->>UI: customer at store "Pay with Card"
  UI->>TransactionService: storekeeper process_payment("payment_method") apply discount
  TransactionService->>TransactionRepository: save_transaction
  TransactionRepository-->>TransactionService: transaction saved
  TransactionService-->>UI: payment processed successfully
  UI->>UI: show payment confirmation


  %% Delete Account Process
  User->>UI: Customer click "Delete Account"
  UI->>UserService: delete_user("user")
  UserService->>UserRepository: remove_user("user")
  UserRepository-->>UserService: user deleted
  UserService-->>UI: confirm account deletion
  UI->>UI: redirect to home screen


  %% Logout Process
  User->>UI: click "Logout" (customer & storekeeper)
  UI->>UserService: logout()
  UserService-->>UI: session terminated
  UI->>UI: redirect to login screen


  %% Storekeeper Operations
  User->>UI: Storekeeper logs in
  UI->>UserService: login("storekeeper", "password")
  UserService->>UserRepository: find_storekeeper_by_username("storekeeper")
  UserRepository-->>UserService: storekeeper data
  UserService-->>UI: storekeeper details
  UI->>UI: show storekeeper dashboard


  %% Storekeeper Loads Money to Customer Card
  User->>UI: enter customer username and amount
  UI->>TransactionService: load_money_to_card("customer", "amount")
  TransactionService->>TransactionRepository: update_customer_balance("customer", "amount")
  TransactionRepository-->>TransactionService: balance updated
  TransactionService-->>UI: confirm money added
  UI->>UI: show updated balance


  %% Views Transaction History
  User->>UI: click "View Transactions" (for both customer & storekeeper)
  UI->>TransactionService: get_transaction_history()
  TransactionService->>TransactionRepository: fetch_transaction_data()
  TransactionRepository-->>TransactionService: transaction list
  TransactionService-->>UI: transaction details
  UI->>UI: display transactions


  %% Storekeeper Views Sales Revenue
  User->>UI: storekeeper click "View Sales Revenue" (total revenue or only cash payment)
  UI->>TransactionService: get_sales_revenue()
  TransactionService->>TransactionRepository: calculate_total_revenue()
  TransactionRepository-->>TransactionService: total revenue
  TransactionService-->>UI: revenue details
  UI->>UI: display revenue information
```


## Data storage
Data is stored in SQLite database. Users and transactions are stored in the SQLite database tables users and transactions, which are initialized in the initialize_database.py file.

### Files
Files used to build up the program are structured as below

```
├── src/
│   ├── initialize_database.py        # Creates and setup initial database schema
│   ├── database_connection.py        # Manages connections to the database
│   │
│   ├── ui/                           # Contains all user interface components
│   │   ├── main_login_view.py        # Main login entry point
│   │   ├── customer_view.py          # Displays the customer interface
│   │   └── storekeeper_view.py       # Shows the storekeeper/admin interface
│   │
│   ├── models/                       # Defines data structures/entities
│   │   ├── user.py                   # User model definition
│   │   └── transaction.py            # Transaction model definition
│   │
│   ├── repositories/                 # Data layer, database operations
│   │   ├── user_repository.py        # Database storage for users
│   │   └── transaction_repository.py # Database storage for transactions
│   │
│   ├── services/                     # Contains business logic
│   │   ├── user_service.py           # User-related business operations
│   │   └── transaction_service.py    # Transaction processing operations
```

## Functionalities for future development (not in this course scope)
Based on business demand, it is possible to add below features to enrich the program: 
- Based on purchased value, classify customers into various classes or levels which entitle customer various discount. 
- Push discount or campaign notification from storekeeper to customer end based on customer class. 
- Fancy user interface can be possible if adding more colors or graphic design elements. 
- Customer dashboard to be integrated with bank account, allow customer load money online from bank to top up the memberhsip card, growing the balance as diposit. Balance is customer's asset.
- Allow customer bind bank card and credit card to memberhsip payment card application, for easier toping up and grow the balance.
- Add possible financial services for customer's balance: grant customer interests daily (reasonable interest rate) if balance reach a certain amount, e.g.>= 1k €.
- integrate with fund and stock sales service, allow customer to purchase and manage fund and stock market investments. 

