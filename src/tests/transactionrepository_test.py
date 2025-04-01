import unittest
from src.models.user import User
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService
from src.models.transaction import Transaction

class TransactionRepository(unittest.TestCase):
    def setUp(self):
        self.repo = TransactionRepository() 
        self.test_user = User("test_user", "pw123")
        self.test_transaction = Transaction(user = self.test_user, testamount = 100.0, payment_method = "card")

    def test_transaction_repository_setup_ok(self):
        self.assertNotEqual(self.repo, None) #transaction_repository successfully created

    #test save_transaction ok, verifies transactions are appended
    def test_save_transaction_setup_ok(self):
        self.repo.save_transaction(self.test_transaction)
        self.assertIn(self.test_transaction, self.repo.transactions)
        self.assertEqual(len(self.repo.transactions), 1)

    #fetch transaction 0, list is empty
    def test_fetch_no_transaction(self):
        self.assertEqual(self.repo.fetch_transaction_data(), [])

    def test_fetch_with_transaction(self):
        test1 = Transaction(self.test_user, 10.0, "card")
        test2 = Transaction(self.test_user, 20.0, "cash")
        self.repo.save_transaction(test1)
        self.repo.save_transaction(test2)
        
        transactions = self.repo.fetch_transaction_data()
        self.assertEqual(len(transactions), 2)
        self.assertIn(test1, transactions)
        self.assertIn(test2, transactions)


    # test updating a new customer, balance 0
    def test_update_balance_new_customer(self): 
        self.repo.update_customer_balance(self.test_user, 30.0)
        self.assertEqual(self.repo.user_balances[self.test_user.username], 30.0)

    # test updating a existing customer
    def test_update_balance_existing_customer(self):
        self.repo.update_customer_balance(self.test_user, 100.0)
        self.assertEqual(self.repo.user_balances[self.test_user.username], 100.0)
        #reduce -30.0
        self.repo.update_customer_balance(self.test_user, -30.0)
        self.assertEqual(self.repo.user_balances[self.test_user.username], 70.0)