# Instructions for use

Download the source code for the latest [release](https://github.com/xiongxiaowen/ot-harjoitustyo/releases/tag/Viikko5) of the project by selecting _Source code_ under the _Assets_ section.

Note: This program was developed on Windows, all commands mentioned in this program is based on Windows. Please use Linux command line if run on Linux. Program was tested every week on Omnissa Horizon Client, program can open and work well with Cubbli Linux.

**Starting the program**


Before starting the program, install the dependencies with the command: 
- poetry install


After which, perform the initialization steps with the command:
- poetry run invoke build


Then start the program with the command:
- poetry run invoke start


**Login**


The application starts in the home page login view:
![](./kuvat/kayttoohje-kirjautuminen.png)

Customer login to the application as a customer role. A storekeeper login as a storepeeker role, which allows to access data and operations as a admin, e.g. view registered customer list and customer's current balance; process payment, load money to customer card, view total revenue including both card and cash payment types; view cash balance (revenue via cash payment); view all customer transactions.

**Creating a new user**


Create for a customer
- 
- 
- 

Create for a storekeeper
- 
- 
- 

**Customer's dashboard functions**
- Customer can modify own profile (password), modified password works as new valid password.
- Customer can view/check the balance aftering loading money to the payment card at store (initial balance 0), loading operation by storepeeker.
- Customer can pay purchases at store by using the payment card or cash. benefit 10% discount if pay by membership payment card, balance will be reduced after transaction.
- Customer can view transaction history(timestamp, amount and payment type). 
- Customer can log out. 
- Customer can delete own account if quit from the membership card.

**Storekeeper's dashboard functions**
- view registered customer list and customer's current balance; 
- process payment: receive the payment via the payment card or cash. Apply discounts for customers during card transactions. Transaction will be declined, if no sufficient money in card.
- load money to customer card. 
- view total revenue including both card and cash payment types; 
- view cash balance (revenue via cash payment); 
- view all customer transactions.
- can log out.
