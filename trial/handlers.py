import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from database import get_user_profile, save_sos, update_user_profile, save_vent
from states import *
from trial.Components.main_menu import show_main_menu
from utils import create_menu_keyboard


logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data['user_id'] = user.id
    await show_main_menu(update, context)
    return MAIN_MENU










async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
