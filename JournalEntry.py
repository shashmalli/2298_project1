import utils as u
from dbms import DatabaseManager

class JournalEntry:
  def __init__(self):
    self.db = DatabaseManager(u.USER, u.PASSWORD, "localhost", "journal_2298_p1")

  #insert
  def insert_into(self, username, content):
    try:
      user_id = self.db.execute_query("SELECT id FROM users WHERE user_name = (%s)", [(username)])[0][0]
      self.db.execute_query("INSERT INTO journal_entries (user_id, content) VALUES (%s, %s)", (user_id, content))
      u.log_event("INFO", "Added journal entry", user_id)
      print("Journal entry added successfully!\n")
    except Exception as e:
      self.db.rollback()
      if e.errno == 1406:  # Data too long for column
        u.log_event("ERROR", "Content exceeds maximum length", user_id)
        print("Error: Content exceeds maximum length.\n")
      else:
        u.log_event("ERROR", "Error inserting journal entry", user_id)
        print("Error inserting entry. Please try again.\n")
    finally:
      self.db.close()

  def custom_query(self, query, params):
    try:
      return self.db.execute_query(query, params)
    except Exception as e:
      self.db.rollback()
      print("Error executing query. Please try again.\n")

  #query
  def query(self, user_name):
    try:
      if user_name == "admin":
        res_set = self.db.execute_query("SELECT DATE(created_at), content, user_id FROM journal_entries")
        u.log_event("INFO", "Fetched all journal entries", 1) # Assuming admin user_id is 1
      else:
        user_id = self.db.execute_query("SELECT id FROM users WHERE user_name = (%s)", [(user_name)])[0][0]
        res_set = self.db.execute_query("SELECT DATE(created_at), content FROM journal_entries WHERE user_id = (%s)", [(user_id)])
      u.log_event("INFO", "Fetched journal entries", user_id)
      return res_set
    except Exception as e:
      self.db.rollback()
      u.log_event("ERROR", "Error fetching journal entries", user_id)
      print("Error fetching journal entries. Please try again.\n")
    finally:
      self.db.close()
  
  def query_users(self):
    try:
      res_set = self.db.execute_query("SELECT id, user_name, role FROM users")
      u.log_event("INFO", "Fetched all users", 1) # Assuming admin user_id is 1
      return res_set
    except Exception as e:
      self.db.rollback()
      u.log_event("ERROR", "Error fetching users", 1) # Assuming admin user_id is 1
      print("Error fetching users. Please try again.\n")

  #update
  def update(self, entry_id, new_content):
    try:
      self.db.execute_query("UPDATE journal_entries SET content = %s WHERE id = %s", (new_content, entry_id))
      u.log_event("INFO", "Edited journal entry", 1)
      print("Journal entry changed successfully!\n")
    except Exception as e:
      self.db.rollback()
      u.log_event("ERROR", "Error editing journal entry", 1)
      print("Error editing journal entry. Please try again.\n")
    finally:
      self.db.close()

  #delete
  def delete(self, entry_id):
    try:
      self.db.execute_query("DELETE FROM journal_entries WHERE id = (%s)", [(entry_id)])
      u.log_event("INFO", "Deleted journal entry", 1)
      print(f"Journal entry {entry_id} deleted successfully!\n")
    except Exception as e:
      self.db.rollback()
      u.log_event("ERROR", "Error deleting journal entry", 1)
      print("Error deleting journal entry.\n")
    finally:
      self.db.close()
  
  def delete_user(self, user_id):
    try:
      self.db.execute_query("DELETE FROM users WHERE id = (%s)", [(user_id)])
      u.log_event("INFO", f"Deleted user {user_id}", 1)
      print(f"User {user_id} deleted successfully!\n")
    except Exception as e:
      if e.errno == 1451:  # Foreign key constraint fails
        u.log_event("ERROR", f"Cannot delete user {user_id} due to existing journal entries", 1)
        print("Error: Cannot delete user due to existing journal entries.\n")
        return
      else:
        self.db.rollback()
        u.log_event("ERROR", "Error deleting user", 1)
        print("Error deleting user.\n")
    finally:
      self.db.close()

  def close_connection(self):
    self.db.close()

