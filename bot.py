import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Filters, MessageHandler, CallbackQueryHandler
from constants import *
from bot_token import TOKEN
from scraper import sneak_info, last_sneak_movies
import pickle
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def store_update(update):
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)
    with open(os.path.join(LOG_FOLDER, f'update-{update.update_id}.pickle'), 'wb') as file:
        pickle.dump(update, file)

    log_files = os.listdir(LOG_FOLDER)
    if len(log_files) % UPDATE_HISTORY_LOG_FREQUENCY == 0:
        logger.info(f'Currently storing {len(log_files)} update files')

def get_keyboard_markup(menu=None):
    if menu == LAST_SNEAKS_MENU:
        buttons = [
            [InlineKeyboardButton(LAST_1_SNEAKS_BUTTON_TEXT, callback_data=LAST_1_SNEAKS_CALLBACK),
             InlineKeyboardButton(LAST_5_SNEAKS_BUTTON_TEXT, callback_data=LAST_5_SNEAKS_CALLBACK),
             InlineKeyboardButton(LAST_10_SNEAKS_BUTTON_TEXT, callback_data=LAST_10_SNEAKS_CALLBACK)],
            [InlineKeyboardButton(LAST_ALL_SNEAKS_BUTTON_TEXT, callback_data=LAST_ALL_SNEAKS_CALLBACK)]
        ]
        return InlineKeyboardMarkup(buttons)
    else:
        return InlineKeyboardMarkup.from_column([
            InlineKeyboardButton(SNEAK_BUTTON_TEXT, callback_data=SNEAK_CALLBACK),
            InlineKeyboardButton(LAST_SNEAKS_BUTTON_TEXT, callback_data=LAST_SNEAKS_CALLBACK)
        ])

def show_start_menu(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=START_MENU_MESSAGE,
                             reply_markup=(get_keyboard_markup()))

def message(update, context):
    show_start_menu(update, context)
    store_update(update)

def button(update, context):
    if update.callback_query.data == SNEAK_CALLBACK:
        next_sneak = sneak_info()
        if next_sneak is None:
            update.callback_query.edit_message_text(text=INTERNAL_ERROR_MESSAGE)
        else:
            update.callback_query.edit_message_text(text=next_sneak)
        show_start_menu(update, context)
    elif update.callback_query.data == LAST_SNEAKS_CALLBACK:
        update.callback_query.edit_message_text(text=SELECT_N_LAST_SNEAKS_MESSAGE,
                                                reply_markup=get_keyboard_markup(LAST_SNEAKS_MENU))
    elif update.callback_query.data == LAST_1_SNEAKS_CALLBACK:
        update.callback_query.edit_message_text(text=last_sneak_movies(1))
        show_start_menu(update, context)
    elif update.callback_query.data == LAST_5_SNEAKS_CALLBACK:
        update.callback_query.edit_message_text(text=last_sneak_movies(5))
        show_start_menu(update, context)
    elif update.callback_query.data == LAST_10_SNEAKS_CALLBACK:
        update.callback_query.edit_message_text(text=last_sneak_movies(10))
        show_start_menu(update, context)
    elif update.callback_query.data == LAST_ALL_SNEAKS_CALLBACK:
        update.callback_query.edit_message_text(text=last_sneak_movies())
        show_start_menu(update, context)
    else:
        update.callback_query.edit_message_text(text=INTERNAL_ERROR_MESSAGE)
        show_start_menu(update, context)
    store_update(update)

def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()