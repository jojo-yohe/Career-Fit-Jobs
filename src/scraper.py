import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE
from database import store_job_listing
import logging

logger = logging.getLogger(__name__)

async def scrape_jobs():
    try:
        logger.info("Starting job scraping...")
        client = TelegramClient('session_name', API_ID, API_HASH)
        await client.start(phone=PHONE)
        
        # Your scraping logic here
        channels = ['channel1', 'channel2']  # Your channel list
        for channel in channels:
            try:
                messages = await client.get_messages(channel, limit=50)
                for msg in messages:
                    store_job_listing(channel, msg.text, msg.id, msg.link)
            except Exception as e:
                logger.error(f"Error scraping channel {channel}: {e}")
                continue
                
        await client.disconnect()
        logger.info("Job scraping completed")
    except Exception as e:
        logger.error(f"Error in scrape_jobs: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(scrape_jobs())
