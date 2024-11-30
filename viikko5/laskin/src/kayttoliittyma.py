from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4

class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self.tmp = 0 
        self.sovelluslogiikka = sovelluslogiikka
        self.lue_syote = lue_syote

    def suorita(self):
        self.tmp = self.sovelluslogiikka.arvo()
        self.sovelluslogiikka.plus(self.lue_syote())


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self.tmp = 0 
        self.sovelluslogiikka = sovelluslogiikka
        self.lue_syote = lue_syote

    def suorita(self):
        self.tmp = self.sovelluslogiikka.arvo()
        self.sovelluslogiikka.miinus(self.lue_syote())

    def kumoa(self):
        self.sovelluslogiikka.aseta_arvo(self.tmp)

class Nollaus:
    def __init__(self, sovelluslogiikka):
        self.sovelluslogiikka = sovelluslogiikka

    def suorita(self):
        self.sovelluslogiikka.nollaa()

class Kumoa:
    def __init__(self, sovelluslogiikka,lue_komentoolio):
        self.komentoolio = lue_komentoolio()
        
        self.sovelluslogiikka = sovelluslogiikka

    def suorita(self):
        self.komentoolio.kumoa()

class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self.arvot = []
        self._komennot = {
            Komento.SUMMA: Summa(sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(sovelluslogiikka,self._lue_syote),
            Komento.NOLLAUS: Nollaus(sovelluslogiikka)
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        return int(self._syote_kentta.get())

    def _suorita_komento(self, komento):
        self._komennot[komento].suorita()

        if not self.arvot:
            self._kumoa_painike["state"] = constants.DISABLED
        else:
            self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())
