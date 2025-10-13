import mysql.connector

class DatabaseManager:
  def __init__(self, user, password, host, database):
    self.cnx = mysql.connector.connect(user=user, password=password,
                                        host=host, database=database)
    self.cursor = self.cnx.cursor()

  def connect(self):
    pass
  
  def execute_query(self, query, params=[]):
    self.cursor.execute(query, params)
    res_set = self.cursor.fetchall()
    self.cnx.commit()
    return res_set

  def close(self):
    self.cursor.close()
    self.cnx.close()
  
  def rollback(self):
    self.cnx.rollback()
