from app.Model.Address import Address
from app.db import Database
from app.Clients.User import User
from app.Clients.Owner import Owner

class Client:
    """
    Client class to interact with the server
    """

    def __init__(self, db):
        self.db = db

    def login(self) -> int:
        f_name = input("First name: ")
        l_name = input("Last name: ")

        if self.db.check_user(l_name, f_name):
            client_id = self.db.get_user_id(l_name, f_name)[0]
            print(f"Welcome back {f_name} {l_name}! Your id is {client_id}")
            return client_id
        else: 
            print(f"User {f_name} {l_name} not found")
            return -1

    def register(self) -> int:
        f_name = input("First name: ")
        l_name = input("Last name: ")
        street = input("Street: ")
        number = int(input("Number: "))
        city = input("City: ")
        country = input("Country: ")
        zip = int(input("Zip code: "))
        address = Address(city, street, country, number, zip)

        client_id = 0

        if self.db.check_user(l_name, f_name):
            client_id = self.db.get_user_id(l_name, f_name)[0]
        else:
            self.db.create_user(l_name, f_name, address).commit()
            client_id = self.db.get_user_id(l_name, f_name)[0]
        print(f"Welcome {f_name} {l_name}! Your id is {client_id}")
        return client_id

    def run(self):
        print("Welcome to iFood!")
        valid = False
        while not valid:
            option = input("Are you a user or an owner? (u/o):")

            if option == "u":
                User(self.db).run()
                valid = True
            else:
                Owner(self.db).run()
                valid = True

