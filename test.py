from app.db import Database
from app.Model.Address import Address
from app.client import Client

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


def test_request2(db):
    # Execute the request2.sql query
    with open("sql/request_2.sql", "r") as file:
        query = file.read()

  
    print("\nExecuting request 2")
    db.cursor.execute(query)
    results = db.cursor.fetchall()

    # Print results for verification
    for row in results:
        print(row)


def test_request5(db):
    # Execute the request5.sql query
    with open("sql/request_5.sql", "r") as file:
        query = file.read()

  
    print("\nExecuting request 5")
    db.cursor.execute(query)
    results = db.cursor.fetchall()

    # Print results for verification
    for row in results:
        print(row)


def test_request6(db):
    # Execute the request6.sql query
    with open("sql/request_6.sql", "r") as file:
        query = file.read()

    print("\nExecuting request 6")
    db.cursor.execute(query)
    results = db.cursor.fetchall()

    # Print results for manual verification
    for row in results:
        print(row)


def test_request3(db):
    # Execute the request3.sql query
    with open("sql/request_3.sql", "r") as file:
        query = file.read()

  
    print("\nExecuting request 3")
    db.cursor.execute(query)
    results = db.cursor.fetchall()

    # Print results for verification
    for row in results:
        print(row)
    

def main():
    db = Database()
    db.connect()
    db.create_tables("sql/create_tables.sql")
    
    test_request2(db)
    test_request3(db)
    test_request5(db)
    test_request6(db)
    

    db.close()

if __name__ == '__main__':
    main()
