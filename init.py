'''
Script to initialize the data in the database from the XML file
'''

from app.extractor import Extractor
from app.db import Database

def main():
    ext = Extractor()
    db = Database()

    db.connect()
    db.create_tables("sql/create_tables.sql");

    restaurants = ext.extract_restaurants("data/restos.xml")
    allergens = set()
    for restaurant in restaurants:
        allergens.update(restaurant.get_all_allergens())
    
    for allergen in allergens:
        db.add_allergen(allergen)

    db.commit()

    for restaurant in restaurants:
        db.add_restaurant(restaurant)

    users = ext.extract_users("data/customers.json")
    for user in users:
        db.add_user(user)

    db.commit()
    
    owner = ext.extract_owners("data/restaurateur.json")
    for user in owner:
        db.add_user(user)
    
    db.commit()

    mods = ext.extract_mods("data/moderators.json")
    for user in mods:
        db.add_user(user)
    
    db.commit()

    comments = ext.extract_comments("data/valid_comments.tsv")
    for comment in comments:
        db.add_comment(comment)

    db.commit()
    db.close()

if __name__ == '__main__':
    main()