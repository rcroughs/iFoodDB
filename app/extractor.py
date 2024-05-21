import xml.etree.ElementTree as ET
import csv
import json
from app.Model.Address import Address
from app.Model.Dish import Dish
from app.Model.Menu import Menu
from app.Model.PriceRange import PriceRange
from app.Model.Restaurant import Restaurant
from app.Model.User import User
from app.Model.Comment import Comment
from app.Model.Recommendation import Recommendation
from app.Model.DeletedComment import DeletedComment

class Extractor:
    def extract_restaurants(self, xml_path: str) -> list[Restaurant]:
        res = []
        with open(xml_path, 'r') as file:
            data = file.read()
            xml = ET.fromstring(data)
            for restaurant in xml:
                res.append(self.extract_restaurant(restaurant))

        return res

    def extract_users(self, json_path: str) -> list[User]:
        res = []
        with open(json_path, 'r') as file:
            data = file.read()
            jsons = json.loads(data)
            for user in jsons:
                res.append(self.extract_user(user))

        return res

    def extract_owners(self, json_path: str) -> list[User]:
        res = []
        with open(json_path, 'r') as file:
            data = file.read()
            jsons = json.loads(data)
            for owner in jsons:
                res.append(self.extract_owner(owner))

        return res

    def extract_mods(self, json_path: str) -> list[User]:
        res = []
        with open(json_path, 'r') as file:
            data = file.read()
            jsons = json.loads(data)
            for mod in jsons:
                res.append(self.extract_user(mod))

        return res
    
    def extract_comments(self, tsv_path: str) -> list[Comment]:
        res = []
        with open(tsv_path, 'r') as file:
            tsv = csv.reader(file, delimiter='\t')
            next(tsv)
            for comment in tsv:
                res.append(self.extract_comment(comment))

        return res

    def extract_deleted_comments(self, tsv_path: str) -> list[DeletedComment]:
        res = []
        with open(tsv_path, 'r') as file:
            tsv = csv.reader(file, delimiter='\t')
            for comment in tsv:
                res.append(self.extract_deleted_comment(comment))

        return res

    def extract_restaurant(self, restaurant) -> Restaurant:
        name = restaurant.find('name').text
        address = self.extract_address(restaurant.find('address'))
        menu = self.extract_menu(restaurant.find('menu'))
        delivery = True if restaurant.find('delivery').text == "Yes" else False
        evaluation = float(restaurant.find('evaluation').text)
        opening = int(restaurant.find('opening_hours').find('opening').text)
        closing = int(restaurant.find('opening_hours').find('closing').text)
        price_range = restaurant.find('price_range').text
        if price_range == "bas":
            price_range = PriceRange.LOW
        elif price_range == "moyen":
            price_range = PriceRange.MEDIUM
        else:
            price_range = PriceRange.HIGH
        type = restaurant.find('type').text
        return Restaurant(name, address, delivery, evaluation, menu, opening, closing, price_range, type)

    def extract_address(self, address) -> Address:
        street = address.find('street').text
        number = int(address.find('number').text)
        city = address.find('city').text
        country = address.find('country').text
        zip_code = int(address.find('zipcode').text)
        return Address(city, street, country, number, zip_code)

    def extract_menu(self, menu) -> Menu:
        dishes = []
        for dish in menu:
            name = dish.find('name').text
            price = float(dish.find('price').text[:-1])
            allergens = self.extract_allergens(dish.find('allergens'))
            dishes.append(Dish(allergens, name, price))
        return Menu(dishes)

    def extract_allergens(self, allergens) -> list[str]:
        res = []
        for allergen in allergens:
            res.append(allergen.text)
        return res

    def extract_user(self, user) -> User:
        fname = user['firstname']
        lname = user['lastname']
        address = Address(user['address']['city'], user['address']['street'], user['address']['country'], user['address']['number'], user['address']['zipcode'])
        return User(lname, fname, address, False)
    
    def extract_owner(self, owner):
        fname = owner['firstname']
        lname = owner['lastname']
        address = Address(owner['address']['city'], owner['address']['street'], owner['address']['country'], owner['address']['number'], owner['address']['zipcode'])
        restaurants = [owner["restaurant"]]
        return User(lname, fname, address, True, restaurants)

    def extract_mod(self, mod):
        fname = mod['firstname']
        lname = mod['lastname']
        address = Address(mod['address']['city'], mod['address']['street'], mod['address']['country'], mod['address']['number'], mod['address']['zipcode'])
        return User(lname, fname, address, False).set_mod()

    def extract_comment(self, comment) -> Comment:
        com = comment[0]
        note = comment[1]
        date = comment[2]
        recommendation = 0
        if comment[3] == "recommandé":
            recommendation = Recommendation.RECOMMENDED
        elif comment[3] == "déconseillé":
            recommendation = Recommendation.NOT_RECOMMENDED
        elif comment[3] == "à éviter d'urgence":
            recommendation = Recommendation.TO_BE_AVOIDED
        else:
            print(comment[3])
        restaurant = comment[4]
        noteservice = None
        notedelivery = None
        if comment[5][0] == "H":
            noteservice = int(comment[5][-1])
        else :
            notedelivery = int(comment[5][-1])

        datecomm = comment[6]
        menu = comment[7].split(';')
        price = float(comment[8])
        begin = int(comment[9])
        end = int(comment[10])
        user = comment[11]
        return Comment(user, com, datecomm, restaurant, note, date, menu, price, begin, end, recommendation, noteservice, notedelivery)

    def extract_deleted_comment(self, deleted_comment) -> DeletedComment:
        comm = deleted_comment[0]
        note = deleted_comment[1]
        date = deleted_comment[2]
        recommendation = 0
        if deleted_comment[3] == "recommandé":
            recommendation = Recommendation.RECOMMENDED
        elif deleted_comment[3] == "déconseillé":
            recommendation = Recommendation.NOT_RECOMMENDED
        elif deleted_comment[3] == "à éviter d'urgence":
            recommendation = Recommendation.TO_BE_AVOIDED
        else:
            print(deleted_comment[3])

        restaurant = deleted_comment[4]
        noteservice = None
        notedelivery = None
        if deleted_comment[5][0] == "H":
            noteservice = int(deleted_comment[5][-1])
        else :
            notedelivery = int(deleted_comment[5][-1])
        
        datecomm = deleted_comment[6]
        menu = deleted_comment[7].split(';')
        price = float(deleted_comment[8])
        begin = int(deleted_comment[9])
        end = int(deleted_comment[10])
        user = deleted_comment[11]
        mod_comment = deleted_comment[12]
        return DeletedComment(user, comm, datecomm, restaurant, note, date, menu, price, begin, end, recommendation, noteservice, notedelivery, mod_comment, None)
