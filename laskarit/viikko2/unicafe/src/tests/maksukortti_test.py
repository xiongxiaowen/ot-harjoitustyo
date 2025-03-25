import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_balanceright_atbeginning(self): 
        #Kortin saldo alussa oikein
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    
    def test_load_balance_correct(self):
        #Rahan lataaminen kasvattaa saldoa oikein
        self.maksukortti.lataa_rahaa(2000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 30.00 euroa")
    
    def test_reduce_balance_correctly(self):
        #Saldo vahenee oikein, jos rahaa on tarpeeksi
        self.maksukortti.ota_rahaa(1000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 0.00 euroa")

    def test_if_balance_not_sufficient(self):
        #Saldo ei muutu, jos rahaa ei ole tarpeeksi
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_return_correct_value(self):
        #Metodi palauttaa True, jos rahat riittivat ja muuten False
        self.assertTrue(self.maksukortti.ota_rahaa(500)) #rahaa riitti
        self.assertFalse(self.maksukortti.ota_rahaa(1500)) #rahaa ei riitta

    def test_balance_return_as_euro(self):
        #cover the line 17 ensure coverage 100%, convert cents into euros.
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)