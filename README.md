
# Flask Project – Flask and mysql with blogs

A **Flask web application** that demonstrates clean application structure, database modeling, and testing.  
The project uses **MySQL** as the backend database (but can easily be switched to another database by editing a single configuration class).

Inspired by a Pluralsight course on Flask with SQLite, this project has been adapted and extended by **Joakim Kvistholm**. In this project I use a mysql server for both the test and production database which are running by docker and I am using HeidiSQL as an extra database handler.  

---

## Features  

- User authentication with hashed passwords.  
- Blog posts with authors, timestamps, and tags.  
- Relational database schema with proper foreign keys.  
- Alembic database migrations.  
- Configurable database connection via `DatabaseConnectionData`.  
- Unit tests with `pytest`.  
- Structured project layout for maintainability.  

---

## Extra Information

All users (that are not test users for pytest) have the password `root`.

## Project Structure  

An simplified overview:

flask_mysql_with_blogs/
│
├── flaskr_carved_rock/ # Main Flask application package
│ ├── init.py # App factory
│ ├── db_connection_wrapper.py
│ ├── database_connection_data.py
│ ├── models/ # ORM and database models
│ └── templates/ 
│
├── migrations/ # Alembic migration scripts
├── tests/ # Unit and integration tests
│ ├── conftest.py
│ └── test_db.py
│
├── requirements.txt
├── pyproject.toml
└── README.md

Note that there is a folder called 'heidisql' that contains three mysql scripts that can be run in 'HeidiSQL':

 - The 'first' script creates the entire database from scratch with tables and data (which is done by the script 'db_flask1.sql').

 - The 'second' script restores the production database 'db_flask1' from the test database 'carved_rock_test' (which is done by the script 'carved_rock_test_save_from_production_db.sql').

- The 'third' script makes the reverse process: it restores the test database from the production database (which is done by the script 'db_flask1_save_from_test_db.sql').

The last two scripts can be used if an accident happens with the databases. ChatGPT can be used to rewrite the scripts if such a need arises (so it suits your databases).

## Database  

The application uses **MySQL 8.1+**.  
Tables include:  

- **user** – stores usernames, hashed passwords, UUIDs, and API keys  
- **post** – blog posts linked to authors  
- **tag** and **tags_association** – tagging system for posts  
- **alembic_version** – versioning for database migrations  

Sample schema and data are provided in ('db_flask1.sql').

## Installation guide and running the server

On windows 11:

To start the virtual environment: python -m venv venvflask1
To enable scripts (if necessary): Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
To activate script / environment: venvflask1\Scripts\activate

To install packages: pip install -r requirements.txt
If you want to install all the package manually then the file 'pip_install.txt' can be of use. 

Don't forget to populate your mysql database from 'db_flask1.sql' in the 'heidisql' folder.

To start the server (in debug mode): python -m flask run --host=0.0.0.0 --port=5000 --debug

Then write the following in a web browser: localhost:5000

## Running pytests

The following pytests can be run (in 'flask_mysql_with_blogs' folder):

- pytest tests/test_db.py
- pytest tests/test_factory.py
- pytest tests/test_auth.py
- pytest tests/test_blog.py
- pytest tests/test_delete_account.py
- pytest tests/test_change_password.py


## Author

This project is made by Joakim Kvistholm.
