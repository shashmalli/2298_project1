import bcrypt
import utils as u
from dbms import DatabaseManager

class User:
  def __init__(self, username, role="user"):
    self.username = username
    self.role = role
    self.db = DatabaseManager(u.USER, u.PASSWORD, "localhost", "journal_2298_p1")

  def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  
  @staticmethod
  def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
  
  def create_user(self, password):
    hashed = User.hash_password(password)
    # Insert user into database
    try:
      self.db.execute_query("INSERT INTO users (user_name, password_hash, role) VALUES (%s, %s, %s)", (self.username, hashed, self.role))
    except Exception as e:
      self.db.rollback()
      if e.errno == 1062:  # Duplicate entry error code
        u.log_event("ERROR", f"User {self.username} already exists", 1)
        print(f"User {self.username} already exists.")
      else:
        u.log_event("ERROR", f"Error creating user {self.username}", 1)
        print("Error creating user. Please try again.\n")
    else:
      u.log_event("INFO", f"Created user {self.username} with role {self.role}", 1)
      print(f"User {self.username} registered successfully!\n")
      return True
    finally:
      self.db.close()
  
  def authenticate(self, username, password):
    # Fetch user from database
    try:
      user_record = self.db.execute_query("SELECT * FROM users WHERE user_name = %s", [(self.username)])
      if user_record:
        if User.check_password(password, user_record[0][2]):  # Assuming password hash is at index 2
          print(f"Welcome {username}\n")
          return user_record
    except Exception as e:
      self.db.rollback()
      u.log_event("ERROR", f"Authentication failed for user {username}", 1)
      print("Invalid username or password\n")
    finally:
      self.db.close()
  
  def close_connection(self):
    self.db.close()
