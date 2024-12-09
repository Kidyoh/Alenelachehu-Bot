import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from database import get_user_profile, save_sos, update_user_profile, save_vent
from states import *
from utils import create_menu_keyboard




async def how_to_use(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'how_to_use':
        buttons = [
            ("How to vent", 'how_to_vent'),
            ("How to report comment", 'how_to_report'),
            ("How to contact Alenelachehu", 'how_to_contact'),
            ("How to view/edit profile", 'how_to_profile'),
            ("View Rules", 'view_rules'),
            ("Back to Main Menu", 'main_menu')
        ]
        keyboard = create_menu_keyboard(buttons)
        await query.edit_message_text('How to use the bot:', reply_markup=keyboard)
    elif query.data in ['how_to_vent', 'how_to_report', 'how_to_contact', 'how_to_profile', 'view_rules']:
        await globals()[query.data](update, context)
    return HOW_TO_USE

async def how_to_vent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("To vent, simply click on the 'Start Venting' button in the main menu. "
            "You can type out your thoughts and feelings, and choose whether to allow reactions, comments, or professional feedback.")
    keyboard = create_menu_keyboard([("Back to How to Use", 'how_to_use')])
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

async def how_to_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("To report a comment, simply click on the 'Report' button next to the comment you wish to report. "
            "You will be prompted to provide a reason for the report.")
    keyboard = create_menu_keyboard([("Back to How to Use", 'how_to_use')])
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

async def how_to_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("To contact Alenelachehu, you can reach out through the following channels:\n"
            "Email: Alenelachehuco@gmail.com\n"
            "Website: www.Alenelachehu.org\n"
            "Phone: +251965579192 or +251919186182\n"
            "Telegram: https://t.me/Alenelachehu\n"
            "LinkedIn: https://www.linkedin.com/company/alenelachehu-charitable-organization/\n"
            "WhatsApp: https://chat.whatsapp.com/KzPWHuG4m3LG7DB7uXVdKZ\n"
            "Facebook: https://www.facebook.com/profile.php?id=100081094233970")
    keyboard = create_menu_keyboard([("Back to How to Use", 'how_to_use')])
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

async def how_to_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("To view or edit your profile, click on the 'My Profile' button in the main menu. "
            "You can set or update your nickname, age, nationality, and other details.")
    keyboard = create_menu_keyboard([("Back to How to Use", 'how_to_use')])
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)