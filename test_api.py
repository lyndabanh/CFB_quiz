import requests
import json

API_KEY = '3i4/ize2rvcXWTkbBrr1i94H8N6eredbrnJW7LdtKQHkp5bN1Q/TRbnUmwOLxHhy'
BASE_URL = 'https://api.collegefootballdata.com'

def test_api_connection():
    url = f'{BASE_URL}/teams'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'accept': 'application/json'
    }

    try:
        print("Testing API connection ...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("API connection succesful!")
            teams = response.json()
            print(f"Retrieved {len(teams)} teams")
            return teams
        
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def explore_team_data(teams, limit=5):
    if not teams:
        return
    
    print(f"\n--- Sample Team Data (first {limit} teams) ---")
    for i, team in enumerate(teams[:limit]):
        print(f"\nTeam {i+1}:")
        for key, value in team.items():
            print(f"{key}: {value}")

def find_teams_by_conference(teams, conference_name):
    if not teams:
        return []
    
    matching_teams = [team for team in teams if (team.get('conference') or '').lower() == conference_name.lower()]
    
    return matching_teams

def get_quiz_relevant_data(teams, limit=10):
    if not teams:
        return []
    
    quiz_data = []
    for team in teams[:limit]:
        team_info = {
            'school': team.get('school', 'N/A'),
            'mascot': team.get('mascot', 'N/A'),
            'conference': team.get('conference', 'N/A'),
            'division': team.get('division', 'N/A'),
            'color': team.get('color', 'N/A'),
            'alt_color': team.get('alt_color', 'N/A'),
            'logos': team.get('logos', []),
        }

        quiz_data.append(team_info)

    return quiz_data

def main():
    data = test_api_connection()

    # explore_team_data(data)

    # conference_name = 'SEC'
    # matching_teams = find_teams_by_conference(data, conference_name)
    # print(f'{conference_name} teams:')
    # for team in matching_teams:
    #     print(team['school'])

    print(get_quiz_relevant_data(data))
    quiz_data = get_quiz_relevant_data(data)
    for i, team in enumerate(quiz_data):
        print(f'\nTeam {i+1}:')
        for key, value in team.items():
            print(f'{key}: {value}')


if __name__ == '__main__':
    main()
    