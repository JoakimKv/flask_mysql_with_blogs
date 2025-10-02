
# database_connection_data.py


import os


class DatabaseConnectionData:


    PRODUCTION_DATABASE = "db_flask1"
    TESTING_DATABASE = "carved_rock_test"
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_BLOGS_DISABLE_SSL = os.getenv("MYSQL_BLOGS_DISABLE_SSL", 1)

    
    def __init__(self, host = MYSQL_HOST, username = MYSQL_USERNAME, password = MYSQL_PASSWORD,
                 database = None, port = MYSQL_PORT, sslDisabled = MYSQL_BLOGS_DISABLE_SSL, 
                 testing = False):

       self.testingDatabase = DatabaseConnectionData.TESTING_DATABASE
       self.productionDatabase = DatabaseConnectionData.PRODUCTION_DATABASE

       self.host = host
       self.username = username
       self.password = password
       self.port = port
       self.sslDisabled = sslDisabled
       self.testing = testing

       self.database = database

       if not database:
                   
          self.database = self.TESTING_DATABASE if testing else self.PRODUCTION_DATABASE

    def getDatabase(self):
          
       return self.database

    def setDatabase(self, database):

       self.database = database

    def getHost(self):
          
       return self.host

    def setHost(self, host):

       self.host = host

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
      

