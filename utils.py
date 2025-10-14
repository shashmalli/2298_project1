from dbms import DatabaseManager
# import logging

USER = "root"
PASSWORD = "shashank935"

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG, 
#                     format='%(asctime)s - %(levelname)s: %(message)s')

def log_event(level, message, user_id):
  try:
    db = DatabaseManager(USER, PASSWORD, "localhost", "journal_2298_p1")
    query = "INSERT INTO log (level, user_id, action) VALUES (%s, %s, %s)"
    db.execute_query(query, (level, user_id, message))
  except Exception as e:
    db.rollback()
    print(f"Failed to log event: {e}")
  finally:
    db.close