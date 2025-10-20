
# Flask Project – Flask and mysql with blogs

A **Flask web application** that demonstrates clean application structure, database modeling, and testing. This project, which is about blogs, is connected with my django project, which is about seasonal works in ArsMagica. This project takes care of the endpoint "blogs/". The project uses **MySQL** as the backend database (but it can easily be switched to another mysql database by editing a single configuration class).

I was inspired by a Pluralsight course on Flask where SQLite is used. This project has been adapted and extended for further development by **Joakim Kvistholm** to work with a 'real' mysql database. In this project I use a mysql server for both the test and production database which are running by docker and I am using HeidiSQL as an extra database handler. All this takes the program one step closer to work as a 'real' web page with a 'real' production database on a server.  

---

## Features  

- User authentication with hashed passwords.  
- Blog posts with users, timestamps, and tags.  
- Relational database schema with proper foreign keys.  
- Alembic database migrations.  
- Configurable database connection via `DatabaseConnectionData`.  
- Unit tests with `pytest`.  
- Structured project layout for maintainability.  

---

## Extra Information

All users (that are not test users for pytest) have the password `root`. It is recommended to look at 'pip_install_info.txt' here is a lot of important information and useful commands if you want to use the project. My domain is 'kvistholm.net' at the time of creating this project, but you may have to change this domain name with your own domain name especially in nginx's 'blogs_seasons.conf' but also in many other places.

## Project Structure  

A simplified overview:

- The main folder: -> 'flask_mysql_with_blogs'.

- 'flaskr_carved_rock': -> Main Flask application package (inside the main folder).

- 'migrations': -> Alembic migration scripts (inside the main folder).

- 'tests': -> Unit and integration tests (inside the main folder).

---

Note that there is a folder called 'heidisql' that contains three mysql scripts that can be run in 'HeidiSQL':

 - The 'first' script creates the entire database from scratch with tables and data (which is done by running the script 'db_flask1.sql').

 - The 'second' script restores the production database 'db_flask1' from the test database 'carved_rock_test' (which is done by running the script 'carved_rock_test_save_from_production_db.sql').

- The 'third' script makes the reverse process: it restores the test database from the production database (which is done by running the script 'db_flask1_save_from_test_db.sql').

The last two scripts can be used if an accident happens with the databases. ChatGPT can be used to rewrite the scripts if such a need arises (so it suits your databases).

## Database  

The application uses **MySQL 8.1+**.  
Tables include:  

- **user** – stores usernames, hashed passwords, UUIDs, and API keys.  
- **post** – blog posts linked to authors.  
- **tag** and **tags_association** – tagging system for posts.  
- **alembic_version** – versioning for database migrations.  

Sample schema and data are provided in ('db_flask1.sql').

## Installation guide and running the server

On windows 11 (and an ubuntu server):

- Install nginx and get the certificate for https (for your hostname). Use my 'blogs_seasons.conf' (on ubuntu server in '/etc/nginx/sites-available' and in this project in 'nginx' folder). This is the same file as corresponding file in my django project. This project has the endpoint 'localhost:5000/blogs' in debug mode. This is the final version of this '.conf' file 'after' the certificate is issued and you need to adapt it to your own server. The 'blogs_seasons_temp.conf' is the 'blogs_seasons.conf' file before you retrieve your needed certificate and it may need to be adapted to your own server. Note that for the Flask and Django project 'blogs_seasons.conf' is the same file that is stored on the ubuntu server. 

- To start the virtual environment: python -m venv venvflask1

- To enable scripts (if necessary): Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

- To activate script and environment: venvflask1\Scripts\activate

- To install packages: python -m pip install -r requirements.txt

- If you want to install all the package manually then the file 'pip_install_info.txt' can be of use. 

- Don't forget to populate your mysql database from 'db_flask1.sql' in the 'heidisql' folder.

- To start the server (in debug mode): python -m flask run --host=0.0.0.0 --port=5000 --debug

- Then write the following in a web browser: localhost:5000/blogs or your own "server adress".

- The flask app is running in a docker. The nginx and the mysql database is run on a ubuntu server, they are not dockerized and are run with services on the ubuntu server. The file 'blogs_seasons.conf' with the use of nginx is needed to configure the different ports that are used to run the programs (the containarized apps: the 'Django app' and the 'Flask app').

## Environmental variables and secrets

These secrets in your repository must be set (stored in your github repository):
- The secrets in 'deploy.yml' (where 'secrets.' has been added to the code): secrets.SERVER_IP (Ubuntu server ip), secrets.SERVER_ROOT_USERNAME (the username for root, often root) and secrets.SSH_PRIVATE_KEY (your ssh key to connect to the server). They are stored in '.flask_env', see '.flask_env.example', for how it can look. The 'SecretVault' class (in the file 'secret_vault_class.py') handles these secrets. On the Ubuntu server they are stored in '/etc/secrets/mysql/keys/.flask_env'.

## Running pytests

The following pytests can be run (in 'flask_mysql_with_blogs' folder):

- pytest tests/test_db.py
- pytest tests/test_factory.py
- pytest tests/test_auth.py
- pytest tests/test_blog.py
- pytest tests/test_delete_account.py
- pytest tests/test_change_password.py

The tests should not be run on the ubuntu server as not to effect your real production database and if the test works on your local windows machine they will work on the ubuntu server, since they are using the same authorizations and the same endpoints.

## Author

This project is made by Joakim Kvistholm.
