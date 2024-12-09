import logging
import os
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from states import *

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
    from Components.main_menu import show_main_menu
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
    # Log the information
    logger.info("SOS request received:")
    logger.info(f"Location: Latitude {location.latitude}, Longitude {location.longitude}")
    logger.info(f"Voice message duration: {voice_message.duration} seconds")
    logger.info(f"Photo dimensions: {photo.width}x{photo.height}")

    # Prepare data for Appwrite
    data = {
        "location": {
            "latitude": location.latitude,
            "longitude": location.longitude
        },
        "voice_message": {
            "file_id": voice_message.file_id,
            "duration": voice_message.duration
        },
        "photo": {
            "file_id": photo.file_id,
            "width": photo.width,
            "height": photo.height
        },
        "timestamp": datetime.now().isoformat()
    }

    # Send data to Appwrite
    send_to_appwrite(data)

def send_to_appwrite(data):
    client = Client()
    client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
    client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
    client.set_key(os.getenv('APPWRITE_API_KEY'))

    databases = Databases(client)
    database_id = os.getenv('DATABASE_ID')
    collection_id = os.getenv('COLLECTION_ID')

    document_data = {
        "location": data['location'],
        "voice_message": data['voice_message'],
        "photo": data['photo'],
        "timestamp": data['timestamp']
    }
    print('Inserting document:', document_data)
    try:
        result = databases.create_document(
            database_id,
            collection_id,
            ID.unique(),
            document_data
        )
        print(f"Document inserted successfully. Document ID:", result['$id'])
    except Exception as error:
        print('Error inserting document:', error)