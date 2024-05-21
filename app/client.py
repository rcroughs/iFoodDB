from app.Model.Address import Address
from app.db import Database
from app.Clients.User import User
from app.Clients.Owner import Owner

class Client:
    """
    Client class to interact with the server (CLI main class)
    """

    def __init__(self, db):
        self.db = db

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

