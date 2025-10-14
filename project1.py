import getpass
from JournalEntry import JournalEntry
from User import User
from dbms import DatabaseManager
import utils as u

def register():
  new_username = input("Enter desired username: ").strip()
  passwd = getpass.getpass("Enter desired password: ").strip()
  conf_passwd = getpass.getpass("Confirm password: ").strip()
  if passwd != conf_passwd:
    print("Passwords do not match\n")
    return
  usr = User(new_username, role="user")
  new_usr = usr.create_user(passwd)
  usr.close_connection()
  if new_usr:
    journal_menu(usr)

def login():
  usrnm = input("Enter username: ").strip()
  pwd = getpass.getpass("Enter password: ").strip()

  usr = User(usrnm)
  if usr.authenticate(usrnm, pwd):
    if usrnm == "admin" :
      admin_menu(usr)
    else:
      journal_menu(usr)
  else:
    print("Login failed. Please try again.\n")
    login()
  usr.close_connection()

def edit_entry(journal_entry, user):
  if user.username == "admin":
    entries_list = journal_entry.custom_query("SELECT j.id, DATE(created_at), content, u.user_name FROM journal_entries AS j JOIN users AS u ON j.user_id = u.id", [])
    print("=== All Journal Entries ===\n")
    for entry in entries_list:
      print("ID:", entry[0], "\nDate:", entry[1], "\nUser:", entry[3], "\nContent:", entry[2], "\n")
  else:
    entries_list = journal_entry.custom_query("SELECT j.id, DATE(created_at), content FROM journal_entries AS j JOIN users AS u ON j.user_id = u.id WHERE u.user_name = %s", [(user.username)])
    print("=== Your Journal ===\n")
    for entry in entries_list:
      print("ID:", entry[0], "\nDate:", entry[1], "\nContent:", entry[2], "\n")
  change_id = input("Enter the ID of the journal entry you want to edit: ").strip()
  new_content = input("Enter new content for the journal entry: ").strip()
  journal_entry.update(change_id, new_content)


def journal_menu(user):
  while True:
    usr_in = input("What would you like to do?\n(R) Read journal entries\n(W) Add journal entry\n"
                   "(E) Edit entries\n(Q) Quit\n")
    
    je = JournalEntry()
    if usr_in.upper() == "R":
      entries_list = je.query(user.username)
      print("=== Your Journal ===\n")
      for entry in entries_list:
        print(">", entry[0], "\n", entry[1], "\n")
      print("====================")
    elif usr_in.upper() == "W":
      content = input("Start your journal entry: ").strip()
      je.insert_into(user.username, content)
    elif usr_in.upper() == "E":
      edit_entry(je, user)
    elif usr_in.upper() == "Q":
      print("Goodbye!")
      break
    else:
      print("You must enter a letter for one of the options")
  
def admin_menu(user):
  while True:
    usr_in = input("What would you like to do?\n(U) View Users\n(X) Remove Users\n(R) Read journal entries\n"
                   "(E) Edit entries\n(D) Delete entries\n(Q) Quit\n")
    
    je = JournalEntry()
    if usr_in.upper() == "U":
      users_list = je.query_users()
      print("=== Users ===\n")
      for usr in users_list:
        print(f"ID: {usr[0]}, Username: {usr[1]}, Role: {usr[2]}")
      print("===============")
      je.close_connection()
    elif usr_in.upper() == "X":
      users_list = je.query_users()
      print("=== Users ===\n")
      for usr in users_list:
        print(f"ID: {usr[0]}, Username: {usr[1]}, Role: {usr[2]}")
      print("===============")
      to_delete = input("Enter the ID of the user you want to delete: ").strip()
      je.delete_user(to_delete)
    elif usr_in.upper() == "R":
      entries_list = je.query(user.username)
      print("=== Journal ===\n")
      for entry in entries_list:
        print(f">{entry[0]}\nUser {entry[2]}- {entry[1]} \n")
      print("===============")
    elif usr_in.upper() == "E":
      edit_entry(je, user)
    elif usr_in.upper() == "D":
      to_delete = input("Enter the ID of the entry you want to delete: ").strip()
      je.delete(to_delete)
    elif usr_in.upper() == "Q":
      print("Goodbye!")
      break
    else:
      print("You must enter a letter for one of the options")

def main():
  # db = DatabaseManager(u.USER, u.PASSWORD, "localhost", "journal_2298_p1")
  
  usr_in = input("What would you like to do?\n(R) Register\n(L) Login\n(Q) Quit\n")
  if usr_in.upper() == "R":
    register()
  elif usr_in.upper() == "L":
    login()
  elif usr_in.upper() == "Q":
    print("Goodbye!")
    return
  else:
    print("You must enter a letter for one of the options")
    main()


if __name__ == "__main__":
  main()
