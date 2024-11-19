import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def varasto_saldo(self, tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                 return 5
            if tuote_id == 3:
                 return 0

    # tehdään toteutus hae_tuote-metodille
    def varasto_hae_tuote(self, tuote_id):
        if tuote_id == 1:
            return Tuote(1, "maito", 5)
        if tuote_id == 2:
             return Tuote(2, "banaani", 2)
        if tuote_id == 3:
             return Tuote(3, "leipää", 3)
            
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()
        self.varasto_mock.saldo.side_effect = self.varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = self.varasto_hae_tuote
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_tilisiirto_oikeat_tiedot(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)
    
    def test_tilisiirto_oikeat_tiedot_kahdella_tuotteella(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 7)

    def test_tilisiirto_oikeat_tiedot_kahdella_eri_tuotteella(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 10)
    
    def test_tilisiirto_oikeat_tiedot_kahdella_eri_tuotteella_josta_yksi_on_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)

    
    def test_alointa_asiointi_ollaa_ostokset(self):
         self.kauppa.aloita_asiointi()
         self.kauppa.lisaa_koriin(1)
         self.kauppa.aloita_asiointi()
         self.kauppa.lisaa_koriin(2)
         self.kauppa.tilimaksu("pekka", "12345")
         self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 2)

    def test_uusi_viite_jokaista_ostoa_kohti(self):
         viitegeneraattori_mock = Mock()
         viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]
         kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_mock)
         kauppa.aloita_asiointi()
         kauppa.lisaa_koriin(1)
         kauppa.tilimaksu("pekka", "12345")
         self.pankki_mock.tilisiirto.assert_called_with("pekka", 1, "12345", ANY, 5)
         kauppa.aloita_asiointi()
         kauppa.lisaa_koriin(1)
         kauppa.tilimaksu("pekka", "12345")
         self.pankki_mock.tilisiirto.assert_called_with("pekka", 2, "12345", ANY, 5)

    def test_tuotteen_poistamine_toimii(self):
         self.kauppa.aloita_asiointi()
         self.kauppa.lisaa_koriin(1)
         self.kauppa.lisaa_koriin(2)
         self.kauppa.poista_korista(1)
         self.kauppa.tilimaksu("pekka", "12345")
         self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 2)