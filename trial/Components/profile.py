from telegram import Update
from telegram.ext import ContextTypes

from database import get_user_profile, update_user_profile
from states import *
from trial.Components.main_menu import show_main_menu
from utils import create_menu_keyboard





async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data['user_id']
    profile = get_user_profile(user_id)
    
    if profile:
        profile_text = f"Nickname: {profile[1]}\nAge: {profile[2]}\nGender: {profile[3]}\nNationality: {profile[4]}"
        buttons = [("Edit Profile", 'edit_profile')]
    else:
        profile_text = "You haven't set up your profile yet."
        buttons = [("Create Profile", 'edit_profile')]
    
    buttons.append(("Back to Main Menu", 'main_menu'))
    keyboard = create_menu_keyboard(buttons)
    
    await update.callback_query.edit_message_text(text=profile_text, reply_markup=keyboard)
    return MY_PROFILE

async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("Please enter your nickname:")
    return EDIT_PROFILE

async def handle_profile_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data['user_id']
    text = update.message.text
    
    if 'profile_step' not in context.user_data:
        context.user_data['profile_step'] = 'nickname'
        context.user_data['nickname'] = text
        await update.message.reply_text("Great! Now, please enter your age:")
        return EDIT_PROFILE
    
    elif context.user_data['profile_step'] == 'nickname':
        context.user_data['profile_step'] = 'age'
        context.user_data['age'] = int(text)
        await update.message.reply_text("Got it! Next, please enter your gender:")
        return EDIT_PROFILE
    
    elif context.user_data['profile_step'] == 'age':
        context.user_data['profile_step'] = 'gender'
        context.user_data['gender'] = text
        await update.message.reply_text("Almost done! Finally, please enter your nationality:")
        return EDIT_PROFILE
    
    elif context.user_data['profile_step'] == 'gender':
        context.user_data['nationality'] = text
        
        # Save the profile to the database
        update_user_profile(user_id, context.user_data['nickname'], context.user_data['age'], 
                            context.user_data['gender'], context.user_data['nationality'])
        
        await update.message.reply_text("Your profile has been updated successfully!")
        await show_main_menu(update, context)
        return MAIN_MENU