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


class Room(ABC):
    def __init__(self, number, price_per_night):

        self.number = number
        self.price_per_night = price_per_night
        self.reserved = []
        self.beolv()

    def beolv(self):
        h1 = []
        h2 = None
        h3 = None

        filename = (str(self.number) + '_reservations.txt')
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('')

        with (open(filename, 'r') as file):
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split(',')
                erkezes_str = parts[0].split(': ')[1].strip("'")
                tavozas_str = parts[1].split(': ')[1].strip("'")
                erkezes = datetime.strptime(erkezes_str, '%Y-%m-%d %H:%M:%S')
                tavozas = datetime.strptime(tavozas_str, '%Y-%m-%d %H:%M:%S')
                self.reserved.append(Idointervallum(erkezes, tavozas))

    def find_available_rooms(self, erk, tav, ):
        overlap = False
        for reservation in self.reserved:
            if reservation.metszi(Idointervallum(erk, tav)):
                overlap = True
        return not overlap

    def book(self, erk, tav):
        if self.find_available_rooms(erk, tav, ):
            with open(str(self.number) + '_reservations.txt', 'a') as file:
                file.write(f"'Erkezes': {erk}, 'Tavozas': {tav}\n")
            self.reserved.append(Idointervallum(erk, tav))

            return f"A(z) {self.number}. Szoba foglalása sikeres a {erk.strftime('%Y-%m.%d')} - {tav.strftime('%Y-%m-%d')} Fizetendő összeg:{Idointervallum(erk, tav).hossza_napokban() * self.price_per_night} JMF."
        else:
            print(f"A(z) {self.number}. Szoba foglalása nem lehetséges, mert már foglalt.")
            return True

    def foglalas_lemond(self, kezd):
        for reservation in self.reserved:
            if reservation.kezdet == kezd:
                self.reserved.remove(reservation)
                with open(str(self.number) + '_reservations.txt', 'w') as file:
                    for reservation in self.reserved:
                        file.write(f"'Erkezes': {reservation.kezdet}, 'Tavozas': {reservation.veg}\n")
                return True

    def reserved_dates(self):
        return ', '.join([str(intervallum) for intervallum in self.reserved])

    @abstractmethod
    def __str__(self):
        pass


class Singel_Bedroom(Room):
    def __str__(self):
        if not hotel.adat == 'Foglalások':
            return f"Egyágyass szoba. Szoba száma: {self.number}, Ár: {self.price_per_night}/nap"
        else:
            reserved_str = self.reserved_dates()
            return f"Egyágyass szoba. Szoba száma: {self.number}, Foglalások: {reserved_str if reserved_str else 'Nincs foglalás erre a szobára'}"


class Double_Bedroom(Room):
    def __str__(self):
        if not hotel.adat == 'Foglalások':
            return f"Ketágyass szoba. Szoba száma: {self.number}, Ár: {self.price_per_night}/nap"
        else:
            reserved_str = self.reserved_dates()
            return f"Kétágyas szoba. Szoba száma: {self.number}, Foglalások: {reserved_str if reserved_str else 'Nincs foglalás erre a szobára'}"


class Hotel:
    def __init__(self):
        self.rooms = []
        self.reserved_rooms = []
        self.adat = ''

    def add_room(self, room: Room):
        if not self.adat == 'Foglalások':
            self.rooms.append(room)
        else:
            self.reserved_rooms.append(room)

    def room_datas(self, adat):
        self.adat = adat
        self.add_room(Singel_Bedroom(101, 200, ))
        self.add_room(Double_Bedroom(102, 666, ))
        self.add_room(Double_Bedroom(103, 9999, ))

    def book_room(self, number, erk, tav):

        for room in self.rooms:
            if room.number == number:
                return room.book(erk, tav)
        else:
            print("A megadott szobaszám nem létezik vagy már foglalt.")
            return False

    def lemond_room(self, number, erk, ):

        for room in self.rooms:
            if room.number == number:
                return room.foglalas_lemond(erk, )
        else:
            print("Nem létezik ilyen foglalás")
            return False

    def available_rooms(self, ):

        return "\n".join(str(room) for room in self.rooms)

    def reservations(self, ):

        return "\n".join(str(room) for room in self.reserved_rooms)

    def input_booking(self):

        erk_str = input("Kérem adja meg az érkezés dátumát (éééé-hh-nn)")
        tav_str = input("Kérem adja meg a távozás időpontját (éééé-hh-nn)")
        number = int(input("Adja meg a kért szoba számát!"))
        erk = datetime.strptime(erk_str, '%Y-%m-%d')
        tav = datetime.strptime(tav_str, '%Y-%m-%d')
        print(hotel.book_room(number, erk, tav))
        return

    def input_lemondas(self):
        erk_str = input("Kérem adja meg az érkezés dátumát (éééé-hh-nn)")
        number = int(input("Adja meg a kért szoba számát!"))
        erk = datetime.strptime(erk_str, '%Y-%m-%d')
        print(hotel.lemond_room(number, erk))
        return


def room_booking(hotel: Hotel):
    while True:
        adat = input("Miben segíthetük?(Szobák/Foglalás/Foglalások/Mégsem)")
        if adat == "Szobák":
            hotel.room_datas(adat)
            print(hotel.available_rooms())
            hotel.rooms = []
        elif adat == "Foglalás":
            hotel.room_datas(adat)
            hotel.input_booking()
        elif adat == "Foglalások":
            hotel.room_datas(adat)
            print(hotel.reservations())
        elif adat == "Mégsem":
            print("Viszont látásra!")
            break
        elif adat == 'Lemondás':
            hotel.room_datas(adat)
            hotel.input_lemondas()
            print('Foglalás sikeresen lemondva')
        else:
            print("Nem megfelelő adat!")


adat = ''
hotel = Hotel()
room_booking(hotel)
