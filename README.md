# College Football Quiz App

A web-based quiz application for college football trivia.

## Setup

1. Clone this repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add a secret key:
   ```bash
   # Generate a secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Add the generated key to your .env file
   echo "SECRET_KEY=your-generated-key-here" > .env
   ```

4. Run the application:
   ```bash
   python app.py
   ```

Visit `http://127.0.0.1:5000` in your browser.

## Features

- Interactive college football quiz
- Team information

## Technologies Used

- Flask (Python web framework)
- SQLite (Database)
- HTML/CSS
