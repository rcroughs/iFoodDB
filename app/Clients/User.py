from app.Model.Address import Address
from app.db import Database
from app.Model.Recommendation import Recommendation
from datetime import date


class User:
    def __init__(self, db: Database):
        self.db = db
        self.client_id = -1 # Default value - not logged in

    def login(self) -> int:
        client_id = 0
        valid = False
        while not valid:
            f_name = input("First name: ")
            l_name = input("Last name: ")

            if self.db.check_user(l_name, f_name):
                client_id = self.db.get_user_id(l_name, f_name)[0]
                print(f"Welcome back {f_name} {l_name}! Your id is {client_id}")
                valid = True
            else: 
                print(f"User {f_name} {l_name} not found")
        return client_id

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

    def leave_review(self):
        # ID du client
        id_client = self.client_id
        
        # ID du restaurant
        restaurant_id = 0

        restaurant_input = input("Nom du restaurant : ")
        restaurant_data = self.db.search_restaurant(restaurant_input.strip())
        
        valid_restaurant = False

        while not valid_restaurant:

            if len(restaurant_data) == 1 and restaurant_input != restaurant_data[0].name():
                answer = input(f"This restaurant doesn't exist, did you mean '{restaurant_data[0].name()}' ? (y/n) ")
                if answer.lower() in ["yes", "y", "ye", "yea"]:
                    restaurant_id = restaurant_data[0].id()
                    valid_restaurant = True
                else:   
                    restaurant_input = input("Nom du restaurant : ")
                    restaurant_data = self.db.search_restaurant(restaurant_input.strip())
            elif len(restaurant_data) == 1 and restaurant_input == restaurant_data[0].name():
                restaurant_id = restaurant_data[0].id()
                valid_restaurant = True     
            else:
                restaurant_input = input("Restaurant introuvable, veuillez entrer un nom valide : ")
                restaurant_data = self.db.search_restaurant(restaurant_input.strip())

        # Début du repas
        opening = restaurant_data[0].opening()
        closing = restaurant_data[0].closing()
        begin = input(f"Please indicate the start time of the meal ({opening} - {closing}): ")
        begin_valid = False

        while not begin_valid:
            try:
                begin = int(begin)
                # Plage horaire normale
                if opening <= closing:
                    if opening <= begin < closing:
                        begin_valid = True
                # Plage dépassant sur la nuit        
                elif closing < opening:
                    if begin >= opening or begin < closing:
                        begin_valid = True       
                if not begin_valid:
                    begin = input(f"Not in opening hours. Please enter a value ({opening} - {closing}): ")

            except ValueError:
                begin = input(f"Incorrect value. Please enter a number ({opening} - {closing}): ")
        
        # Fin du repas
        end = input(f"Please indicate the finish time of the meal ({begin + 1} - {closing}): ")
        end_valid = False

        while not end_valid:
            try:
                end = int(end)
                # Plage horaire normale
                if opening <= closing:
                    if (opening < end <= closing) and (end > begin):
                        end_valid = True
                # Plage dépassant sur la nuit        
                elif closing < opening:
                    if (end <= closing < begin):
                        end_valid = True
                    elif (opening < end <= closing) and (end > begin):
                        end_valid = True    
                             
                if not end_valid:
                    end = input(f"Incorrect value. Please enter a value ({begin + 1} - {closing}): ")                 

            except ValueError:
                end = input(f"Incorrect value. Please enter a number ({begin + 1} - {closing}): ")
        
        # Plats commandés
        menu = restaurant_data[0].menu() # Attention, ne renvoie pas un objet Menu mais bien un int étant l'id du menu
        dishes = [dish[2] for dish in self.db.get_dishes(menu)]
        
        print("Menu reminder : ")
        counter = 1
        for dish in dishes:
            print(counter, end="")
            print('.', dish) 
            counter += 1

        eaten_dishes = []

        user_input = input("(1) Add a dish\n(2) Stop here\n")
        
        while user_input != '2':
            if user_input.strip() not in ['1', '2']:
                user_input = input("Invalid option. Enter a valid number : ")
            else:
                if user_input == '1':
                    dish_input = input("Enter a dish name : ") 
                    dish_input = dish_input.strip()

                    if dish_input not in dishes:
                        print("This dish doesn't exist in this establishment")   
                    else:
                        eaten_dishes.append(dish_input)
                        user_input = input("(1) Add a dish\n(2) Stop here\n")
        
        # Prix du repas
        price = input("Total cost of the meal : ")
        price_valid = False

        while not price_valid:
            try:
                price = int(price)
                if price > 1:
                    price_valid = True
                else:
                    price = input("Please enter a valid number : ")    
            except ValueError:
                price = input("Not valid. Please enter a number : ")

        # Commentaire
        comment = input("Please enter a comment about your meal (max. 4096 char.): ")

        # Recommendation
        appreciation = input("Would you recommend this place ?\n(1) Yes, I would recommend this place.\n" \
                             "(2) No. I would not recommend this place.\n(3) Avoid this place at all costs!\n")
        appreciation_valid = False

        while not appreciation_valid:
            if appreciation == "1" or appreciation == "2" or appreciation == "3":
                appreciation_valid = True
                if appreciation == "1":
                    appreciation = Recommendation.RECOMMENDED
                elif appreciation == "2":
                    appreciation = Recommendation.NOT_RECOMMENDED
                else:
                    appreciation = Recommendation.TO_BE_AVOIDED
            else:
                appreciation = input("Invalid option. Would you recommend this place ?\n(1) Yes, I would recommend this place." \
                                     "\n(2) No. I would not recommend this place\n(3) Avoid this place at all costs!\n")

        # Notes 
        user_input = input("Were you there in person or did you order (1-2) ? ")
        
        input_valid = False
        physical_note = 0
        delivery_note = 0
        while not input_valid:
            if user_input == "1":
               
                physical_note = int(input("What would you rate the quality of service and the reception ? (1-5) "))
                while not (1 <= physical_note <= 5):
                     physical_note = int(input("Invalid value. What would you rate the quality of service and the reception ? (1-5) "))
                input_valid = True     
            elif user_input == "2":
                delivery_note = int(input("What would you rate the delivery ? (1-5) "))
                while not (1 <= delivery_note <= 5):
                    delivery_note = input("Invalid value. What would you rate the delivery ? (1-5) ")
                input_valid = True
            else:
                user_input = int(input("Invalid option. Were you there in person or did you order (1-2) ? "))
        
        # Note finale
        global_note = input("Finally, indicate your global rating for this establishment (1-5) : ")

        valid_note = False
        
        while not valid_note:
            try:
                global_note = int(global_note)
                if (1 <= global_note <= 5):
                    valid_note = True
                else:
                    input("Invalid number. Indicate your global rating for this establishment (1-5) : ")
            except ValueError:
                global_note = input("Invalid value. Indicate your global rating for this establishment (1-5) : ")

        # Date de la review
        current_date = date.today()
        current_date = str(current_date)
        
        # Requête en DB
        self.db.add_review(restaurant_id, id_client, global_note, comment, appreciation, eaten_dishes, price, begin, end, current_date, physical_note, delivery_note)
        self.db.commit()
 

    def get_all_reviews(self):
        reviews = self.db.get_user_reviews(self.client_id)
        
        reviews_counter = 1

        for review in reviews:
            print(f"| Review number {reviews_counter} :")
            print("╪ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ╪")
            print(f"| Review ID : {review[0]}")
            print(f"| User ID : {review[1]}")
            print(f"| Restaurant ID : {review[2]}")
            print(f"| Rating date : {review[3]}")
            print(f"| Comment : {review[4]}")
            print(f"| Global rating : {review[5]}")
            appreciation = "Recommanded" if review[6] == 3 else "Not recommanded" if review[6] == 2 else "To avoid"
            print(f"| Appreciation : {appreciation}")
            print(f"| Delivery note (0 if none) : {review[7]}")
            print(f"| Physical note (0 if none) : {review[8]}")
            print(f"| Start-end of the meal : {review[9]}-{review[10]}")
            print(f"| Total price : {review[11]}")
            print("╪ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ┅ ╪")

            reviews_counter += 1



            


    def run(self):
        print("Would you like to login or register?")
        valid = False
        while not valid:
            option = input("Login or Register? (l/r):")

            if option == "l":
                self.client_id = self.login()
                valid = True
            elif option == "r":
                self.client_id = self.register()
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
            option = input("Option: ")
            if option == "1":
                pass
            elif option == "2":
                self.leave_review()
            elif option == "3":
                self.get_all_reviews()
            else:
                print("Invalid option")
                leaved = False
