import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from states import *
from Components.main_menu import show_main_menu
from database import save_sos


logger = logging.getLogger(__name__)

async def sos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("Share Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.callback_query.answer()
    await update.callback_query.message.reply_text('This is an SOS situation. Please share your location:', reply_markup=reply_markup)
    
    return SOS_LOCATION

async def sos_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_location = update.message.location
    context.user_data['sos_location'] = user_location
    await update.message.reply_text('Location received. Please send a 10-second voice message describing your situation.')
    return SOS_VOICE

async def sos_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    voice_message = update.message.voice
    context.user_data['sos_voice'] = voice_message
    await update.message.reply_text('Voice message received. If possible, please send a photo of your surroundings.')
    return SOS_PHOTO

async def sos_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo = update.message.photo[-1]
    context.user_data['sos_photo'] = photo

    acknowledgment = "Thank you for providing the information. We have received:\n"
    acknowledgment += "✅ Your location\n"
    acknowledgment += "✅ Your voice message\n"
    acknowledgment += "✅ Your photo\n\n"
    acknowledgment += "We are processing your SOS request and will respond as soon as possible. Stay safe."


    await update.message.reply_text(acknowledgment)

    # Send SOS message with location, voice message, and photo
    await send_sos(context.user_data['sos_location'], context.user_data['sos_voice'], context.user_data['sos_photo'], context)
    
    # Return to main menu
    await show_main_menu(update, context)
    return MAIN_MENU

async def send_sos(location, voice_message, photo, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Here you would implement the logic to send the SOS information to the appropriate responders
    # For now, we'll just log the information
    logger.info("SOS request received:")
    logger.info(f"Location: Latitude {location.latitude}, Longitude {location.longitude}")
    logger.info(f"Voice message duration: {voice_message.duration} seconds")
    logger.info(f"Photo dimensions: {photo.width}x{photo.height}")
