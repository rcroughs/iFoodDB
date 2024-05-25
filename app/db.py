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
        """
        Connect to the PostgreSQL database server
        """
        self.connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port="5432",
            client_encoding="utf-8",
        )
        self.cursor = self.connection.cursor()

    def create_tables(self, sql_file: str) -> None:
        """
        Create tables in the PostgreSQL database, if they don't already exist

        :param sql_file: The path to the SQL file containing the tables creation queries
        """
        with open(sql_file, "r") as f:
            self.cursor.execute(f.read())
        self.connection.commit()

    def close(self):
        """
        Close the connection to the PostgreSQL database server
        """
        self.cursor.close()
        self.connection.close()

    def execute(self, query: str, args=None) -> int:
        """
        Execute a query on the database

        :param query: The query to execute
        :param args: The arguments to pass to the query

        :return: The return value of the query
        """
        if args is None:
            args = ()
        try:
            self.cursor.execute(query, args)
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

    def exec_file(self, file: str):
        """
        Execute a SQL file

        :param file: The path to the SQL file
        """
        res = ()
        with open(file, "r") as f:
            res = self.cursor.execute(f.read())
        return res

    def select(self, table: str, columns: list, condition: str = None, args=None):
        """
        Perform a SELECT query on the database

        :param table: The table to select from
        :param columns: The columns to select
        :param condition: The condition to apply to the query
        """
        if args is None:
            args = ()
        query = f"SELECT {', '.join(columns)} FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def commit(self):
        """
        Commit the database transaction
        """
        self.connection.commit()

    def add_restaurant(self, restaurant: Restaurant) -> int:
        """
        Add a restaurant to the database

        :param restaurant: The restaurant to add

        :return: The ID of the restaurant
        """
        dishes_id = []
        for dishes in restaurant.menu():
            allergenes_id = []
            for allergenes in dishes.allergens():
                allergenes_id.append(
                    self.select("allergenes", ["id"], "name = %s", (allergenes,))[0]
                )
            dishes_id.append(
                self.execute(
                    "INSERT INTO plats (NAME, PRICE) VALUES (%s, %s) RETURNING id",
                    (dishes.name(), dishes.price()),
                )
            )
            for allergene in allergenes_id:
                self.execute(
                    "INSERT INTO plats_allergenes (ID_PLAT, ID_ALLERGENE) VALUES (%s, %s)",
                    (dishes_id[-1][0], allergene[0]),
                )

        menu_id = self.execute("INSERT INTO menus DEFAULT VALUES RETURNING id")[0]

        # Update plats with menu_id
        for dish_id in dishes_id:
            self.execute(
                "UPDATE plats SET menu = %s WHERE id = %s", (menu_id, dish_id[0])
            )

        return self.execute(
            "INSERT INTO restaurants (NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, delivery, average_rating, menu, opening_time, closing_time, price_range, food_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                restaurant.name(),
                restaurant._address.street(),
                int(restaurant._address.number()),
                restaurant._address.city(),
                restaurant._address.zip_code(),
                restaurant._address.city(),
                restaurant.delivery(),
                restaurant.evaluation(),
                menu_id,
                restaurant.opening(),
                restaurant.closing(),
                restaurant.price_range().int(),
                restaurant.type(),
            ),
        )

    def add_allergen(self, allergen: str):
        """
        Adds an allergen to the database

        :param allergen: The allergen to add
        """
        return self.execute(
            "INSERT INTO allergenes (NAME) VALUES (%s) RETURNING id", (allergen,)
        )[0]

    def add_dish(self, menu_id: int, dish_name: str, price: float):
        return self.execute(
            "INSERT INTO plats (NAME, PRICE, MENU) VALUES (%s, %s, %s) returning id",
            (dish_name, price, menu_id),
        )[0]

    def remove_dish(self, dish_id: int):
        """
        Remove a dish from the database

        :param dish_id: The ID of the dish
        """
        self.execute("DELETE FROM plats_allergenes WHERE ID_PLAT = %s", (dish_id,))
        # Dont deleted completely, just set the menu to NULL so the dish is not displayed but still accessible for the reviews
        self.execute("UPDATE plats SET MENU = NULL WHERE ID = %s", (dish_id,))
        return self

    def add_dish_allergen(self, dish_id: int, allergen_id: int):
        """
        Adds an allergen to a dish

        :param dish_id: The ID of the dish
        :param allergen_id: The ID of the allergen
        """
        self.execute(
            "INSERT INTO plats_allergenes (ID_PLAT, ID_ALLERGENE) VALUES (%s, %s)",
            (dish_id, allergen_id),
        )
        return self

    def create_user(self, name: str, first_name: str, address: Address):
        """
        Create a user in the database

        :param name: The name of the user
        :param first_name: The first name of the user
        :param address: The address of the user
        """
        self.execute(
            "INSERT INTO users (NAME, FIRST_NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, RESTAURANT_OWNER) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                name,
                first_name,
                address.street(),
                address.number(),
                address.city(),
                address.zip_code(),
                address.country(),
                False,
            ),
        )
        return self

    def get_user_id(self, name: str, first_name: str) -> int:
        """
        Get the ID of a user by their name

        :param name: The name of the user
        :param first_name: The first name of the user
        """
        self.cursor.execute(
            "SELECT ID FROM users WHERE NAME = %s AND FIRST_NAME = %s",
            (name, first_name),
        )
        return self.cursor.fetchone()

    def get_user(self, user_id: int) -> tuple:
        self.cursor.execute("SELECT * FROM users WHERE ID = %s", (user_id,))
        return self.cursor.fetchone()

    def is_owner(self, client_id: int) -> bool:
        """
        Returns if a user is a restaurant owner
        """
        self.cursor.execute(
            "SELECT RESTAURANT_OWNER FROM users WHERE ID = %s", (client_id,)
        )
        return self.cursor.fetchone()[0] is True

    def add_owns(self, client_id: int, restaurant_id: int):
        """
        Add a restaurant to the list of restaurants owned by a user
        """
        if self.is_owner(client_id):
            self.execute(
                "INSERT INTO owns (ID_USER, ID_RESTAURANT) VALUES (%s, %s)",
                (client_id, restaurant_id),
            )
        return self

    def create_owner(self, name: str, first_name: str, address: Address):
        """
        Create a restaurant owner in the database
        """
        self.execute(
            "INSERT INTO users (NAME, FIRST_NAME, STREET, STREET_NUMBER, CITY, ZIP_CODE, COUNTRY, RESTAURANT_OWNER) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                name,
                first_name,
                address.street(),
                address.number(),
                address.city(),
                address.zip_code(),
                address.country(),
                True,
            ),
        )
        return self

    def check_owner(self, name: str, first_name: str) -> bool:
        """
        Check if a given user is a restaurant owner
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE NAME = %s AND FIRST_NAME = %s AND RESTAURANT_OWNER = TRUE",
            (name, first_name),
        )
        return self.cursor.fetchone() is not None

    def check_user(self, name: str, first_name: str) -> bool:
        """
        Check if a given user exists in the database

        :param name: The name of the user
        :param first_name: The first name of the user
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE NAME = %s AND FIRST_NAME = %s AND RESTAURANT_OWNER = FALSE",
            (name, first_name),
        )
        return self.cursor.fetchone() is not None

    def is_mod(self, client_id) -> bool:
        """
        Check if a given user is a moderator
        """
        self.cursor.execute(
            "SELECT * FROM moderators WHERE ID_CLIENT = %s", (client_id,)
        )
        return self.cursor.fetchone() is not None

    def add_moderator(self, client_id: int):
        """
        Gives moderator rights to a user
        """
        self.execute("INSERT INTO moderators (ID_CLIENT) VALUES (%s)", (client_id,))
        return self

    def get_dish_id(self, name: str, menu_id: int = None) -> int:
        """
        Get the ID of a dish by its name
        """
        if menu_id is None:
            return self.execute("SELECT ID FROM plats WHERE NAME = %s", (name,))
        else:
            return self.execute(
                "SELECT ID FROM plats WHERE NAME = %s AND MENU = %s", (name, menu_id)
            )

    def get_dishes(self, menu_id) -> tuple:
        return self.execute("SELECT * FROM plats WHERE MENU = %s", (menu_id,))

    def get_dishes_id_from_review(self, review_id: int) -> list:
        """
        Get the dishes ordered in a review
        """
        self.cursor.execute(
            "SELECT ID_PLAT FROM notes_plat WHERE ID_NOTE = %s", (review_id,)
        )
        return self.cursor.fetchall()

    def get_dish_name(self, dish_id: int) -> str:
        """
        Get the name of a dish by its ID
        """
        self.cursor.execute("SELECT NAME FROM plats WHERE ID = %s", (dish_id,))
        return self.cursor.fetchone()[0]

    def get_all_allergens(self) -> list:
        """
        Get all allergens from the database
        """
        self.cursor.execute("SELECT * FROM allergenes")
        return self.cursor.fetchall()

    def get_allergens(self, dish_id: int) -> list:
        """
        Get all allergens of a dish
        """
        self.cursor.execute(
            "SELECT * FROM plats_allergenes WHERE ID_PLAT = %s", (dish_id,)
        )
        return self.cursor.fetchall()

    def get_allergen_name(self, allergen_id: int) -> str:
        """
        Get the name of an allergen by its ID
        """
        self.cursor.execute("SELECT NAME FROM allergenes WHERE ID = %s", (allergen_id,))
        return self.cursor.fetchone()[0]

    def add_review(
        self,
        restaurant_id: int,
        client_id: int,
        rating: int,
        comment: str,
        recommendation: Recommendation,
        plat: list[str],
        price: int,
        begin: int,
        end: int,
        date_rating: str,
        physical_note: int = None,
        delivery_note: int = None,
    ):
        """
        Add a review to a restaurant

        :param restaurant_id: The ID of the restaurant
        :param client_id: The ID of the client
        :param rating: The rating of the restaurant
        :param comment: The comment of the client
        :param recommendation: The recommendation of the client (RECOMMENDED, NOT_RECOMMENDED, TO_BE_AVOIDED)
        :param plat: The ordered dishes
        :param price: The price of the meal
        :param begin: The beginning of the meal
        :param end: The end of the meal
        :param date_rating: The date of the rating
        :param physical_note: The physical note of the restaurant
        :param delivery_note: The delivery note of the restaurant
        """
        review_id = None
        if not self.is_owner(client_id):
            review_id = self.execute(
                "INSERT INTO notes (ID_RESTAURANT, ID_CLIENT, NOTE, COMMENT, RECOMMENDATION, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY, BEGIN_HOUR, END_HOUR, DATE_RATING) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    restaurant_id,
                    client_id,
                    rating,
                    comment,
                    recommendation.int(),
                    price,
                    physical_note,
                    delivery_note,
                    begin,
                    end,
                    date_rating,
                ),
            )[0]
            for elem in plat:
                self.execute(
                    "INSERT INTO notes_plat (ID_PLAT, ID_NOTE) VALUES (%s, %s)",
                    (
                        self.get_dish_id(elem, self.get_menu_id(restaurant_id))[0],
                        review_id,
                    ),
                )

            # Update the average rating of the restaurant
            self.execute(
                "UPDATE restaurants SET AVERAGE_RATING = (SELECT AVG(NOTE) FROM notes WHERE ID_RESTAURANT = %s) WHERE ID = %s",
                (restaurant_id, restaurant_id),
            )
        return review_id

    def get_menu_id(self, restaurant_id: int) -> int:
        """
        Get the menu ID of a restaurant
        """
        return self.execute(
            "SELECT MENU FROM restaurants WHERE ID = %s", (restaurant_id,)
        )[0]

    def get_review_id(
        self, restaurant_id: int, client_id: int, date_rating: str
    ) -> int:
        """
        Get the review id of a given review
        """
        self.cursor.execute(
            "SELECT ID FROM notes WHERE ID_RESTAURANT = %s AND ID_CLIENT = %s AND DATE_RATING = %s",
            (restaurant_id, client_id, date_rating),
        )
        return self.cursor.fetchone()

    def get_mod_id(self, client_id: int) -> int:
        """
        Get the mod id of a given user
        """
        self.cursor.execute(
            "SELECT ID FROM moderators WHERE ID_CLIENT = %s", (client_id,)
        )
        return self.cursor.fetchone()

    def delete_review(self, review_id: int, client_id: int, mod_comment: str):
        """
        Delete a review from the database and add it to the deleted reviews table
        """
        if self.is_mod(client_id):
            mod_id = self.get_mod_id(client_id)
            informations = self.execute(
                "SELECT * FROM reviews WHERE ID = %s", (review_id,)
            )
            self.cursor.execute(
                "INSERT INTO notes_supprimées (ID, ID_RESTAURANT, ID_CLIENT, RATING, COMMENT, RECOMMENDATION, ORDERED_DISH, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY, ID_MEDERATEUR, MOD_COMMENT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (informations, mod_id, mod_comment),
            )
            self.execute("DELETE FROM reviews WHERE ID = %s", (review_id,))
        return self

    def delete_review_anonymously(self, review_id: int, mod_comment: str):
        """
        Delete a review from the database and add it to the deleted reviews table without specifying the moderator
        Please note that this function is only used when the moderator is not known (e.g. when we are parsing the file)
        """
        note_informations = self.execute(
            "SELECT * FROM notes WHERE ID = %s", (review_id,)
        )[0]
        id = note_informations[0]
        client_id = note_informations[1]
        restaurant_id = note_informations[2]
        date_rating = note_informations[3]
        comment = note_informations[4]
        rating = note_informations[5]
        recommendation = note_informations[6]
        note_physical = note_informations[7]
        note_delivery = note_informations[8]
        begin_hour = note_informations[9]
        end_hour = note_informations[10]
        price = note_informations[11]
        self.execute(
            "INSERT INTO notes_supprimees (ID, ID_RESTAURANT, ID_CLIENT, DATE_RATING, COMMENT, NOTE, RECOMMENDATION, PRICE, NOTE_PHYSICAL, NOTE_DELIVERY, BEGIN_HOUR, END_HOUR, MOD_COMMENT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                id,
                restaurant_id,
                client_id,
                date_rating,
                comment,
                rating,
                recommendation,
                price,
                note_physical,
                note_delivery,
                begin_hour,
                end_hour,
                mod_comment,
            ),
        )
        self.execute("DELETE FROM notes WHERE ID = %s", (review_id,))
        return self

    def search_restaurant(self, name: str) -> list[Restaurant]:
        """
        Search for a restaurant by its name
        """
        self.cursor.execute(
            "SELECT * FROM restaurants WHERE name ILIKE %s", ("%" + name + "%",)
        )
        response = self.cursor.fetchall()
        result = []
        for restaurant in response:
            result.append(
                Restaurant(
                    restaurant[1],
                    Address(
                        restaurant[4],
                        restaurant[2],
                        restaurant[6],
                        restaurant[3],
                        restaurant[5],
                    ),
                    restaurant[13],
                    restaurant[10],
                    restaurant[8],
                    restaurant[11],
                    restaurant[12],
                    PriceRange(restaurant[9]),
                    restaurant[7],
                    restaurant[0],
                )
            )
        return result

    def get_restaurant_reviews(self, restaurant_id: int) -> list:
        """
        Get reviews of a given restaurant
        """
        self.cursor.execute(
            "SELECT * FROM notes WHERE ID_RESTAURANT = %s", (restaurant_id,)
        )
        return self.cursor.fetchall()

    def get_user_reviews(self, client_id: int) -> list:
        """
        Get reviews posted by a given user
        """
        self.cursor.execute("SELECT * FROM reviews WHERE ID_CLIENT = %s", (client_id,))
        return self.cursor.fetchall()

    def get_owner_restaurants(self, client_id: int) -> list:
        """
        Get all restaurants owned by a given user
        """
        return self.execute(
            "SELECT ID_RESTAURANT FROM owns WHERE ID_USER = %s", (client_id,)
        )

    def get_restaurant_id(self, name: str) -> int:
        """
        Get the ID of a restaurant by its name
        """
        self.cursor.execute("SELECT ID FROM restaurants WHERE NAME = %s", (name,))
        return self.cursor.fetchone()

    def get_restaurant_name(self, restaurant_id: int) -> str:
        """
        Get the name of a restaurant by its ID
        """
        self.cursor.execute(
            "SELECT NAME FROM restaurants WHERE ID = %s", (restaurant_id,)
        )
        return self.cursor.fetchone()[0]

    def restaurant_exists(self, name: str, zip: int) -> bool:
        """
        Search for a restaurant by its name and zip code
        """
        self.cursor.execute(
            "SELECT * FROM restaurants WHERE NAME = %s AND ZIP_CODE = %s", (name, zip)
        )
        return self.cursor.fetchone() is not None

    ### Functions for the parser (can be used outside of it, but are mostly used in the parser) ###

    def add_user(self, user):
        if user.is_owner():
            if not self.check_user(user.name(), user.first_name()):
                self.create_owner(user.name(), user.first_name(), user.address())
                self.commit()
            for restaurant in user.restaurants():
                self.add_owns(
                    self.get_user_id(user.name(), user.first_name()),
                    self.get_restaurant_id(restaurant),
                )
        else:
            if not self.check_user(user.name(), user.first_name()):
                self.create_user(user.name(), user.first_name(), user.address())
            if user.is_mod():
                self.add_moderator(self.get_user_id(user.name(), user.first_name()))
        return self

    def add_comment(self, comment):
        if len(comment.comment()) > 4096:
            print(f"Comment too long: {len(comment.comment())}")
            return self
        return self.add_review(
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
            comment.notedelivery(),
        )

    def delete_comment(self, comment):
        review_id = self.get_review_id(
            self.get_restaurant_id(comment.restaurant()),
            self.get_user_id(comment.name(), comment.first_name()),
            comment.datecomm(),
        )
        if review_id is None:
            review_id = self.add_comment(comment)
            self.commit()
        self.delete_review_anonymously(review_id, comment.mod_comment())
        return self

    def fetchall(self):
        return self.cursor.fetchall()
