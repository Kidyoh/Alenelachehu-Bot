import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from database import get_user_profile, save_sos, update_user_profile, save_vent
from states import *
from Components.help_components import how_to_use
from utils import create_menu_keyboard

from Components.profile import my_profile
from Components.information_components import rules
from Components.information_components import help_menu
from Components.information_components import about
from Components.sos import sos


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    buttons = [
        ("How to use the bot", 'how_to_use'),
        ("Start Venting", 'start_venting'),
        ("My Profile", 'my_profile'),
        ("Rules and Regulation", 'rules'),
        ("Help", 'help'),
        ("About Alenelachehu", 'about'),
        ("SOS", 'sos')
    ]
    keyboard = create_menu_keyboard(buttons)
    await update.effective_message.reply_text('Welcome to Alenelachehu venting platform. Please choose an option:', reply_markup=keyboard)

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from Components.venting_components import start_venting
    query = update.callback_query
    await query.answer()

    if query.data == 'how_to_use':
        await how_to_use(update, context)
        return HOW_TO_USE
    elif query.data == 'start_venting':
        await start_venting(update, context)
        return START_VENTING
    elif query.data == 'my_profile':
        await my_profile(update, context)
        return MY_PROFILE
    elif query.data == 'rules':
        await rules(update, context)
        return RULES
    elif query.data == 'help':
        await help_menu(update, context)
        return HELP
    elif query.data == 'about':
        await about(update, context)
        return ABOUT
    elif query.data == 'sos':
        await sos(update, context)
        return SOS_LOCATION
    elif query.data == 'main_menu':
        await show_main_menu(update, context)
        return MAIN_MENU