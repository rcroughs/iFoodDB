import psycopg2
from app.Model.PriceRange import PriceRange
from app.Model.Restaurant import Restaurant
from app.Model.Address import Address
from app.Model.Recommendation import Recommendation
from config import Config


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port="5432",
            client_encoding="utf-8"
        )
        self.cursor = self.connection.cursor()

    def create_tables(self, sql_file: str) -> None:
        with open(sql_file, 'r') as f:
            self.cursor.execute(f.read())
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query: str, args=None) -> int:
        if args is None:
            args = ()
        try:
            self.cursor.execute(query, args)
            # Get the returned id if any (using RETURNING id)
            if self.cursor.description:
                return self.cursor.fetchall()
        except Exception as e:
            # Rollback the transaction
            # self.connection.rollback()
            # Handle exceptions
            print(f"Error executing query: {e}")
            print(f"Query: {query}")
            print(f"Args: {args}")
            exit(1)
            return None
    
    def exec_file(self, file: str):
        res = ()
        with open(file, 'r') as f:
            res = self.cursor.execute(f.read())
        return res

    def select(self, table: str, columns: list, condition: str = None, args=None):
        if args is None:
            args = ()
        query = f"SELECT {', '.join(columns)} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def add_restaurant(self, restaurant: Restaurant) -> int:
        dishes_id = []
        for dishes in restaurant.menu():
            allergenes_id = []
            for allergenes in dishes.allergens():
                allergenes_id.append(self.select("allergenes", ["id"], "name = %s", (allergenes,))[0])
            dishes_id.append(
                self.execute(
                    "INSERT INTO plats (NAME, PRICE) VALUES (%s, %s) RETURNING id",
                    (dishes.name(), dishes.price())
                )
            )
            for allergene in allergenes_id:
                self.execute(
                    "INSERT INTO plats_allergenes (ID_PLAT, ID_ALLERGENE) VALUES (%s, %s)",
                    (dishes_id[-1][0], allergene[0])
                )

        menu_id = self.execute(
            "INSERT INTO menus DEFAULT VALUES RETURNING id")[0]

        # Update plats with menu_id
        for dish_id in dishes_id:
            self.execute(
                "UPDATE plats SET menu = %s WHERE id = %s",
                (menu_id, dish_id[0])
            )

        return self.execute(
            "INSERT INTO restaurants (NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, delivery, average_rating, menu, opening_time, closing_time, price_range, food_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (restaurant.name(), restaurant._address.street(), int(restaurant._address.number()), restaurant._address.city(), restaurant._address.zip_code(), restaurant._address.city(
            ), restaurant.delivery(), restaurant.evaluation(), menu_id, restaurant.opening(), restaurant.closing(), restaurant.price_range().int(), restaurant.type())
        )

    def add_allergen(self, allergen: str):
        self.execute(
            "INSERT INTO allergenes (NAME) VALUES (%s)",
            (allergen,)
        )
        return self

    def create_user(self, name: str, first_name: str, address: Address):
        self.execute(
            "INSERT INTO users (NAME, FIRST_NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, RESTAURANT_OWNER) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, first_name, address.street(), address.number(), address.city(), address.zip_code(), address.country(), False)
        )
        return self
    
    def get_user_id(self, name: str, first_name: str) -> int:
        self.cursor.execute(
            "SELECT ID FROM users WHERE NAME = %s AND FIRST_NAME = %s",
            (name, first_name)
        )
        return self.cursor.fetchone()

    def is_owner(self, client_id: int) -> bool:
        self.cursor.execute(
            "SELECT RESTAURANT_OWNER FROM users WHERE ID = %s",
            (client_id,)
        )
        return self.cursor.fetchone() is True

    def add_owns(self, client_id: int, restaurant_id: int):
        if (self.is_owner(client_id)):
            self.execute(
                "INSERT INTO owns (ID_CLIENT, ID_RESTAURANT) VALUES (%s, %s)",
                (client_id, restaurant_id)
            )
        return self

    def create_owner(self, name: str, first_name: str, address: Address):
        self.execute(
            "INSERT INTO users (NAME, FIRST_NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, RESTAURANT_OWNER) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, first_name, address.street(), address.number(), address.city(), address.zip_code(), address.country(), True)
        )
        return self

    def check_owner(self, name: str, first_name: str) -> bool:
        self.cursor.execute(
            "SELECT * FROM users WHERE NAME = %s AND FIRST_NAME = %s AND RESTAURANT_OWNER = TRUE",
            (name, first_name)
        )
        return self.cursor.fetchone() is not None

    def check_user(self, name: str, first_name: str) -> bool:
        self.cursor.execute(
            "SELECT * FROM users WHERE NAME = %s AND FIRST_NAME = %s AND RESTAURANT_OWNER = FALSE",
            (name, first_name)
        )
        return self.cursor.fetchone() is not None
    
    def is_mod(self, client_id) -> bool:
        self.cursor.execute(
            "SELECT * FROM moderators WHERE ID_CLIENT = %s",
            (client_id,)
        )
        return self.cursor.fetchone() is not None

    def add_moderator(self, client_id: int):
        self.execute(
            "INSERT INTO moderators (ID_CLIENT) VALUES (%s)",
            (client_id,)
        )
        return self

    def get_dish_id(self, name: str) -> int:
        self.execute(
            "SELECT ID FROM plats WHERE NAME = %s",
            (name,)
        )
        return self.cursor.fetchone()

    def add_review(self, restaurant_id: int, client_id: int, rating: int, comment: str, recommendation: Recommendation, plat: str, price: int, begin: int, end: int, date_rating: str, physical_note: int = None, delivery_note: int = None):
        if not self.is_owner(client_id):
            self.execute(
                "INSERT INTO notes (ID_RESTAURANT, ID_CLIENT, NOTE, COMMENT, RECOMMENDATION, ORDERED_DISH, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY, BEGIN_HOUR, END_HOUR, DATE_RATING) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (restaurant_id, client_id, rating, comment,
                recommendation.int(), self.get_dish_id(plat[0]) ,price, physical_note, delivery_note, begin, end, date_rating)
            )
        return self

    def get_mod_id(self, client_id: int) -> int:
        self.cursor.execute(
            "SELECT ID FROM moderators WHERE ID_CLIENT = %s",
            (client_id,)
        )
        return self.cursor.fetchone()

    def delete_review(self, review_id: int, client_id: int):
        if self.is_mod(client_id):
            mod_id = self.get_mod_id(client_id)
            self.execute(
                "SELECT * FROM reviews WHERE ID = %s",
                (review_id,)
            )
            self.cursor.execute(
                "INSERT INTO notes_supprimées (ID, ID_RESTAURANT, ID_CLIENT, RATING, COMMENT, RECOMMENDATION, ORDERED_DISH, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY, ID_MEDERATEUR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (self.cursor.fetchone(), mod_id)
            )
            self.execute(
                "DELETE FROM reviews WHERE ID = %s",
                (review_id,)
            )
        return self

    def search_restaurant(self, name: str) -> list[Restaurant]:
        self.cursor.execute(
            "SELECT * FROM restaurants WHERE name ILIKE %s",
            ("%" + name + "%",)
        )
        response = self.cursor.fetchall()
        result = []
        for restaurant in response:
            result.append(
                Restaurant(
                    restaurant[1],
                    Address(restaurant[4], restaurant[2], restaurant[6], restaurant[3], restaurant[5]),
                    restaurant[13],
                    restaurant[10],
                    restaurant[8],
                    restaurant[11],
                    restaurant[12],
                    PriceRange(restaurant[9]),
                    restaurant[7],
                    restaurant[0]
                )
            )
        return result
        
    def get_restaurant_reviews(self, restaurant_id: int) -> list:
        self.cursor.execute(
            "SELECT * FROM reviews WHERE ID_RESTAURANT = %s",
            (restaurant_id,)
        )
        return self.cursor.fetchall()

    def get_user_reviews(self, client_id: int) -> list:
        self.cursor.execute(
            "SELECT * FROM reviews WHERE ID_CLIENT = %s",
            (client_id,)
        )
        return self.cursor.fetchall()

    def get_owner_restaurants(self, client_id: int) -> list:
        self.cursor.execute(
            "SELECT ID_RESTAURANT FROM owns WHERE ID_USER = %s",
            (client_id,)
        )
        return self.cursor.fetchall()
    
    def get_restaurant_id(self, name: str) -> int:
        self.cursor.execute(
            "SELECT ID FROM restaurants WHERE NAME = %s",
            (name,)
        )
        return self.cursor.fetchone()

    def restaurant_exists(self, name: str, zip: int) -> bool:
        self.cursor.execute(
            "SELECT * FROM restaurants WHERE NAME = %s AND ZIP_CODE = %s",
            (name, zip)
        )
        return self.cursor.fetchone() is not None

    def add_user(self, user):
        if user.is_owner():
            self.create_owner(user.name(), user.first_name(), user.address())
            self.commit()
            for restaurant in user.restaurants():
                self.add_owns(self.get_user_id(user.name(), user.first_name()), self.get_restaurant_id(restaurant))
        else:
            if not self.check_user(user.name(), user.first_name()):
                self.create_user(user.name(), user.first_name(), user.address())
            if user.is_mod():
                self.add_moderator(self.get_user_id(user.name(), user.first_name()))
        return self

    def add_comment(self, comment):
        self.add_review(
            self.get_restaurant_id(comment.restaurant()),
            self.get_user_id(comment.name(), comment.first_name()),
            comment.note(),
            comment.comment(),
            comment.recommendation(),
            comment.menu(),
            comment.price(),
            comment.begin_hour(),
            comment.end_hour(),
            comment.datecomm(),
            comment.noteservice(),
            comment.notedelivery()
        )
        return self

    def fetchall(self):
        return self.cursor.fetchall()
