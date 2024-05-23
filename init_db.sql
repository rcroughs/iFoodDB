CREATE DATABASE "iFoodDB";
CREATE USER ifooddb_user WITH PASSWORD 'password';
ALTER ROLE ifooddb_user SET client_encoding TO 'utf8';
ALTER ROLE ifooddb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ifooddb_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE "iFoodDB" TO ifooddb_user;