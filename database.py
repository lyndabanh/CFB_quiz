import sqlite3
import requests
import os
from config import Config

class CFBDatabase:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.headers = {
        'Authorization': f'Bearer {Config.CFB_API_KEY}',
        'accept': 'application/json'
        }

    def create_database(self):
        """Create the database and tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school TEXT NOT NULL UNIQUE,
                mascot TEXT,
                conference TEXT,
                division TEXT,
                color TEXT,
                alt_color TEXT,
                logo_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create an index on school name for faster lookups
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_school ON teams(school)')

        conn.commit()
        conn.close()
        print("Database and tables created successfully")
    
    def drop_database(self):
        """Drop (delete) the database file"""
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print(f"Database {self.db_path} deleted successfully")
        except Exception as e:
            print(f"Error deleting database: {e}")

    def fetch_teams_data(self):
        """Fetch teams data from College Football Data API"""
        try:
            # Get teams data
            response = requests.get(f'{Config.CFB_API_BASE_URL}/teams', headers=self.headers)
            response.raise_for_status()
            teams_data = response.json()

            print(f"Fetched {len(teams_data)} teams from API")
            return teams_data
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []
        
    def populate_database(self, teams_data):
        """Populate the database with teams data"""
        if not teams_data:
            print("No data to populate")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Insert teams data
        for team in teams_data:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO teams
                    (school, mascot, conference, division, color, alt_color, logo_url, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    team.get('school'),
                    team.get('mascot'),
                    team.get('conference'),
                    team.get('division'),
                    team.get('color'),
                    team.get('alt_color'),
                    team.get('logos')[0] if team.get('logos') and len(team.get('logos')) > 0 else None
                ))
            except sqlite3.Error as e:
                print(f"Error inserting team {team.get('school', 'Unknown')}: {e}")
            
        conn.commit()

        # Get count of inserted records
        cursor.execute('SELECT COUNT(*) FROM teams')
        count = cursor.fetchone()[0]
        print(f"Database populated with {count} teams")

        conn.close()

    def query_teams(self, limit=10):
        """Query and display some teams data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT school, mascot, conference, division, color, alt_color
            FROM teams
            WHERE conference IS NOT NULL
            ORDER BY school
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()

        print(f"\nSample of {len(results)} teams:")
        print("-" * 80)
        for row in results:
            print(f"School: {row[0]}")
            print(f"Mascot: {row[1]}")
            print(f"Conference: {row[2]}")
            print(f"Division: {row[3]}")
            print(f"Colors: {row[4]} / {row[5]}")
            print("-" * 40)

        conn.close()
    
    def get_quiz_question_data(self):
        """Get random team data for quiz questions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get random team
        cursor.execute('''
            SELECT school, mascot, conference, color, logo_url
            FROM teams
            WHERE mascot is NOT NULL
                AND conference IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 1
        ''')

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'school': result[0],
                'mascot': result[1],
                'conference': result[2],
                'color': result[3],
                'logo_url': result[4]
            }
        return {}
    
    def get_data_for_four_teams(self):
        """Get random team data for four teams"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get random team
        cursor.execute('''
            SELECT school, mascot, conference, color, logo_url
            FROM teams
            WHERE mascot IS NOT NULL
                AND conference IS NOT NULL
            ORDER BY RANDOM()
            LIMIT 4
        ''')

        results = cursor.fetchall()
        conn.close()

        if results:
            teams = []
            for result in results:
                team = {
                    'school': result[0],
                    'mascot': result[1],
                    'conference': result[2],
                    'color': result[3],
                    'logo_url': result[4] 
                }
                teams.append(team)
            return teams
        return []

# # Usage example
# def main():
#     # Initializa database
#     db = CFBDatabase()

#     # Drop existing database (stale)
#     print("Deleting old database...")
#     db.drop_database()

#     # Create database structure
#     print("Creating database...")
#     db.create_database()

#     # Fetch data from API
#     teams_data = db.fetch_teams_data()

#     if teams_data:
#         # Populate database
#         print("\nQuerying database...")
#         db.populate_database(teams_data)

#         # Display some results
#         print("\nQuerying database...")
#         db.query_teams()

#         # Test quiz functionality
#         print("\nSample quiz question data:")
#         quiz_data = db.get_quiz_question_data()
#         if quiz_data:
#             print(f"Question: What is the mascot of {quiz_data['school']}?")
#             print(f"Answer: {quiz_data['mascot']}")
#         else:
#             print("Failed to fetch data from API ")

# if __name__ == "__main__":
#     main()
        