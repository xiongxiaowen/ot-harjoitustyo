import unittest
from src.models.user import User
from datetime import datetime
from src.services.transaction_service import TransactionService
from src.models.transaction import Transaction
from unittest.mock import Mock, patch

class TestTransactionService(unittest.TestCase):
    def setUp(self):
        #setup mock repository
        self.mock_repo_transaction = Mock()
        self.mock_repo_user = Mock()
        self.service = TransactionService(
            transaction_repo=self.mock_repo_transaction,
            user_repo=self.mock_repo_user
            )
        #setup test user and test transaction       
        self.test_user = User(
            user_id=1,
            username="test_customer",
            password="pass123",
            role="customer",
            balance=100.0
        )

        self.test_transaction = Transaction(
            user_id=1,
            amount=100.0,  # 90 to be reduced from balance with 10% discount by card
            payment_method="card",
            date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

    def test_load_money_ok(self):
        self.mock_repo_user.update_balance.return_value = True
        result = self.service.load_money_to_card("test_customer", 100.0)
        self.assertTrue(result)
        self.mock_repo_user.update_balance.assert_called_once_with("test_customer", 100.0)

    def test_load_money_negative_amount(self):
        self.assertFalse(self.service.load_money_to_card("test_customer", -10.0))
        self.mock_repo_user.update_balance.assert_not_called()
        
    def test_process_card_payment_success(self):
        self.mock_repo_user.get_balance.return_value = 100.0  # Numeric balance
        self.mock_repo_user.find_user_by_username.return_value = self.test_user
        self.mock_repo_transaction.save_transaction.return_value = True

        transaction = self.service.process_payment("test_customer", 100.0, "card")
        self.assertEqual(transaction.amount, 90.0) #10% discount by card
        self.mock_repo_user.update_balance.assert_called_once_with("test_customer", -90.0)
        self.mock_repo_transaction.save_transaction.assert_called_once()

    def test_process_card_payment_insufficient_balance(self):
        #reject card payment with insufficient balance
        self.mock_repo_user.get_balance.return_value = 50.0
        
        with self.assertRaises(ValueError) as context:
            self.service.process_payment("test_customer", 100.0, "card")
        self.assertEqual(str(context.exception), "Not sufficient balance to pay after discount!")
        self.mock_repo_user.update_balance.assert_not_called()

    def test_process_payment_invalid_amount(self):
        #reject non-positive amounts
        with self.assertRaises(ValueError) as context:
            self.service.process_payment("test_customer", -50.0, "card")
        self.assertEqual(str(context.exception), "Amount must be positive")

    def test_process_cash_payment_success(self):
        cash_transaction = self.service.process_payment("test_customer", 100.0, "cash")
        self.assertEqual(cash_transaction.amount, 100.0) #10% discount not apply to cash payment
        self.mock_repo_user.update_balance.assert_not_called() #no need update balance
        self.mock_repo_transaction.save_transaction.assert_called_once()

    def test_get_customer_transactions(self):
        expected_transactions = [self.test_transaction]
        self.mock_repo_transaction.get_transactions_by_username.return_value = expected_transactions
        
        result = self.service.get_customer_transactions("test_customer")
        self.assertEqual(result, expected_transactions)
        self.mock_repo_transaction.get_transactions_by_username.assert_called_once_with("test_customer")

    def test_get_transaction_history(self):
        #Return all transaction records stored in database. for storekeeper.
        expected_history = [self.test_transaction]
        self.mock_repo_transaction.get_all_transactions.return_value = expected_history
        
        result = self.service.get_transaction_history()
        self.assertEqual(result, expected_history)

    def test_get_total_revenue(self):
        #Should calculate total revenue for storekeeper
        self.mock_repo_transaction.get_total_revenue.return_value = 500.0
        
        result = self.service.get_total_revenue()
        self.assertEqual(result, 500.0)

    def test_get_cash_register_balance(self):
        #Should calculate cash balance for storekeeper
        self.mock_repo_transaction.get_cash_register_balance.return_value = 200.0
        
        result = self.service.get_cash_register_balance()
        self.assertEqual(result, 200.0)

if __name__ == "__main__":
    unittest.main()