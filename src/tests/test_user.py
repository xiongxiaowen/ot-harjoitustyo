import unittest
from src.models.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        #setup users for testing
        self.customer = User(
            user_id = 1,
            username="customer_test",
            password="password123",
            role= "customer",
            balance= 100.0
            )

        self.storekeeper = User(
            user_id = 2,
            username="admin",
            password="adminpassword123",
            role= "storekeeper",
            balance= 0.0
            )

    def test_setup_value_ok(self):
        #users setup ok
        self.assertEqual(self.customer.user_id, 1)
        self.assertEqual(self.customer.username, "customer_test")
        self.assertEqual(self.customer.password, "password123")
        self.assertEqual(self.customer.role, "customer")
        self.assertEqual(self.customer.balance, 100.0)
        self.assertEqual(self.storekeeper.user_id, 2)
        self.assertEqual(self.storekeeper.username, "admin")
        self.assertEqual(self.storekeeper.password, "adminpassword123")
        self.assertEqual(self.storekeeper.role, "storekeeper")
        self.assertEqual(self.storekeeper.balance, 0.0)

    def test_is_storekeeper(self):
        #should identify the storekeeper role
        self.assertTrue(self.storekeeper.is_storekeeper())
        self.assertFalse(self.customer.is_storekeeper())

    def test_is_customer(self):
        #should identify the customer role
        self.assertTrue(self.customer.is_customer())
        self.assertFalse(self.storekeeper.is_customer())


if __name__ == "__main__":
    unittest.main()