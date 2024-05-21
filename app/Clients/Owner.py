from app.Model.Address import Address
from app.db import Database

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
                owner_id = self.db.get_user_id(l_name, f_name)[0]
                if self.db.is_owner(owner_id):
                    print(f"Welcome back {f_name} {l_name}! Your id is {owner_id}")
                    valid = True
                else:
                    print(f"{f_name} {l_name} is not an owner")
                    valid = False
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
    
    def add_dish(self):
        restaurants = self.db.get_owner_restaurants(self.owner_id)
        print("Which restaurant would you like to add a dish to?")
        for i, restaurant in enumerate(restaurants):
            print(f"{i+1}. {self.db.get_restaurant_name(restaurant[0])}")
        valid = False
        optionrest = 0
        while not valid:
            optionrest = int(input("Option: "))
            if optionrest < 1 or optionrest > len(restaurants):
                print("Invalid option")
                valid = False
            else:
                valid = True
        restaurant_id = restaurants[optionrest-1][0]
        menu_id = self.db.get_menu_id(restaurant_id)
        dish_name = input("Dish name: ")
        price = float(input("Price: "))
        dish_id = self.db.add_dish(menu_id, dish_name, price)
        print("Would you like to inform of any allergens ?")
        allergens = self.db.get_all_allergens()
        for i, allergen in enumerate(allergens):
            print(f"{i+1}. {allergen[1]}")

        print("Press N to add a new allergen")
        print("Press enter to finish")
        valid = False
        inp = []
        while not valid:
            option = input("Option: ")
            if option == "":
                valid = True
            elif option == "N":
                allergen_name = input("Allergen name: ")
                allergen_id = self.db.add_allergen(allergen_name)
                self.db.commit()
                inp.append(allergen_id)
            elif option.isdigit() and int(option) <= len(allergens):
                inp.append(allergens[int(option)-1][0])
            else:
                print("Invalid option")
                valid = False

        for allergen_id in inp:
            self.db.add_dish_allergen(allergen_id, dish_id)

        self.db.commit()
        print("Dish added successfully")

    def remove_dish(self):
        restaurants = self.db.get_owner_restaurants(self.owner_id)
        print("Which restaurant would you like to remove a dish from?")
        for i, restaurant in enumerate(restaurants):
            print(f"{i+1}. {self.db.get_restaurant_name(restaurant[0])}")
        valid = False
        optionrest = 0
        while not valid:
            optionrest = int(input("Option: "))
            if optionrest < 1 or optionrest > len(restaurants):
                print("Invalid option")
                valid = False
            else:
                valid = True
        restaurant_id = restaurants[optionrest-1][0]
        menu_id = self.db.get_menu_id(restaurant_id)
        dishes = self.db.get_dishes(menu_id)
        print("Which dish would you like to remove?")
        for i, dish in enumerate(dishes):
            print(f"{i+1}. {dish[2]}")
        valid = False
        optiondish = 0
        while not valid:
            optiondish = int(input("Option: "))
            if optiondish < 1 or optiondish > len(dishes):
                print("Invalid option")
                valid = False
            else:
                valid = True
        dish_id = dishes[optiondish-1][0]
        self.db.remove_dish(dish_id)
        self.db.commit()
        print("Dish removed successfully")

    def see_menus(self):
        restaurants = self.db.get_owner_restaurants(self.owner_id)
        print("Which restaurant would you like to see the menu of?")
        for i, restaurant in enumerate(restaurants):
            print(f"{i+1}. {self.db.get_restaurant_name(restaurant[0])}")
        valid = False
        optionrest = 0
        while not valid:
            optionrest = int(input("Option: "))
            if optionrest < 1 or optionrest > len(restaurants):
                print("Invalid option")
                valid = False
            else:
                valid = True
        restaurant_id = restaurants[optionrest-1][0]
        menu_id = self.db.get_menu_id(restaurant_id)
        dishes = self.db.get_dishes(menu_id)
        print()
        print(f"Menu of {self.db.get_restaurant_name(restaurant_id)}")
        print("Dishes:")
        for dish in dishes:
            print(f"➡️ {dish[2]}: {dish[3]}€")

            allergens = self.db.get_allergens(dish[0])
            print(f"⚠️ {', '.join([self.db.get_allergen_name(allergen[1]) for allergen in allergens])}")

        print()

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
            print("2. See your menus")
            print("3. Add a dish")
            print("4. Remove a dish")
            print("5. See Reviews")
            print("6. Leave")
            option = input("Option: ")
            if option == "1":
                pass
            elif option == "2":
                self.see_menus()
            elif option == "3":
                self.add_dish()
            elif option == "4":
                self.remove_dish()
            elif option == "5":
                pass 
            elif option == "6":
                leaved = True
            else:
                print("Invalid option")
                leaved = False