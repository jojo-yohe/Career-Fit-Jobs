import logging
import sys
from telegram.ext import Application
from config import TOKEN, JOB_CATEGORIES
from database import get_all_users, get_job_listings, get_user_preferences, clear_job_listings
from message_formatter import create_job_update
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def match_jobs_with_preferences(jobs, preferences):
    matched_jobs = defaultdict(list)
    for job in jobs:
        job_summary_lower = job['summary'].lower()
        for pref in preferences:
            pref_keywords = pref.lower().split('/')
            if any(keyword in job_summary_lower for keyword in pref_keywords):
                matched_jobs[pref].append(job)
                break
    return matched_jobs

async def send_job_updates():
    logger.info("Starting send_job_updates function")
    try:
        application = Application.builder().token(TOKEN).build()
        logger.info("Application built successfully")
        
        job_listings = get_job_listings()
        logger.info(f"Retrieved {len(job_listings)} job listings")
        
        if job_listings:
            users = get_all_users()
            logger.info(f"Retrieved {len(users)} users")
            
            for user in users:
                logger.info(f"Processing user {user['user_id']}")
                user_preferences = get_user_preferences(user['user_id'])
                if user_preferences:
                    logger.info(f"User preferences: {user_preferences}")
                    matched_jobs = match_jobs_with_preferences(job_listings, user_preferences)
                    if matched_jobs:
                        logger.info(f"Found {sum(len(jobs) for jobs in matched_jobs.values())} matched jobs")
                        summary_text = "📊 <b>This Week's Career Fit Jobs</b>\n\n"
                        for category in JOB_CATEGORIES:
                            if category in matched_jobs:
                                jobs = matched_jobs[category]
                                channels = set(job['channel'] for job in jobs)
                                summary_text += f"🔹 <b>{category}</b> - found {len(jobs)} matching jobs from channels:\n"
                                for channel in channels:
                                    summary_text += f"    • {channel}\n"
                                summary_text += "\n"
                        
                        update_url = create_job_update(matched_jobs)
                        
                        message = (
                            "📊 Job Updates Summary\n"
                            f"{summary_text}\n"
                            "➖➖➖➖➖➖➖➖\n"
                            f"🔍 [View Full Details]({update_url})"
                        )
                        
                        await application.bot.send_message(
                            chat_id=user['user_id'], 
                            text=message, 
                            parse_mode='Markdown',
                            disable_web_page_preview=True
                        )
                        logger.info(f"Sent update to user {user['user_id']}")
                        await clear_job_listings()
                    else:
                        logger.info(f"No matching jobs found for user {user['user_id']}")
                else:
                    logger.info(f"No preferences found for user {user['user_id']}")
        else:
            logger.info("No job listings found")
    except Exception as e:
        logger.error(f"Error in send_job_updates: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Script started")
    import asyncio
    asyncio.run(send_job_updates())
    logger.info("Script finished")
