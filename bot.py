import django
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CallbackContext, CommandHandler, MessageHandler, Filters, \
    ConversationHandler, CallbackQueryHandler
from django.conf import settings

django.setup()
from account.models import Account


# Returns a constant text as an unknown command entered
def unknown(update: Update, context: CallbackContext):
    """
        Unknown command
    """

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Hey my friend!')


def menu(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton('Download Vector', callback_data=1)
        ]
    ]
    reply_keyboard = InlineKeyboardMarkup(keyboard)
    msg = 'Hello & Welcome to the world of *Strangers*'

    update.message.reply_text(
        msg,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=reply_keyboard
    )
    return 1


def download_vector(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    query.answer()

    msg = 'Enter your vector *data_id*'
    query.edit_message_text(
        msg,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    return 2


def get_vector(update: Update, context: CallbackContext) -> int:
    response = int(update.message.text)
    account = Account.get_first_available_account()
    if not account:
        msg = 'Sorry, I\'m in the limit too ;('
        update.message.reply_text(
            msg,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        return ConversationHandler.END

    download_link = account.download_vector(response)
    msg = f'Download link: *{download_link}*'

    update.message.reply_text(
        msg,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(token=settings.TELEGRAM.get('bot_token'),
                      use_context=True)

    # Get the dispatcher to register handlers
    dispatcher: Dispatcher = updater.dispatcher

    menu_handler = ConversationHandler(
        entry_points=[CommandHandler('menu', menu)],
        states={
            1: [
                CallbackQueryHandler(download_vector, pattern=r'^1$'),
            ],
            2: [
                MessageHandler(Filters.regex(r'\d+'), get_vector)
            ]
        },
        fallbacks=[CommandHandler('menu', menu)]
    )
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(menu_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully
    updater.idle()


if __name__ == '__main__':
    main()
