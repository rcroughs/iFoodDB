from app.Model.Address import Address
from app.db import Database
from app.Model.Restaurant import Restaurant
from app.Model.PriceRange import PriceRange
from app.Model.Menu import Menu
from app.os import clear


class Owner:
    def __init__(self, db):
        self.db: Database = db
        self.owner_id = -1  # Default value - not logged in

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

    def add_restaurant(self):
        print("🏪 Add a restaurant")
        print("-" * 50)
        try:
            restaurant_name = input("Restaurant name: ")
            zip_code = int(input("Zip code: "))

            if self.db.restaurant_exists(restaurant_name, zip_code):
                print("Restaurant already exists. Adding you as an owner.")
                restaurant_id = self.db.get_restaurant_id(restaurant_name)[0]
                owner_id = self.register()
                if owner_id != -1:
                    self.db.add_owns(owner_id, restaurant_id).commit()
                    print(f"You have been added as an owner of {restaurant_name}.")
                return
            else:
                print(
                    "Restaurant does not exist. Please provide the following details to create it."
                )

                street = input("Street: ")
                number = int(input("Number: "))
                city = input("City: ")
                country = input("Country: ")

                delivery = input("Delivery (yes/no): ").lower() == "yes"

                opening_time = int(input("Opening time (HH): "))
                closing_time = int(input("Closing time (HH): "))
                price_range = int(
                    input("Price range: ( 1 - Low,  2 - Medium, 3 - High)")
                )
                food_type = input("Food type: ")

                address = Address(city, street, country, number, zip_code)

                if self.owner_id != -1:
                    restaurant = Restaurant(
                        name=restaurant_name,
                        address=address,
                        type=food_type,
                        evaluation=0,
                        delivery=delivery,
                        menu=Menu(),
                        opening=opening_time,
                        closing=closing_time,
                        price_range=PriceRange(price_range),
                    )
                    restaurant_id = self.db.add_restaurant(restaurant)[0]
                    self.db.add_owns(self.owner_id, restaurant_id).commit()
                    print(
                        f"{restaurant_name} has been created and you have been added as an owner."
                    )
        except Exception as e:
            print(e)
            print("\nThere was an error creating the restaurant, please try again\n")
            self.add_restaurant()
        input("Press enter to continue")

    def add_dish(self):
        print("🍽️ Add a dish")
        print("-" * 50)
        restaurants = self.db.get_owner_restaurants(self.owner_id)
        print("Which restaurant would you like to add a dish to?")
        for i, restaurant in enumerate(restaurants):
            print(f"{i+1}. {self.db.get_restaurant_name(restaurant[0])}")
        valid = False
        optionrest = 0
        while not valid:
            optionrest = input("Option: ")
            if optionrest.isdigit():
                optionrest = int(optionrest)
                if optionrest < 1 or optionrest > len(restaurants):
                    print("Invalid option")
                    valid = False
                else:
                    valid = True
            else:
                print("Invalid option")
                valid = False
        restaurant_id = restaurants[optionrest - 1][0]
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
                inp.append(allergens[int(option) - 1][0])
            else:
                print("Invalid option")
                valid = False

        for allergen_id in inp:
            self.db.add_dish_allergen(dish_id, allergen_id)

        self.db.commit()
        input("Dish added successfully. Press enter to continue")

    def remove_dish(self):
        print("🗑 Remove a dish")
        print("-" * 50)
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
        restaurant_id = restaurants[optionrest - 1][0]
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
        dish_id = dishes[optiondish - 1][0]
        self.db.remove_dish(dish_id)
        self.db.commit()
        input("Dish removed successfully. Press enter to continue")

    def see_menus(self):
        print("📜 See all your menus")
        print("-" * 50)
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
        restaurant_id = restaurants[optionrest - 1][0]
        menu_id = self.db.get_menu_id(restaurant_id)
        dishes = self.db.get_dishes(menu_id)
        print()
        print(f"Menu of {self.db.get_restaurant_name(restaurant_id)}")
        print("Dishes:")
        for dish in dishes:
            print(f"➡️ {dish[2]}: {dish[3]}€")

            allergens = self.db.get_allergens(dish[0])
            print(
                f"⚠️ {', '.join([self.db.get_allergen_name(allergen[1]) for allergen in allergens])}"
            )

        input("Press enter to continue")

    def print_review(self, review):
        user = self.db.get_user(review[1])
        print(f"👤 {user[1]} {user[2]} on {review[3]} with {review[5]} stars")
        print(review[4])
        print("Took:")
        dishes_id = self.db.get_dishes_id_from_review(review[0])
        for dish_id in dishes_id:
            dish = self.db.get_dish_name(dish_id[0])
            print(f"➡️ {dish}")

        print("-" * 50)

    def see_reviews(self):
        print("🌟 See all your reviews")
        print("-" * 50)
        restaurants = self.db.get_owner_restaurants(self.owner_id)
        print("Which restaurant would you like to see the reviews of?")
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
        restaurant_id = restaurants[optionrest - 1][0]
        reviews = self.db.get_restaurant_reviews(restaurant_id)
        print()
        print(f"Reviews of {self.db.get_restaurant_name(restaurant_id)}")
        for review in reviews:
            self.print_review(review)
        input("Press enter to continue")

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
            clear()
            print("📖 Owner Menu")
            print("-" * 50)
            print("What would you like to do?")
            print("1. Add a restaurant")
            print("2. See your menus")
            print("3. Add a dish")
            print("4. Remove a dish")
            print("5. See Reviews")
            print("6. Leave")
            option = input("Option: ")
            clear()
            if option == "1":
                self.add_restaurant()
            elif option == "2":
                self.see_menus()
            elif option == "3":
                self.add_dish()
            elif option == "4":
                self.remove_dish()
            elif option == "5":
                self.see_reviews()
            elif option == "6":
                leaved = True
            else:
                print("Invalid option")
                leaved = False
