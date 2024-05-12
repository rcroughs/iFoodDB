import psycopg2
from app.Model.Restaurant import Restaurant
from app.Model.Address import Address
from app.Model.Recommendation import Recommendation


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname="iFoodDB",
            user="postgres",
            password="verysecurepassword",
            host="localhost",
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
                return self.cursor.fetchone()
        except Exception as e:
            # Rollback the transaction
            self.connection.rollback()
            # Handle exceptions
            print(f"Error executing query: {e}")
            return None

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
                    (dishes_id[-1], allergene)
                )

        menu_id = self.execute(
            "INSERT INTO menus DEFAULT VALUES RETURNING id")[0]

        # Update plats with menu_id
        for dish_id in dishes_id:
            self.execute(
                "UPDATE plats SET menu = %s WHERE id = %s",
                (menu_id, dish_id)
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
            "SELECT RESTAURANT_OWNER FROM users WHERE ID_CLIENT = %s",
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
            "INSERT INTO users (NAME, FIRST_NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, RESTAURANT_OWNER) VALUES (%s, %s, %s, %s, %s, %s, %s)",
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

    def add_owner(self, client_id: int, restaurant_id: int):
        self.execute(
            "INSERT INTO owners (ID_CLIENT, ID_RESTAURANT) VALUES (%s, %s)",
            (client_id, restaurant_id)
        )
        return self

    def add_moderator(self, client_id: int):
        self.execute(
            "INSERT INTO moderators (ID_CLIENT) VALUES (%s)",
            (client_id,)
        )
        return self

    def add_review(self, restaurant_id: int, client_id: int, rating: int, comment: str, recommendation: Recommendation, plat: str, price: int, physical_note: int = None, delivery_note: int = None):
        if not self.is_owner(client_id):
            self.execute(
                "INSERT INTO reviews (ID_RESTAURANT, ID_CLIENT, RATING, COMMENT, RECOMMENDATION, ORDERED_DISH, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (restaurant_id, client_id, rating, comment,
                recommendation.int(), plat, price, physical_note, delivery_note)
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
                    Address(restaurant[2], restaurant[3], restaurant[4], restaurant[5], restaurant[6]),
                    restaurant[7],
                    restaurant[8],
                    restaurant[9],
                    restaurant[10],
                    restaurant[11],
                    restaurant[12],
                    restaurant[13],
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

    def fetchall(self):
        return self.cursor.fetchall()