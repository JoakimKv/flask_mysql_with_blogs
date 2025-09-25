
# database_connection_data.py


import os


class DatabaseConnectionData:


    PRODUCTION_DATABASE = "db_flask1"
    TESTING_DATABASE = "carved_rock_test"
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306


    def __init__(self, host = MYSQL_HOST, username = MYSQL_USERNAME, password = MYSQL_PASSWORD,
                 database = None, port = MYSQL_PORT, testing = False):

       self.testingDatabase = DatabaseConnectionData.TESTING_DATABASE
       self.productionDatabase = DatabaseConnectionData.PRODUCTION_DATABASE

       self.host = DatabaseConnectionData.MYSQL_HOST
       self.username = DatabaseConnectionData.MYSQL_USERNAME
       self.password = DatabaseConnectionData.MYSQL_PASSWORD
       self.port = DatabaseConnectionData.MYSQL_PORT
       self.testing = testing

       self.database = database

       if not database:
                   
          self.database = self.TESTING_DATABASE if testing else self.PRODUCTION_DATABASE

    def getDatabase(self):
          
       return self.database

    def setDatabase(self, database):

       self.database = database

    def setIsTestingAndChangeDatabase(self, testing):
       
       self.testing = testing

       if testing:
          
          self.database = self.testingDatabase

       else:

          self.database = self.productionDatabase

    def getIsTesting(self):
       
       return self.testing

    def getProductionDatabase(self):
          
       return self.productionDatabase

    def setProductionDatabase(self, database):

       self.productionDatabase = database

    def getTestingDatabase(self):
          
       return self.testingDatabase

    def setTestingDatabase(self, database):

       self.testingDatabase = database
      