import logging
from dbms import DatabaseManager
from JournalEntry import JournalEntry

class Journal:
  def __init__(self):
    self.db = DatabaseManager

  def add_entry(self, text, date):
    entry = JournalEntry()
    # with open(self.filename, "a") as f:
    #   f.write(f"\n>{entry.date}\n{entry.entry}\n")
    entry.insert_into
  
  def write_from_file(self, file):
    try:
      if file.lower().endswith(".csv"):
        with open(file, newline="") as f:
          lines = list(csv.DictReader(f))
      elif file.lower().endswith(".json"):
        with open(file, "r") as f:
          lines = json.load(f)
      else:
        raise ValueError
    except ValueError:
      print("Warning: Unsupported file type (must be .csv or .json)\n")
    except FileNotFoundError:
      print("Warning: File does not exist\n")
    else:
      with open(self.filename, "a") as j:
        for line in lines:
          entry = JournalEntry(line['entry'], line['date'])
          j.write(f"\n>{entry.date}\n{entry.entry}\n")

  def read_entries(self):
    # with open(self.filename, "r") as f:
    #   print("===== Journal =====\n")
    #   print(f.read())
    entry = JournalEntry()
    entry.query()
  
  def create_user(self, username, password):
    entry = JournalEntry()
    entry.insert_into()
    # insert into sql
