from app.Model.Address import Address
from app.db import Database

class User:
    def __init__(self, db: Database):
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
        print("Would you like to login or register?")
        valid = False
        while not valid:
            option = input("Login or Register? (l/r):")

            if option == "l":
                self.login()
                valid = True
            elif option == "r":
                self.register()
                valid = True
            else:
                print("Invalid option")
                valid = False

        leaved = False
        while not leaved:
            print("What would you like to do? ")
            print("1. Search a restaurant")
            print("2. Review a restaurant")
            print("3. See your reviews")
            print("4. Leave")
