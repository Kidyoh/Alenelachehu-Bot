import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from database import get_user_profile, update_user_profile, save_vent
from states import *
from utils import create_menu_keyboard


logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data['user_id'] = user.id
    await show_main_menu(update, context)
    return MAIN_MENU

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

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
