# Requirements Specification

**Purpose of the application**


The application allows storekeeper and staff to offer a membership payment card solution to customers. It attracts customers to benefit discounts by using the membership payment card solution. It helps to retain long-term customer loyalty, provides user-friendly cash and card payment experience, support customers to keep track of completed purchases, and streamline store keeper's transaction management. A fixed 10% discount applys to the users using payment card as a payment method. The application can be used by multiple registered users.

**Users**


The application has a user role, normal end users as customers. A payment card store's storekeeper role as centralized admin was added to the application in the later phase.

**User interface**


UI for customers
- Home Screen elements (DONE)


Own profile (view own username, change password); View payment card balance; View past purchase history (transaction list).(DONE)

UI for storekeeper
- Home Screen elements (DONE)


Own profile (view own username); View customer list and customer's current balance; View cash register balance; View transaction history; View the amount of sales revenue. (DONE)


**Functionality in the basic version**


1 Before user logon, incl. customer and storekeeper
- user can create user account with unique credentials. (DONE)
- user can logon to the system by username and password. (DONE)


2 After customer logon
- Customer can review loaded balance to the payment card, loading to be operated by storekeeper. (DONE)
- Customer can pay purchases by using the payment card or cash, payment to be processed by storekeeper when trasaction happens. (DONE)
- Customer can check the balance and transaction history. (DONE)
- Customer can log out. (DONE)


3 Payment card's storekeeper
- Storekeeper can load money to customer cards. (DONE)
- can process or receive the payment via the payment card or cash.(DONE)
- can view the transaction history and sales revenue.(DONE)
- can view cash register balance which supports accurate transaction monitor.(DONE)
- can log out. (DONE)

**Further development**
- A user friendly GUI. (DONE)
- User can modify own profile (password). (DONE)
- Customer as a User can delete own account. (DONE)
- A user friendly dashboard to view the balance, transaction history for storekeeper. (DONE)
- Apply discounts for customers during transactions. Customer paying with the membership payment card can receive fixed percentage discounts. (DONE)
- Transaction will be declined, if no sufficient money in card. (DONE)
