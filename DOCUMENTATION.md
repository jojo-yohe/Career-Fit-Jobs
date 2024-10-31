# Telegram Job Search Bot Documentation

## Project Structure

Carrer-Fit-Job-bot/
├── src/
│ ├── bot.py
│ ├── scraper.py
│ ├── main.py
│ ├── config.py
│ ├── database.py
│ ├── message_formatter.py
│ └── policy.py
├── tests/
│ └── test_.py
├── .github/
│ └── workflows/
│ └── job_update.yml
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
└── .env

## Components

### bot.py
Handles the Telegram bot interface, including user interactions and preference settings.

### scraper.py
Manages the scraping of job listings from specified Telegram channels.

### main.py
The entry point of the application, coordinating the bot and scraper operations.

### config.py
Contains configuration variables and constants used throughout the project.

### database.py
Manages interactions with the Supabase database for storing user preferences and job listings.

### message_formatter.py
Formats job listings and promotional content using Telegraph.

### policy.py
Generates and manages the privacy policy for the bot.

## Workflow

1. The scraper runs periodically (3 times a day) to collect job listings from specified channels.
2. Job listings are stored in the Supabase database.
3. The bot sends personalized job updates to users based on their preferences.
4. After sending updates, the database is cleared to maintain efficiency.

## Database Schema

### Users Table
- user_id (primary key)
- preferences (JSON array)
- created_at
- updated_at

### Job Listings Table
- id (primary key)
- channel
- summary
- full_text
- message_id
- created_at

## Deployment

The bot is deployed using GitHub Actions, which automates the scraping and update processes.

## Error Handling

Errors are logged using Python's logging module. Critical errors trigger alerts to the admin.

## Future Improvements

- Implement more advanced text analysis for job matching
- Add support for multiple languages
- Introduce a feedback system for job listings
