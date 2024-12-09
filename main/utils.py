from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_menu_keyboard(buttons):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in buttons
    ])
