
# database_connection_data.py


import os
from secret_vault_class import SecretVault 


class DatabaseConnectionData:

    secretVault = SecretVault()

    PRODUCTION_DATABASE = secretVault.getProductionDatabase()
    TESTING_DATABASE = secretVault.getTestDatabase()
    MYSQL_JK_USERNAME = secretVault.getMySQLJKUsername()
    MYSQL_JK_PASSWORD = secretVault.getMySQLJKPassword()
    MYSQL_HOST = secretVault.getMySQLHost()
    MYSQL_PORT = int(secretVault.getMySQLPort())
    MYSQL_BLOGS_DISABLE_SSL = secretVault.getMySQLBlogsDisableSSL()

    
    def __init__(self, host = MYSQL_HOST, username = MYSQL_JK_USERNAME, password = MYSQL_JK_PASSWORD,
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
      

