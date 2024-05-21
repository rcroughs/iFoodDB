<h2 align="center">Internet Food Database</h2>
<p align="center">INFO-H303 @ULB</p>

## Overview
This project is a PostgreSQL database application built using psycopg2, a PostgreSQL adapter for Python. It aims to provide an implementation of the project for the course `INFO-H303` (Database) at the Université Libre de Bruxelles.

The database is a simple restaurant reviewing system. It allows users to add restaurants, add reviews to restaurants, and search for restaurants based on their name, location, or type of cuisine. It also allows the user to see the menu of a restaurant.

The interaction with the database is done through a Python terminal interface.

## Installation
### Prerequisites
Before you begin, ensure you have the following installed on your local machine:
- [Python 3](https://www.python.org/downloads/) (>=3.8)
- [PostgreSQL](https://www.postgresql.org/download/) (>=15)

### Steps
1. **Clone the repository**
```bash
git clone https://github.com/rcroughs/iFoodDB.git
cd iFoodDB
```

2. **Install the dependencies**
```bash
pip install -r requirements.txt
```

### Configuration
1. **Create a new PostgreSQL database**
  - Run psql as a superuser and with user postgres:
```bash
sudo -u postgres psql
```
  - Create a new database with the following commands on `psql`:
```sql
CREATE DATABASE iFoodDB;
CREATE USER ifooddb_user WITH PASSWORD 'password';
ALTER ROLE ifooddb_user SET client_encoding TO 'utf8';
ALTER ROLE ifooddb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ifooddb_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE iFoodDB TO ifooddb_user;
\q
```

- Setup the database schema by running the following command:

```bash
sudo -u postgres psql -d iFoodDB
```
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ifooddb_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO ifooddb_user;
ALTER SCHEMA public OWNER TO ifooddb_user;
\q
```
**Note:** The database name, user, and password can be changed in the `config.py` file.

## Usage
1. **Initialize the intial datas** *(must be run only once)*
```bash
python3 init.py 
```
2. **Run the application**
```bash
python3 ifood.py
```

### Useful commands
- **Drop all tables**
If you want to reset the database, you can drop all tables by running the following command:
```bash
sudo -u postgres psql -d iFoodDB
```
Enter the following command in the `psql` shell:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO ifooddb_user;
\q
```

## Acknowledgements
- [psycopg2](https://www.psycopg.org/)
- [PostgreSQL](https://www.postgresql.org/)


## Authors
- [Romain Croughs](mailto:romain.croughs@ulb.be)
- [Lucas Van Praag](mailto:lucas.van.praag@ulb.be)
- [Gabriel Goldsztajn](mailto:gabriel.goldsztajn@ulb.be)
- [Chris Eid](mailto:chris.eid@ulb.be)