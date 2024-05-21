'''
Script to initialize the data in the database from the XML file
'''

from app.extractor import Extractor
from app.db import Database
from tqdm import tqdm

def main():
    ext = Extractor()
    db = Database()

    db.connect()
    db.create_tables("sql/create_tables.sql");

    restaurants = ext.extract_restaurants("data/restos.xml")
    allergens = set()
    for restaurant in tqdm(restaurants, desc="🧪 Extracting allergens", total=len(restaurants)):
        allergens.update(restaurant.get_all_allergens())
    
    for allergen in tqdm(allergens, desc="🧪 Adding allergens", total=len(allergens)):
        db.add_allergen(allergen)

    db.commit()

    for restaurant in tqdm(restaurants, desc="🍽️ Extracting restaurants", total=len(restaurants)):
        db.add_restaurant(restaurant)

    users = ext.extract_users("data/customers.json")
    for user in tqdm(users, desc="👤 Extracting users", total=len(users)):
        db.add_user(user)

    db.commit()
    
    owner = ext.extract_owners("data/restaurateur.json")
    for user in tqdm(owner, desc="👩‍🍳 Extracting owners", total=len(owner)):
        db.add_user(user)
    
    db.commit()

    mods = ext.extract_mods("data/moderators.json")
    for user in tqdm(mods, desc="🛡️ Extracting moderators", total=len(mods)):
        db.add_user(user)
    
    db.commit()

    comments = ext.extract_comments("data/valid_comments.tsv")
    for comment in tqdm(comments, desc="💬 Extracting comments", total=len(comments)):
        db.add_comment(comment)

    db.commit()

    deleted_comments = ext.extract_deleted_comments("data/removed_comments.tsv")
    for comment in tqdm(deleted_comments, desc="🗑️ Extracting deleted comments", total=len(deleted_comments)):
        db.delete_comment(comment)

    db.commit()
    db.close()

if __name__ == '__main__':
    main()