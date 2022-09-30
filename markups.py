from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Main menu
btnProfile = KeyboardButton('📃PROFILE')
btnSub = KeyboardButton('💎SUBSCRIBE')
btnFaq = KeyboardButton('📋FAQ')
btnPrivate = KeyboardButton('🛂LINK TO THE PRIVATE CHANNEL')
btnTech = KeyboardButton('📝TECHNICAL SUPPORT')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu.add(btnProfile, btnSub, btnFaq, btnPrivate, btnTech)

# Subscribe 
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btnSubMonth = InlineKeyboardButton(text="Month", callback_data="submonth")
sub_inline_markup.insert(btnSubMonth)

#Admin Menu
btnProfile = KeyboardButton('Тикеты')