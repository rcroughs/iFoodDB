from app.db import Database
import psycopg2


def setup_test_data(db):
    # Clear existing data
    db.cursor.execute("TRUNCATE TABLE notes RESTART IDENTITY CASCADE;")
    db.cursor.execute("TRUNCATE TABLE restaurants RESTART IDENTITY CASCADE;")

    # Insert test data into restaurants
    db.cursor.execute("""
        INSERT INTO restaurants (id, food_type) VALUES
        (1, 'Italian'),
        (2, 'Chinese'),
        (3, 'Mexican');
    """)

    # Insert test data into notes
    db.cursor.execute("""
        INSERT INTO notes (id_restaurant, note) VALUES
        (1, 5),
        (1, 4),
        (1, 4),
        (2, 3),
        (2, 3),
        (2, 4),
        (3, 2),
        (3, 2),
        (3, 1);
    """)

    db.connection.commit()


def test_file_resquest(db: Database, file_name: str) -> None:
    # Testing a request from a file
    print(f"🚀 Testing request from file: {file_name}")
    request = ""
    result = None
    with open(file_name, "r") as file:
        request = file.read()
    try:
        db.cursor.execute(request)
        result = db.cursor.fetchall()
    except psycopg2.errors.ProgrammingError as e:
        print(e)
        return
    if result is None:
        print("No result")
    else:
        for row in result:
            print(row)


def main():
    db = Database()
    db.connect()
    db.create_tables("sql/create_tables.sql")

    test_file_resquest(db, "sql/request_1.sql")
    test_file_resquest(db, "sql/request_2.sql")
    test_file_resquest(db, "sql/request_3.sql")
    test_file_resquest(db, "sql/request_4.sql")
    test_file_resquest(db, "sql/request_5.sql")
    test_file_resquest(db, "sql/request_6.sql")

    db.close()


if __name__ == "__main__":
    main()
