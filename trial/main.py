import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters

from config import TOKEN
from database import setup_database
from Components.main_menu import *
from Components.venting_components import *
from Components.profile import *
from Components.information_components import *
from Components.sos import *
from Components.help_components import *
from Components.support_components import *
from states import *
from handlers import start

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Setup the database before running the bot
    setup_database()

    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Setup command handlers
    application.add_handler(CommandHandler('start', start))

    # Setup conversation handlers
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(main_menu_handler, pattern='^(how_to_use|start_venting|my_profile|rules|help|about|sos)$')],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu_handler, pattern='^(how_to_use|start_venting|my_profile|rules|help|about|sos)$'),
            ],
            HOW_TO_USE: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(how_to_use, pattern='^(how_to_vent|how_to_report|how_to_contact|how_to_profile|view_rules)$'),
            ],
            START_VENTING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, venting),
                CallbackQueryHandler(handle_vent_options, pattern='^(allow_reactions|allow_public_comments|allow_professional_comments|post_vent)$')
            ],
            VENT_OPTIONS: [
                CallbackQueryHandler(handle_vent_options, pattern='^(allow_reactions|allow_public_comments|allow_professional_comments|post_vent)$')
            ],
            MY_PROFILE: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(edit_profile, pattern='edit_profile'),
                CallbackQueryHandler(my_profile, pattern='view_profile'),
            ],
            EDIT_PROFILE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_input),
            ],
            RULES: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(rules, pattern='view_rules')
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
                CallbackQueryHandler(main_menu_handler, pattern='main_menu'),
                CallbackQueryHandler(handle_support_group, pattern='support_group'),
            ],
            ABOUT: [
                CallbackQueryHandler(main_menu_handler, pattern='main_menu')
            ],
            SOS: [
            CallbackQueryHandler(sos, pattern='^sos$'),
            ],
            SOS_LOCATION: [
                MessageHandler(filters.LOCATION, sos_location),
            ],
            SOS_VOICE: [
                MessageHandler(filters.VOICE, sos_voice),
            ],
            SOS_PHOTO: [
                MessageHandler(filters.PHOTO, sos_photo),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add conversation handler to application
    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()