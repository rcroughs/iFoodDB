from app.Model.Address import Address
from app.db import Database
from app.Clients.User import User
from app.Clients.Owner import Owner
from app.os import clear, Colors


class Client:
    """
    Client class to interact with the server (CLI main class)
    """

    def __init__(self, db: Database):
        self.db = db

    def print_header(self):
        print(
            f" _______              _____________ \n(_)  ___|            | |  _  \ ___ \ \n _| |_ ___   ___   __| | | | | |_/ / \n| |  _/ _ \ / _ \ / _` | | | | ___ \ \n| | || (_) | (_) | (_| | |/ /| |_/ / \n|_\_| \___/ \___/ \__,_|___/ \____/"
            + Colors.gray("*Powered by PostgreSQL")
        )

    def try_requests(self):
        for i in range(1, 7):
            print(f"Request {i}: ", end="")
            with open(f"sql/request_{i}.sql") as f:
                print(f.readline()[2:].strip())

        valid = False
        while not valid:
            print("Which request do you want to try?")
            if (request := input("Request number:")) in ["1", "2", "3", "4", "5", "6"]:
                print(self.db.exec_file(f"sql/request_{request}.sql"))
                valid = True
            else:
                print("Invalid request number")

    def run(self):
        clear()
        self.print_header()
        valid = False
        while not valid:
            option = input(
                "Are you a user, an owner or just here to try the requests? (u/o/t):"
            )
            if option == "u":
                User(self.db).run()
                valid = True
            elif option == "o":
                Owner(self.db).run()
                valid = True
            elif option == "t":
                self.try_requests()
                valid = True
            else:
                print("Invalid option")
