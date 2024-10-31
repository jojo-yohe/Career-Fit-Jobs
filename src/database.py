import os
from supabase import create_client, Client
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def init_db():
    # This function might not be necessary if Supabase handles schema creation
    logger.info("Database connection initialized")

def add_user(user_id: int) -> bool:
    try:
        response = supabase.table('users').insert({"user_id": user_id}).execute()
        if len(response.data) > 0:
            logger.info(f"User {user_id} added successfully")
            return True
        else:
            logger.warning(f"Failed to add user {user_id}")
            return False
    except Exception as e:
        logger.error(f"Error adding user {user_id}: {e}")
        return False

def update_user_preferences(user_id: int, preferences: list):
    try:
        supabase.table('users').update({"preferences": preferences}).eq("user_id", user_id).execute()
        logger.info(f"Preferences updated for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating preferences for user {user_id}: {e}")

def get_user_preferences(user_id: int) -> list:
    try:
        response = supabase.table('users').select("preferences").eq("user_id", user_id).execute()
        if len(response.data) > 0:
            return response.data[0]['preferences']
        else:
            logger.warning(f"No preferences found for user {user_id}")
            return []
    except Exception as e:
        logger.error(f"Error getting preferences for user {user_id}: {e}")
        return []

def add_job_listing(channel: str, summary: str, message_id: int, message_link: str):
    try:
        supabase.table('job_listings').insert({
            'channel': channel,
            'summary': summary,
            'message_id': message_id,
            'message_link': message_link
        }).execute()
        logger.info(f"Job listing added from {channel}, message ID: {message_id}")
    except Exception as e:
        logger.error(f"Error adding job listing: {e}")

def get_job_listings():
    try:
        response = supabase.table('job_listings').select('*').execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting job listings: {e}")
        return []

def clear_job_listings():
    try:
        supabase.table('job_listings').delete().neq('id', 0).execute()
        logger.info("Job listings cleared")
    except Exception as e:
        logger.error(f"Error clearing job listings: {e}")

def get_all_users():
    try:
        response = supabase.table('users').select('user_id').execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

if __name__ == '__main__':
    # You can add test code here to verify database operations
    pass
