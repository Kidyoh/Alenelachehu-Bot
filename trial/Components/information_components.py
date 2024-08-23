from telegram import Update
from telegram.ext import ContextTypes
from utils import create_menu_keyboard
from states import *


async def view_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = """
    Rules and Regulations:
    1. No personal attacks
    2. No explicit content
    3. No spam or promotion
    4. Moderator discretion
    5. Suspension/banning for repeated violations
    6. Use reporting system for violations
    7. Data privacy protected
    8. Appeal process available
    9. Respect privacy of others
    10. Alenelachehu may use anonymized content for positive impact
    """
    keyboard = create_menu_keyboard([("Back to How to Use", 'how_to_use')])
    await update.callback_query.edit_message_text(text=rules_text, reply_markup=keyboard)



async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = """
    Rules and Regulations:
    1. No personal attacks
    2. No explicit content
    3. No spam or promotion
    4. Moderator discretion
    5. Suspension/banning for repeated violations
    6. Use reporting system for violations
    7. Data privacy protected
    8. Appeal process available
    9. Respect privacy of others
    10. Alenelachehu may use anonymized content for positive impact
    """
    keyboard = create_menu_keyboard([("Back to Main Menu", 'main_menu')])
    await update.callback_query.edit_message_text(text=rules_text, reply_markup=keyboard)
    return RULES

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ("Need Professional Support", 'professional_support'),
        ("Need Support Group", 'support_group'),
        ("Contact Alenelachehu", 'contact_org'),
        ("Back to Main Menu", 'main_menu')
    ]
    keyboard = create_menu_keyboard(buttons)
    await update.callback_query.edit_message_text('Help Menu:', reply_markup=keyboard)
    return HELP

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
    Alenelachehu Charitable Organization (ACO) is a non-profit organization established in May 2023.
    
    Mission: To provide accessible and compassionate support for those struggling with mental health challenges.
    
    Vision: Creating an Ethiopia where mental health is not stigmatized and all individuals have access to resources and support.
    
    Goals:
    - Reducing stigma around mental health
    - Minimizing suicide rates in Ethiopia
    - Providing support services to individuals and families affected by mental illness
    - Collaborating with other organizations to address mental health challenges
    
    Contact: 
    - Email: Alenelacehuco@gmail.com
    - Website: www.Alenelachehu.org
    - Phone: +251965579192 or +251919186182
    - Telegram: https://t.me/Alenelachehu
    - LinkedIn: https://www.linkedin.com/company/alenelachehu-charitable-organization/
    - WhatsApp: https://chat.whatsapp.com/KzPWHuG4m3LG7DB7uXVdKZ
    - Facebook: https://www.facebook.com/profile.php?id=100081094233970
    """
    keyboard = create_menu_keyboard([("Back to Main Menu", 'main_menu')])
    await update.callback_query.edit_message_text(text=about_text, reply_markup=keyboard)
    return MAIN_MENU