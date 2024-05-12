from app.db import Database
from app.Model.Address import Address
from app.client import Client

def main():
    db = Database()
    db.connect()
    db.create_tables("sql/create_tables.sql");

    Client(db).run()
    
    db.close()

if __name__ == '__main__':
    main()