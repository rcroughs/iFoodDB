"""
Python script to initialize the DDL
"""

from app.db import Database


def main():
    db = Database()
    db.connect()
    print("💾 Creating tables...")
    db.create_tables("sql/create_tables.sql")
    db.close()


if __name__ == "__main__":
    main()
