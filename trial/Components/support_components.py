from telegram import Update
from telegram.ext import ContextTypes
import logging
from states import *
from Components.information_components import help_menu
from Components.main_menu import show_main_menu
from utils import create_menu_keyboard

logger = logging.getLogger(__name__)


async def professional_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("If you need professional support, we're here to help. "
            "Please choose your preferred method of support:")
    buttons = [
        ("Online Support", 'online_support'),
        ("In-Person Support", 'in_person_support'),
        ("Back to Help Menu", 'help')
    ]
    keyboard = create_menu_keyboard(buttons)
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return PROFESSIONAL_SUPPORT

async def support_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Support groups can be a great way to connect with others who understand what you're going through. "
            "Please choose your preferred type of support group:")
    buttons = [
        ("Online Support Group", 'online_group'),
        ("In-Person Support Group", 'in_person_group'),
        ("Back to Help Menu", 'help')
    ]
    keyboard = create_menu_keyboard(buttons)
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return SUPPORT_GROUP


async def handle_professional_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'online_support':
        text = ("For online professional support, please provide the following information:\n"
                "1. Your full name\n"
                "2. Your age\n"
                "3. Preferred date and time for the session\n"
                "4. Brief description of your concern\n\n"
                "Please send this information in a single message.")
        await query.edit_message_text(text=text)
        return PROFESSIONAL_SUPPORT
    elif query.data == 'in_person_support':
        text = ("For in-person professional support, please provide the following information:\n"
                "1. Your full name\n"
                "2. Your age\n"
                "3. Your location (city/region)\n"
                "4. Preferred date and time for the session\n"
                "5. Brief description of your concern\n\n"
                "Please send this information in a single message.")
        await query.edit_message_text(text=text)
        return PROFESSIONAL_SUPPORT
    elif query.data == 'help':
        await help_menu(update, context)
        return HELP

async def handle_support_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'online_group':
        text = ("To join an online support group, please follow these steps:\n"
                "1. Join our Telegram channel: https://t.me/Alenelachehu\n"
                "2. Check the pinned message for upcoming online support group sessions\n"
                "3. RSVP for the session you'd like to attend\n\n"
                "We'll send you further instructions before the session begins.")
    elif query.data == 'in_person_group':
        text = ("To join an in-person support group, please provide the following information:\n"
                "1. Your full name\n"
                "2. Your age\n"
                "3. Your location (city/region)\n"
                "4. Preferred days of the week for meetings\n\n"
                "Please send this information in a single message.")
    elif query.data == 'help':
        await help_menu(update, context)
        return HELP

    keyboard = create_menu_keyboard([("Back to Help Menu", 'help')])
    await query.edit_message_text(text=text, reply_markup=keyboard)
    return SUPPORT_GROUP

async def process_professional_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    support_request = update.message.text

    # For now, we'll just log it
    logger.info(f"Professional support request from user {user_id}: {support_request}")

    response_text = ("Thank you for reaching out for professional support. "
                     "We have received your request and will contact you soon with further details.")
    await update.message.reply_text(response_text)
    await show_main_menu(update, context)
    return MAIN_MENU

async def process_support_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    group_request = update.message.text

    # For now, we'll just log it
    logger.info(f"Support group request from user {user_id}: {group_request}")

    response_text = ("Thank you for your interest in joining a support group. "
                     "We have received your information and will contact you soon with available group options.")
    await update.message.reply_text(response_text)
    await show_main_menu(update, context)
    return MAIN_MENU