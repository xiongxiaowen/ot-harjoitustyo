import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate() 
        self.kortti = Maksukortti(1000)

    def test_kassapaate_setup_ok(self):
        self.assertNotEqual(self.kassa, None) #kassapaate successfully created

    def test_initial_status_correct(self):
        # rahamaara ja myytyjen lounaiden maara on oikea (rahaa 1000 euroa, lounaita myyty 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)

    #edullisten lounaiden osalta
    def test_take_edullisten_cashpayment_enough(self):
        vaihtoraha =self.kassa.syo_edullisesti_kateisella(300)
        self.assertEqual(vaihtoraha, 60) # edullisten lounaiden maksaa 240
        self.assertEqual(self.kassa.kassassa_rahaa, 100240) #kassa kasvaa 240
        self.assertEqual(self.kassa.edulliset, 1) #saa 1 lounaan myyty

    def test_take_edullisten_cashpayment_notenough(self):
        vaihtoraha =self.kassa.syo_edullisesti_kateisella(100)
        self.assertEqual(vaihtoraha, 100) #kaikki rahat palautetaan vaihtorahana
        self.assertEqual(self.kassa.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassa.edulliset, 0) 
    
    #maukkaan lounaiden osalta
    def test_take_maukkaan_cashpayment_enough(self):
        vaihtoraha =self.kassa.syo_maukkaasti_kateisella(600)
        self.assertEqual(vaihtoraha, 200) # maukkaan lounaiden maksaa 400
        self.assertEqual(self.kassa.kassassa_rahaa, 100400) #kassa kasvaa 400
        self.assertEqual(self.kassa.maukkaat, 1) #saa 1 lounaan myyty

    def test_take_maukkaan_cashpayment_notenough(self):
        vaihtoraha =self.kassa.syo_maukkaasti_kateisella(100)
        self.assertEqual(vaihtoraha, 100) #kaikki rahat palautetaan vaihtorahana
        self.assertEqual(self.kassa.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassa.maukkaat, 0) 

    #Kortilla
    def test_take_edullisten_cardpayment_enough(self):
        payment = self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertTrue(payment)
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_take_edullisten_cardpayment_notenough(self):
        kortti1 = Maksukortti(100)
        payment = self.kassa.syo_edullisesti_kortilla(kortti1)
        self.assertFalse(payment)
        self.assertEqual(self.kortti.saldo, 100)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_take_maukkaan_cardpayment_enough(self):
        payment = self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertTrue(payment)
        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_take_maukkaan_cardpayment_notenough(self):
        kortti2 = Maksukortti(300)
        payment = self.kassa.syo_maukkaasti_kortilla(kortti2)
        self.assertFalse(payment)
        self.assertEqual(self.kortti.saldo, 300)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

#Kortille rahaa ladattaessa
    def test_load_card(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 700)
        self.assertEqual(self.kortti.saldo, 1700)
        self.assertEqual(self.kassa.kassassa_rahaa, 100700)
    
    def test_load_card_no_negatiive(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -700)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
    
    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)

