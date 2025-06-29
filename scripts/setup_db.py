import sys
import os

# TODO Delete later
# absolute path of current file is /Users/lynda/Code/CFB_quiz/scripts/setup_db.py
# dirname is /scripts
# outer dirname is /CFB_quiz
# sys.path is a list of directories where Python looks for modules
# /CFB quiz is a added to the list of directories to that search directory

# Add parent directory to path so that we can import database
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import CFBDatabase

def setup_database():
    print("Setting up CFB Quiz database")

    db = CFBDatabase()

    # Create database structure
    db.create_database()

    # Fetch and populate data
    teams_data = db.fetch_teams_data()

    if teams_data:
        db.populate_database(teams_data)
        print("Database setup complete!")
    else:
        print("Failed to fetch data from API")

if __name__ == "__main__":
    setup_database()