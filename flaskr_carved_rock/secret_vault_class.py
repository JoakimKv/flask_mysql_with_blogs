
# secret_vault_class.py


import os
import platform
from pathlib import Path
from dotenv import load_dotenv


class SecretVault:

   def __init__(self):

      # Detect the current OS.
      self.currentOS = platform.system()

      # Default: assume local Windows development
      if self.currentOS == "Windows":

         # Path to .django_env on your Windows machine.
         self.envPath = Path(__file__).resolve().parent / ".flask_env"
         self.isOnServer = False
         self.debugMode = True

      # Otherwise assume Ubuntu server.
      else:

         # Path where you keep secrets on your production server.
         self.envPath = Path("/etc/secrets/mysql/keys/.flask_env")
         self.isOnServer = True
         self.debugMode = False

      # Load environment variables early.

      if self.envPath.exists():

         load_dotenv(dotenv_path = self.envPath)
         print(f"[SecretVault]: Loaded environment from: '{self.envPath}'.")

      else:

         print(f"[SecretVault]: No '.django_env' found at '{self.envPath}'.")

      self.productionDB = "db_flask1"
      self.testDB = "carved_rock_test"

      self.openAIApiKey = os.getenv("OPENAI_API_KEY")
      self.MySQLPort = os.getenv("MYSQL_PORT", "3306")

      self.MySQLUsername = os.getenv("MYSQL_USERNAME")
      self.MySQLPassword = os.getenv("MYSQL_PASSWORD")

      self.MySQLJKUsername = os.getenv("MYSQL_JK_USERNAME")
      self.MySQLJKPassword = os.getenv("MYSQL_JK_PASSWORD")

      if not self.isOnServer:
         self.MySQLHost = os.getenv("MYSQL_HOST", "127.0.0.1")
      else:
         self.MySQLHost = os.getenv("MYSQL_HOST", "host.docker.internal")

      self.secretKey = os.getenv("SECRET_KEY")
      self.secretKeyForDevelopment = os.getenv("SECRET_KEY_SEASONS")

      self.MySQLBlogsDisableSSL = os.getenv("MYSQL_BLOGS_DISABLE_SSL", 1)

   def getCurrentOS(self):

      return self.currentOS
   
   def getIsOnServer(self):

      return self.isOnServer
   
   def getEnvironmentalPath(self):

      return self.envPath
   
   def getProductionDatabase(self):

      return self.productionDB

   def getTestDatabase(self):

      return self.testDB

   def getOpenAIApiKey(self):

      return self.openAIApiKey 
   
   def getMySQLPort(self):

      return self.MySQLPort

   def getMySQLUsername(self):

      return self.MySQLUsername   

   def getMySQLPassword(self):

      return self.MySQLPassword
   
   def getMySQLJKUsername(self):

      return self.MySQLJKUsername   

   def getMySQLJKPassword(self):

      return self.MySQLJKPassword 

   def getMySQLHost(self):

      return self.MySQLHost
   
   def getSecretKey(self):

      return self.secretKey

   def getSecretKeyForDevelopment(self):

      return self.secretKeyForDevelopment
   
   def getMySQLBlogsDisableSSL(self):

      return self.MySQLBlogsDisableSSL

   def setMySQLBlogsDisableSSL(self, MySQLBlogsDisableSSL):

      self.MySQLBlogsDisableSSL = MySQLBlogsDisableSSL

   def getDebugMode(self):

      return self.debugMode
   
   def setDebugMode(self, debugMode):

      self.debugMode = debugMode
 