import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import TOKEN, JOB_CATEGORIES
from database import add_user, update_user_preferences, get_user_preferences, add_pending_user
from policy import get_privacy_policy_url
from message_formatter import create_job_update, create_promotion_banner
from telegram.error import BadRequest
from datetime import datetime, time
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_PREFERENCES = 15

async def check_bot_availability(update: Update) -> bool:
    is_sleeping, sleep_message = is_bot_sleeping()
    if is_sleeping:
        await update.message.reply_text(sleep_message, parse_mode='Markdown')
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_bot_availability(update):
        return
    user = update.effective_user
    is_new_user = add_user(user.id)
    
    privacy_url = get_privacy_policy_url()
    welcome_message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "Let's set up your job preferences.\n\n"
        f"Please read our Privacy Policy:\n{privacy_url}"
    )
    await update.message.reply_text(welcome_message)
    
    await show_preference_menu(update, context)

async def preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_bot_availability(update):
        return
    await show_preference_menu(update, context)

async def show_preference_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_preferences = get_user_preferences(user_id)
    
    keyboard = []
    row = []
    for i, category in enumerate(JOB_CATEGORIES, 1):
        icon = "✅" if category in user_preferences else "⬜️"
        row.append(InlineKeyboardButton(f"{icon} {category}", callback_data=f"pref_{category.lower().replace(' ', '_').replace('/', '_')}"))
        
        if i % 3 == 0 or i == len(JOB_CATEGORIES):
            keyboard.append(row)
            row = []
    
    keyboard.append([InlineKeyboardButton("Submit", callback_data="pref_submit")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (f"Please select up to {MAX_PREFERENCES} job preferences:\n"
               f"(You have selected {len(user_preferences)}/{MAX_PREFERENCES})")
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=message, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_bot_availability(update):
        return
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == "pref_submit":
        await submit_preferences(update, context)
    else:
        category = query.data.replace("pref_", "").replace("_", " ").title()
        current_preferences = set(get_user_preferences(user_id))
        
        if category in current_preferences:
            current_preferences.remove(category)
        elif len(current_preferences) < MAX_PREFERENCES:
            current_preferences.add(category)
        else:
            await query.answer(f"You can only select up to {MAX_PREFERENCES} preferences. Please remove one before adding another.", show_alert=True)
            return
        
        update_user_preferences(user_id, list(current_preferences))
        await show_preference_menu(update, context)

async def submit_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    preferences = get_user_preferences(user_id)
    formatted_preferences = "\n".join([f"• {pref}" for pref in preferences])
    message = f"Your preferences have been updated:\n\n{formatted_preferences}"
    await update.callback_query.edit_message_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_bot_availability(update):
        return
    help_text = (
        "✨ *Career Fit Job Bot*\n\n"
        "🔍 *Available Commands:*\n"
        "• /start - Start the bot, Privacy Policy & set preferences\n"
        "• /preferences - Update your job categories\n"
        "• /help - Show this help message\n\n"
        "📬 *Updates Schedule:*\n"
        "You'll receive job matches 3 times daily\n"
        "• Morning Update: 8:30 AM\n"
        "• Afternoon Update: 4:30 PM\n"
        "• Night Update: 12:30 AM\n\n"
        "💡 *Need Help?*\n"
        "Contact: @cfjsupport"
    )
    await update.message.reply_text(help_text)

async def send_job_updates(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implement the logic to send job updates here
    # This function will be called every 8 hours by the job queue
    pass

def is_bot_sleeping() -> tuple[bool, str]:
    ethiopia_tz = pytz.timezone('Africa/Addis_Ababa')
    current_time = datetime.now(ethiopia_tz)
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Night sleep (1 AM - 7 AM)
    if 1 <= current_hour < 7:
        return True, (
            "😴 *Bot is having its night sleep*\n\n"
            "Will be back at 7:00 AM EAT\n"
            "Regular hours: 7:00 AM - 1:00 AM"
        )

    # Hourly breaks
    break_hours = {
        9: "10:00 AM",   # 9-10 AM break
        12: "1:00 PM",   # 12-1 PM break
        15: "4:00 PM",   # 3-4 PM break
        18: "7:00 PM",   # 6-7 PM break
        21: "10:00 PM",  # 9-10 PM break
        0: "1:00 AM"     # 12-1 AM break
    }

    if current_hour in break_hours:
        return True, (
            "🔄 *Bot is taking a short break*\n\n"
            f"Will be back at {break_hours[current_hour]} EAT\n"
            "Thanks for your patience!"
        )

    return False, ""

def setup_handlers(application: Application) -> None:
    """Setup bot handlers"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("preferences", preferences))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Add other handlers here

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    setup_handlers(application)

    application.run_polling()

if __name__ == '__main__':
    main()
