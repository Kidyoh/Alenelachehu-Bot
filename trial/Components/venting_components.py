from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from database import save_vent
from states import *
from trial.Components.main_menu import show_main_menu
from utils import create_menu_keyboard



async def start_venting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text('Please start typing your thoughts. When you\'re done, send /done')
    return VENTING

async def venting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '/done':
        context.user_data['vent_content'] = context.user_data.get('vent_content', '')
        await vent_options(update, context)
        return VENT_OPTIONS
    else:
        context.user_data['vent_content'] = context.user_data.get('vent_content', '') + update.message.text + '\n'
        return VENTING

async def vent_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ("Allow reactions", 'allow_reactions'),
        ("Allow public comments", 'allow_public_comments'),
        ("Allow professional comments", 'allow_professional_comments'),
        ("Post vent", 'post_vent')
    ]
    keyboard = create_menu_keyboard(buttons)
    await update.effective_message.reply_text('Choose options for your vent:', reply_markup=keyboard)

async def handle_vent_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'allow_reactions':
        context.user_data['allow_reactions'] = not context.user_data.get('allow_reactions', False)
    elif query.data == 'allow_public_comments':
        context.user_data['allow_public_comments'] = not context.user_data.get('allow_public_comments', False)
    elif query.data == 'allow_professional_comments':
        context.user_data['allow_professional_comments'] = not context.user_data.get('allow_professional_comments', False)
    elif query.data == 'post_vent':
        user_id = context.user_data['user_id']
        content = context.user_data['vent_content']
        allow_reactions = context.user_data.get('allow_reactions', False)
        allow_public_comments = context.user_data.get('allow_public_comments', False)
        allow_professional_comments = context.user_data.get('allow_professional_comments', False)
        
        save_vent(user_id, content, allow_reactions, allow_public_comments, allow_professional_comments)
        
        await query.edit_message_text('Your vent has been posted. Thank you for sharing.')
        await show_main_menu(update, context)
        return MAIN_MENU

    current_options = f"Current options:\n" \
                      f"Allow reactions: {'Yes' if context.user_data.get('allow_reactions', False) else 'No'}\n" \
                      f"Allow public comments: {'Yes' if context.user_data.get('allow_public_comments', False) else 'No'}\n" \
                      f"Allow professional comments: {'Yes' if context.user_data.get('allow_professional_comments', False) else 'No'}"
    
    buttons = [
        ("Allow reactions", 'allow_reactions'),
        ("Allow public comments", 'allow_public_comments'),
        ("Allow professional comments", 'allow_professional_comments'),
        ("Post vent", 'post_vent')
    ]
    keyboard = create_menu_keyboard(buttons)
    await query.edit_message_text(text=f"{current_options}\n\nChoose options for your vent:", reply_markup=keyboard)

    return VENT_OPTIONS