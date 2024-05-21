from app.Model.Address import Address

class Owner:
    def __init__(self, db):
        self.db = db
        self.owner_id = -1 # Default value - not logged in

    def login(self) -> int:
        owner_id = 0
        valid = False
        while not valid:
            f_name = input("First name: ")
            l_name = input("Last name: ")

            if self.db.check_owner(l_name, f_name):
                owner_id = self.db.get_owner_id(l_name, f_name)[0]
                print(f"Welcome back {f_name} {l_name}! Your id is {owner_id}")
                valid = True
            else: 
                print(f"Owner {f_name} {l_name} not found")
        return owner_id
        
    def register(self) -> int:
        f_name = input("First name: ")
        l_name = input("Last name: ")
        street = input("Street: ")
        number = int(input("Number: "))
        city = input("City: ")
        country = input("Country: ")
        zip = int(input("Zip code: "))
        address = Address(city, street, country, number, zip)

        owner_id = 0

        if self.db.check_owner(l_name, f_name):
            print("Owner already exists")
            return -1
        else:
            self.db.create_owner(l_name, f_name, address).commit()
            owner_id = self.db.get_user_id(l_name, f_name)[0]
        print(f"Welcome {f_name} {l_name}! Your id is {owner_id}")
        return owner_id

    def run(self):
        print("Would you like to login or register?")
        valid = False
        while not valid:
            option = input("Login or Register? (l/r):")

            if option == "l":
                self.owner_id = self.login()
                if self.owner_id == -1:
                    valid = False
                else:
                    valid = True
            elif option == "r":
                self.owner_id = self.register()
                if self.owner_id == -1:
                    valid = False
                else:
                    valid = True
            else:
                print("Invalid option")
                valid = False
        
        leaved = False
        while not leaved:
            print("What would you like to do?")
            print("1. Add a restaurant")
            print("2. Add a dish")
            print("3. See Reviews")
            print("4. Leave")
            option = input("Option: ")
            if option == "1":
                pass
            elif option == "2":
                pass
            elif option == "3":
                pass
            else:
                print("Invalid option")
                leaved = False