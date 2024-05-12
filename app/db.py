import psycopg2
from app.Model.Restaurant import Restaurant


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

    def add_allergen(self, allergen: str) -> None:
        self.execute(
            "INSERT INTO allergenes (NAME) VALUES (%s)",
            (allergen,)
        )

    def fetchall(self):
        return self.cursor.fetchall()
