
# db_connection_wrapper.py


import pymysql

from flaskr_carved_rock.database_connection_data import DatabaseConnectionData


class DBConnectionWrapper:


   def __init__(self, conn = None, databaseConnectionData = None, testing = False):


      """
      Initialize the wrapper and create a PyMySQL connection.
      """

      self.databaseConnectionData = databaseConnectionData

      if not databaseConnectionData:
           
         self.databaseConnectionData = DatabaseConnectionData(testing = testing)

      username = self.databaseConnectionData.username
      password = self.databaseConnectionData.password
      database = self.databaseConnectionData.database
      host = self.databaseConnectionData.host
      port = self.databaseConnectionData.port
      sslDisabled = self.databaseConnectionData.sslDisabled

      if conn:

         self._conn = conn

      else:

         if not username or not password or not database:
                
            raise ValueError("user, password, and database must be provided")
            
         self._conn = pymysql.connect(
            host = host,
            port = port,
            user = username,
            password = password,
            database = database,
            ssl = {"ssl": {}} if not sslDisabled else None,
            cursorclass = pymysql.cursors.DictCursor
         )

      # Internal storage for autocommit to avoid recursion
      self._autocommit = True
      self.autocommit = True  # call setter to propagate to connection

   def _ensure_open(self):
      
      if self._conn is None:
            
         raise pymysql.err.InterfaceError("Connection already closed")

   def cursor(self):
      
      self._ensure_open()
      return self._conn.cursor()

   def commit(self):
      
      self._ensure_open()
      return self._conn.commit()

   def rollback(self):
      
      self._ensure_open()
      return self._conn.rollback()

   def execute(self, query, params=None):
      
      self._ensure_open()
      with self._conn.cursor() as cursor:
            
         cursor.execute(query, params or ())
         return cursor

   def close(self):
      
      try:
         
         self._conn.close()

      finally:
         
         self._conn = None  # make it unusable.


   # --- autocommit property ---
   @property
   def autocommit(self):
        
      return self._autocommit

   @autocommit.setter
   def autocommit(self, value):
        
      self._autocommit = value
      if hasattr(self._conn, "autocommit"):
            
         # PyMySQL connections support autocommit()
         try:
             
            self._conn.autocommit(value)

         except Exception:
             
            # fallback if autocommit attribute is not callable
            self._conn.autocommit = value

   # Forward all other attributes to real connection
   def __getattr__(self, name):
        
      if name in self.__dict__:
          
         return self.__dict__[name]
        
      return getattr(self._conn, name)
