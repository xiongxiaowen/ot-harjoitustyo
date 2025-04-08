
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
    - View transaction amounts and sales revenue


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
        +show_payment_confirmation(): void
        +show_updated_balance(): void
        +display_transactions(): void
        +display_revenue_info(): void
        +redirect_to_login(): void
        +redirect_to_home(): void
    }

    class UserService {
        +login(username: str, password: str): User
        +create_user(username: str, password: str): User
        +delete_user(username: str): void
        +logout(): void
    }

    class TransactionService {
        +process_payment(payment_method: str): void
        +load_money_to_card(customer: str, amount: float): void
        +get_transaction_history(): List<Transaction>
        +get_sales_revenue(): float
    }

    class UserRepository {
        +find_user_by_username(username: str): User
        +check_if_username_exists(username: str): bool
        +create_user(username: str, password: str): void
        +remove_user(username: str): void
    }

    class TransactionRepository {
        +save_transaction(transaction: Transaction): void
        +update_customer_balance(customer: str, amount: float): void
        +fetch_transaction_data(): List<Transaction>
        +calculate_total_revenue(): float
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

Sequence diagram below


```mermaid
sequenceDiagram
  participant User
  participant UI
  participant UserService
  participant TransactionService
  participant UserRepository
  participant TransactionRepository


  %% Login Process
  User->>UI: click "Login" button
  UI->>UserService: login("user", "password")
  UserService->>UserRepository: find_user_by_username("user")
  UserRepository-->>UserService: user data
  UserService-->>UI: user details
  UI->>UI: show user dashboard


  %% Create New User Process
  User->>UI: click "Create User" button
  UI->>UserService: create_user("new_user", "password")
  UserService->>UserRepository: check_if_username_exists("new_user")
  UserRepository-->>UserService: No existing user
  UserService->>UserRepository: create_user("new_user", "password123")
  UserRepository-->>UserService: user created
  UserService-->>UI: user created successfully
  UI->>UI: show user dashboard


  %% Transaction Process
  User->>UI: click "Pay with Card"
  UI->>TransactionService: process_payment("payment_method")
  TransactionService->>TransactionRepository: save_transaction
  TransactionRepository-->>TransactionService: transaction saved
  TransactionService-->>UI: payment processed successfully
  UI->>UI: show payment confirmation


  %% Delete Account Process
  User->>UI: click "Delete Account"
  UI->>UserService: delete_user("user")
  UserService->>UserRepository: remove_user("user")
  UserRepository-->>UserService: user deleted
  UserService-->>UI: confirm account deletion
  UI->>UI: redirect to home screen


  %% Logout Process
  User->>UI: click "Logout"
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
  User->>UI: enter customer details and amount
  UI->>TransactionService: load_money_to_card("customer", "amount")
  TransactionService->>TransactionRepository: update_customer_balance("customer", "amount")
  TransactionRepository-->>TransactionService: balance updated
  TransactionService-->>UI: confirm money added
  UI->>UI: show updated balance


  %% Storekeeper Views Transaction History
  User->>UI: click "View Transactions"
  UI->>TransactionService: get_transaction_history()
  TransactionService->>TransactionRepository: fetch_transaction_data()
  TransactionRepository-->>TransactionService: transaction list
  TransactionService-->>UI: transaction details
  UI->>UI: display transactions


  %% Storekeeper Views Sales Revenue
  User->>UI: click "View Sales Revenue"
  UI->>TransactionService: get_sales_revenue()
  TransactionService->>TransactionRepository: calculate_total_revenue()
  TransactionRepository-->>TransactionService: total revenue
  TransactionService-->>UI: revenue details
  UI->>UI: display revenue information
```



## Data storage


## Files


## Core Functionalities

