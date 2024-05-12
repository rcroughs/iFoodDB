import xml.etree.ElementTree as ET
from app.Model.Address import Address
from app.Model.Dish import Dish
from app.Model.Menu import Menu
from app.Model.PriceRange import PriceRange
from app.Model.Restaurant import Restaurant

class Extractor:
    def extract_restaurants(self, xml_path: str) -> list[Restaurant]:
        res = []
        with open(xml_path, 'r') as file:
            data = file.read()
            xml = ET.fromstring(data)
            for restaurant in xml:
                res.append(self.extract_restaurant(restaurant))

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
        print(address)
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