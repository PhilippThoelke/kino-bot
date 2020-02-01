import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Filters, MessageHandler, CallbackQueryHandler
from constants import *
from bot_token import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_keyboard_markup(menu=None):
    if menu == 0:
        pass
    else:
        buttons = [[InlineKeyboardButton(SNEAK_BUTTON_TEXT, callback_data=SNEAK_CALLBACK_DATA)]]
        return InlineKeyboardMarkup(buttons)

def show_start_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=START_MENU_MESSAGE,
                             reply_markup=(get_keyboard_markup()))

def message(update, context):
    show_start_menu(update, context)

def button(update, context):
    if update.callback_query.data == SNEAK_CALLBACK_DATA:
        update.callback_query.edit_message_text(text='Yaay sneeaaaak')
        show_start_menu(update, context)
    else:
        update.callback_query.edit_message_text(text=INTERNAL_ERROR_MESSAGE)
        show_start_menu(update, context)

def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()