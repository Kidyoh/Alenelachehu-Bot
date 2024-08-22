import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters

from trial.handlers import sos

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
(MAIN_MENU, HOW_TO_USE, START_VENTING, VENTING, VENT_OPTIONS, MY_PROFILE, EDIT_PROFILE,
 RULES, HELP, ABOUT, PROFESSIONAL_SUPPORT, SUPPORT_GROUP, SOS) = range(13)

# Database setup
def setup_database():
    conn = sqlite3.connect('alenelachehu_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, nickname TEXT, age INTEGER, gender TEXT, nationality TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT, timestamp TEXT, 
                  allow_reactions BOOLEAN, allow_public_comments BOOLEAN, allow_professional_comments BOOLEAN)''')
    conn.commit()
    conn.close()

# User profile functions
def get_user_profile(user_id):
    conn = sqlite3.connect('alenelachehu_bot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    return profile

def update_user_profile(user_id, nickname, age, gender, nationality):
    conn = sqlite3.connect('alenelachehu_bot.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, nickname, age, gender, nationality) VALUES (?, ?, ?, ?, ?)",
              (user_id, nickname, age, gender, nationality))
    conn.commit()
    conn.close()

def save_vent(user_id, content, allow_reactions, allow_public_comments, allow_professional_comments):
    conn = sqlite3.connect('alenelachehu_bot.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO vents (user_id, content, timestamp, allow_reactions, allow_public_comments, allow_professional_comments) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, content, timestamp, allow_reactions, allow_public_comments, allow_professional_comments))
    conn.commit()
    conn.close()

# Command handler for /start
async def start(update: Update, context):
    user = update.effective_user
    context.user_data['user_id'] = user.id
    await show_main_menu(update, context)
    return MAIN_MENU

# Function to show the main menu
async def show_main_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("How to use the bot", callback_data='how_to_use')],
        [InlineKeyboardButton("Start Venting", callback_data='start_venting')],
        [InlineKeyboardButton("My Profile", callback_data='my_profile')],
        [InlineKeyboardButton("Rules and Regulation", callback_data='rules')],
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("About Alenelachehu", callback_data='about')]
        [InlineKeyboardButton("Sos", callback_data='sos')]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text('Welcome to Alenelachehu venting platform. Please choose an option:', reply_markup=reply_markup)

# Callback query handler for main menu
async def main_menu_handler(update: Update, context):
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
    elif query.data == 'sos':
        await sos(update, context)
        return ABOUT
    elif query.data == 'main_menu':
        await show_main_menu(update, context)
        return MAIN_MENU   

# Handler for "How to vent"
async def how_to_vent(update: Update, context):
    text = ("To vent, simply click on the 'Start Venting' button in the main menu. "
            "You can type out your thoughts and feelings, and choose whether to allow reactions, comments, or professional feedback.")
    keyboard = [[InlineKeyboardButton("Back to How to Use", callback_data='how_to_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return HOW_TO_USE

# Handler for "How to report comment"
async def how_to_report(update: Update, context):
    text = ("To report a comment, simply click on the 'Report' button next to the comment you wish to report. "
            "You will be prompted to provide a reason for the report.")
    keyboard = [[InlineKeyboardButton("Back to How to Use", callback_data='how_to_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return HOW_TO_USE

# Handler for "How to contact Alenelachehu"
async def how_to_contact(update: Update, context):
    text = ("To contact Alenelachehu, you can reach out through the following channels:\n"
            "Email: Alenelachehuco@gmail.com\n"
            "Website: www.Alenelachehu.org\n"
            "Phone: +251965579192 or +251919186182\n"
            "Telegram: https://t.me/Alenelachehu\n"
            "LinkedIn: https://www.linkedin.com/company/alenelachehu-charitable-organization/\n"
            "WhatsApp: https://chat.whatsapp.com/KzPWHuG4m3LG7DB7uXVdKZ\n"
            "Facebook: https://www.facebook.com/profile.php?id=100081094233970")
    keyboard = [[InlineKeyboardButton("Back to How to Use", callback_data='how_to_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return HOW_TO_USE

# Handler for "How to view/edit profile"
async def how_to_profile(update: Update, context):
    text = ("To view or edit your profile, click on the 'My Profile' button in the main menu. "
            "You can set or update your nickname, age, nationality, and other details.")
    keyboard = [[InlineKeyboardButton("Back to How to Use", callback_data='how_to_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return HOW_TO_USE

# Handler for "View Rules"
async def view_rules(update: Update, context):
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
    keyboard = [[InlineKeyboardButton("Back to How to Use", callback_data='how_to_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=rules_text, reply_markup=reply_markup)
    return HOW_TO_USE




# Handler for "How to use the bot"
async def how_to_use(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("How to vent", callback_data='how_to_vent')],
        [InlineKeyboardButton("How to report comment", callback_data='how_to_report')],
        [InlineKeyboardButton("How to contact Alenelachehu", callback_data='how_to_contact')],
        [InlineKeyboardButton("How to view/edit profile", callback_data='how_to_profile')],
        [InlineKeyboardButton("View Rules", callback_data='view_rules')],
        [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('How to use the bot:', reply_markup=reply_markup)


# Handler for "Start Venting"
async def start_venting(update: Update, context):
    await update.callback_query.edit_message_text('Please start typing your thoughts. When you\'re done, send /done')
    return VENTING

async def venting(update: Update, context):
    if update.message.text == '/done':
        context.user_data['vent_content'] = context.user_data.get('vent_content', '')
        await vent_options(update, context)
        return VENT_OPTIONS
    else:
        context.user_data['vent_content'] = context.user_data.get('vent_content', '') + update.message.text + '\n'
        return VENTING

async def vent_options(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Allow reactions", callback_data='allow_reactions')],
        [InlineKeyboardButton("Allow public comments", callback_data='allow_public_comments')],
        [InlineKeyboardButton("Allow professional comments", callback_data='allow_professional_comments')],
        [InlineKeyboardButton("Post vent", callback_data='post_vent')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text('Choose options for your vent:', reply_markup=reply_markup)

async def handle_vent_options(update: Update, context):
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

    # Update the message with current options
    current_options = f"Current options:\n" \
                      f"Allow reactions: {'Yes' if context.user_data.get('allow_reactions', False) else 'No'}\n" \
                      f"Allow public comments: {'Yes' if context.user_data.get('allow_public_comments', False) else 'No'}\n" \
                      f"Allow professional comments: {'Yes' if context.user_data.get('allow_professional_comments', False) else 'No'}"
    
    keyboard = [
        [InlineKeyboardButton("Allow reactions", callback_data='allow_reactions')],
        [InlineKeyboardButton("Allow public comments", callback_data='allow_public_comments')],
        [InlineKeyboardButton("Allow professional comments", callback_data='allow_professional_comments')],
        [InlineKeyboardButton("Post vent", callback_data='post_vent')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"{current_options}\n\nChoose options for your vent:", reply_markup=reply_markup)

    return VENT_OPTIONS

# Handler for "My Profile"
async def my_profile(update: Update, context):
    user_id = context.user_data['user_id']
    profile = get_user_profile(user_id)
    
    if profile:
        profile_text = f"Nickname: {profile[1]}\nAge: {profile[2]}\nGender: {profile[3]}\nNationality: {profile[4]}"
        keyboard = [[InlineKeyboardButton("Edit Profile", callback_data='edit_profile')]]
    else:
        profile_text = "You haven't set up your profile yet."
        keyboard = [[InlineKeyboardButton("Create Profile", callback_data='edit_profile')]]
    
    keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(text=profile_text, reply_markup=reply_markup)
    return MY_PROFILE

async def edit_profile(update: Update, context):
    await update.callback_query.edit_message_text("Please enter your nickname:")
    return EDIT_PROFILE

async def handle_profile_input(update: Update, context):
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

# Handler for "Rules and Regulation"
async def rules(update: Update, context):
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
    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=rules_text, reply_markup=reply_markup)
    return RULES

# Handler for "Help"
async def help_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Need Professional Support", callback_data='professional_support')],
        [InlineKeyboardButton("Need Support Group", callback_data='support_group')],
        [InlineKeyboardButton("Contact Alenelachehu", callback_data='contact_org')],
        [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('Help Menu:', reply_markup=reply_markup)
    return HELP

async def professional_support(update: Update, context):
    text = ("If you need professional support, we're here to help. "
            "Please choose your preferred method of support:")
    keyboard = [
        [InlineKeyboardButton("Online Support", callback_data='online_support')],
        [InlineKeyboardButton("In-Person Support", callback_data='in_person_support')],
        [InlineKeyboardButton("Back to Help Menu", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return PROFESSIONAL_SUPPORT

async def support_group(update: Update, context):
    text = ("Support groups can be a great way to connect with others who understand what you're going through. "
            "Please choose your preferred type of support group:")
    keyboard = [
        [InlineKeyboardButton("Online Support Group", callback_data='online_group')],
        [InlineKeyboardButton("In-Person Support Group", callback_data='in_person_group')],
        [InlineKeyboardButton("Back to Help Menu", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    return SUPPORT_GROUP

# Handler for "About Alenelachehu" (continued)
async def about(update: Update, context):
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
    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=about_text, reply_markup=reply_markup)
    return MAIN_MENU

# Handler for professional support options
async def handle_professional_support(update: Update, context):
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

# Handler for support group options
async def handle_support_group(update: Update, context):
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

    keyboard = [[InlineKeyboardButton("Back to Help Menu", callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SUPPORT_GROUP

# Handler for processing professional support requests
async def process_professional_support(update: Update, context):
    user_id = update.effective_user.id
    support_request = update.message.text

    # Here you would typically save this information to your database
    # For now, we'll just log it
    logger.info(f"Professional support request from user {user_id}: {support_request}")

    response_text = ("Thank you for reaching out for professional support. "
                     "We have received your request and will contact you soon with further details.")
    await update.message.reply_text(response_text)
    await show_main_menu(update, context)
    return MAIN_MENU

# Handler for processing support group requests
async def process_support_group(update: Update, context):
    user_id = update.effective_user.id
    group_request = update.message.text

    # Here you would typically save this information to your database
    # For now, we'll just log it
    logger.info(f"Support group request from user {user_id}: {group_request}")

    response_text = ("Thank you for your interest in joining a support group. "
                     "We have received your information and will contact you soon with available group options.")
    await update.message.reply_text(response_text)
    await show_main_menu(update, context)
    return MAIN_MENU


# Error handler
async def error(update: Update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == '__main__':
    # Setup the database before running the bot
    setup_database()
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('7103950749:AAFW0KFdWJyG-zpvaG0MTTd-SeMg63GsE8A').build()
    # Setup command handlers
    application.add_handler(CommandHandler('start', start))
    # Setup conversation handlers
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(main_menu_handler, pattern='^(how_to_use|start_venting|my_profile|rules|help|about)$')],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu_handler, pattern='^(how_to_use|start_venting|my_profile|rules|help|about)$'),
            ],
            HOW_TO_USE: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(how_to_vent, pattern='how_to_vent'),
                CallbackQueryHandler(how_to_report, pattern='how_to_report'),
                CallbackQueryHandler(how_to_contact, pattern='how_to_contact'),
                CallbackQueryHandler(how_to_profile, pattern='how_to_profile'),
                CallbackQueryHandler(view_rules, pattern='view_rules'),

            ],
            START_VENTING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, venting),
                CallbackQueryHandler(handle_vent_options, pattern='^(allow_reactions|allow_public_comments|allow_professional_comments|post_vent)$')
            ],
            MY_PROFILE: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(edit_profile, pattern='edit_profile')
            ],
            EDIT_PROFILE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_input),
            ],
            RULES: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu')
            ],
            HELP: [
                CallbackQueryHandler(handle_professional_support, pattern='^(professional_support|support_group|contact_org)$'),
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
            ],
            PROFESSIONAL_SUPPORT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_professional_support),
            ],
            SUPPORT_GROUP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_support_group),
            ],
            ABOUT: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu')
            ],
            SOS: [
                CallbackQueryHandler(sos, pattern='sos')
            ]

        },
        fallbacks=[CommandHandler('start', start)],
    )
    # Add conversation handler to application
    application.add_handler(conv_handler)
    # Log all errors
    application.add_error_handler(error)
    # Start the Bot
    application.run_polling()