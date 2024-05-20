import os
from datetime import datetime
from abc import ABC, abstractmethod


class Idointervallum:
    def __init__(self, kezdet, veg):
        self.kezdet = kezdet
        self.veg = veg

    def __str__(self):
        return f"{self.kezdet}/{self.veg}"

    def metszi(self, masik_intervallum):
        return self.kezdet <= masik_intervallum.veg and self.veg >= masik_intervallum.kezdet

    def hossza_napokban(self):
        return (self.veg - self.kezdet).days


class Szoba(ABC):
    def __init__(self, szam, ar_per_nap):

        self.szam = szam
        self.ar_per_nap = ar_per_nap
        self.lefoglalt = []
        self.beolv()

    def beolv(self):
        h1 = []
        h2 = None
        h3 = None

        filename = (str(self.szam) + '_reservations.txt')
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('')

        with (open(filename, 'r') as file):
            sorok = file.readlines()
            for sor in sorok:
                sor = sor.strip()
                parts = sor.split(',')
                erkezes_str = parts[0].split(': ')[1].strip("'")
                tavozas_str = parts[1].split(': ')[1].strip("'")
                erkezes = datetime.strptime(erkezes_str, '%Y-%m-%d %H:%M:%S')
                tavozas = datetime.strptime(tavozas_str, '%Y-%m-%d %H:%M:%S')
                self.lefoglalt.append(Idointervallum(erkezes, tavozas))

    def elerheto_szobak(self, erk, tav, ):
        atfedes = False
        for foglalasok in self.lefoglalt:
            if foglalasok.metszi(Idointervallum(erk, tav)):
                atfedes = True
        return not atfedes

    def book(self, erk, tav):
        if self.elerheto_szobak(erk, tav, ):
            with open(str(self.szam) + '_reservations.txt', 'a') as file:
                file.write(f"'Erkezes': {erk}, 'Tavozas': {tav}\n")
            self.lefoglalt.append(Idointervallum(erk, tav))

            return f"A(z) {self.szam}. Szoba foglalása sikeres a {erk.strftime('%Y-%m.%d')} - {tav.strftime('%Y-%m-%d')} Fizetendő összeg:{Idointervallum(erk, tav).hossza_napokban() * self.ar_per_nap} JMF."
        else:
            print(f"A(z) {self.szam}. Szoba foglalása nem lehetséges, mert már foglalt.")
            return True

    def foglalas_lemond(self, kezd):
        for foglalas in self.lefoglalt:
            if foglalas.kezdet == kezd:
                self.lefoglalt.remove(foglalas)
                with open(str(self.szam) + '_reservations.txt', 'w') as file:
                    for foglalas in self.lefoglalt:
                        file.write(f"'Erkezes': {foglalas.kezdet}, 'Tavozas': {foglalas.veg}\n")
                return True

    def foglalt_datumok(self):
        return ', '.join([str(intervallum) for intervallum in self.lefoglalt])

    @abstractmethod
    def __str__(self):
        pass


class Egyagyas_Szoba(Szoba):
    def __str__(self):
        if not szalloda.adat == 'Foglalások':
            return f"Egyágyass szoba. Szoba száma: {self.szam}, Ár: {self.ar_per_nap}/nap"
        else:
            lefoglalt_str = self.foglalt_datumok()
            return f"Egyágyass szoba. Szoba száma: {self.szam}, Foglalások: {lefoglalt_str if lefoglalt_str else 'Nincs foglalás erre a szobára'}"


class Ketagyas_Szoba(Szoba):
    def __str__(self):
        if not szalloda.adat == 'Foglalások':
            return f"Ketágyass szoba. Szoba száma: {self.szam}, Ár: {self.ar_per_nap}/nap"
        else:
            lefoglalt_str = self.foglalt_datumok()
            return f"Kétágyas szoba. Szoba száma: {self.szam}, Foglalások: {lefoglalt_str if lefoglalt_str else 'Nincs foglalás erre a szobára'}"


class Lakosztaly(Szoba):
    def __str__(self):
        if not szalloda.adat == 'Foglalások':
            return f"Lakosztály szoba. Szoba száma: {self.szam}, Ár: {self.ar_per_nap}/nap"
        else:
            lefoglalt_str = self.foglalt_datumok()
            return f"Lakosztály szoba. Szoba száma: {self.szam}, Foglalások: {lefoglalt_str if lefoglalt_str else 'Nincs foglalás erre a szobára'}"


class Szalloda:
    def __init__(self):
        self.szobak = []
        self.lefoglalt_szobak = []
        self.adat = ''

    def szoba_hozzad(self, szoba: Szoba):
        if not self.adat == 'Foglalások':
            self.szobak.append(szoba)
        else:
            self.lefoglalt_szobak.append(szoba)

    def room_datas(self, adat):
        self.adat = adat
        self.szoba_hozzad(Egyagyas_Szoba(101, 12000, ))
        self.szoba_hozzad(Ketagyas_Szoba(102, 20000, ))
        self.szoba_hozzad(Lakosztaly(103, 35000, ))

    def szoba_foglal(self, szam, erk, tav):

        for szoba in self.szobak:
            if szoba.szam == szam:
                return szoba.book(erk, tav)
        else:
            print("A megadott szobaszám nem létezik vagy már foglalt.")
            return False

    def szoba_lemond(self, szam, erk, ):

        for szobak in self.szobak:
            if szobak.szam == szam:
                return szobak.foglalas_lemond(erk)
        else:
            print("Nem létezik ilyen foglalás")
            return False

    def elerheto_szobak(self):

        return "\n".join(str(szobak) for szobak in self.szobak)

    def foglalasok(self):

        return "\n".join(str(szobak) for szobak in self.lefoglalt_szobak)

    def foglalas_adatok(self):

        erk_str = input("Kérem adja meg az érkezés dátumát (éééé-hh-nn)")
        tav_str = input("Kérem adja meg a távozás időpontját (éééé-hh-nn)")
        number = int(input("Adja meg a kért szoba számát!"))
        erk = datetime.strptime(erk_str, '%Y-%m-%d')
        tav = datetime.strptime(tav_str, '%Y-%m-%d')
        print(szalloda.szoba_foglal(number, erk, tav))
        return

    def lemondas_adatok(self):
        erk_str = input("Kérem adja meg az érkezés dátumát (éééé-hh-nn)")
        number = int(input("Adja meg a kért szoba számát!"))
        erk = datetime.strptime(erk_str, '%Y-%m-%d')
        print(szalloda.szoba_lemond(number, erk))
        return


def szoba_foglalas(szalloda: Szalloda):
    while True:
        adat = input("Miben segíthetük?(Szobák/Foglalás/Foglalások/Mégsem)")
        if adat == "Szobák":
            szalloda.room_datas(adat)
            print(szalloda.elerheto_szobak())
            szalloda.szobak = []
        elif adat == "Foglalás":
            szalloda.room_datas(adat)
            szalloda.foglalas_adatok()
        elif adat == "Foglalások":
            szalloda.room_datas(adat)
            print(szalloda.foglalasok())
        elif adat == "Mégsem":
            print("Viszont látásra!")
            break
        elif adat == 'Lemondás':
            szalloda.room_datas(adat)
            szalloda.lemondas_adatok()
            print('Foglalás sikeresen lemondva')
        else:
            print("Nem megfelelő adat!")


adat = ''
szalloda = Szalloda()
szoba_foglalas(szalloda)
