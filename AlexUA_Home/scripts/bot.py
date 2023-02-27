import os
import logging
from typing import Dict

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from apps.english.models import Words
from asgiref.sync import sync_to_async

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

reply_keyboard = [
    ["Start learn", "List"],
    ["English", "Add word"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
        reply_markup=markup,
    )


@sync_to_async
def save_word(word, translate):
    return Words.objects.create(english=word, russian=translate)


@sync_to_async
def get_words():
    all_words = Words.objects.all()
    english_words = [word.english for word in all_words]
    answer = str(len(english_words)) + ": " + ', '.join(english_words)
    return answer


@sync_to_async
def get_word():
    word = Words.objects.filter().order_by("?").first()
    return word


async def list_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_words = await get_words()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=all_words,
        reply_markup=markup,
    )


async def start_add_word(update: Update, context) -> int:
    logger.warning("start add word")
    text = update.message.text
    logger.debug("input word:" + text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Type the word",
        reply_markup=ReplyKeyboardRemove()
    )

    return WORD


async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    word = update.message.text
    logger.debug("input word:" + word)
    context.user_data["word"] = word

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="input translate:",
    )
    return TRANSTATE


async def add_translate_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("write translate word")
    translate_ = update.message.text
    logger.debug("input word:" + translate_)
    context.user_data["translate"] = translate_
    user_data = context.user_data
    word = user_data["word"]
    reply_keyboard = [
        ["Yes", "No"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"you input: {word} - {translate_}. Save?",
        reply_markup=markup,
    )
    return DONE


async def save_word_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Вывод собранной информации и завершение разговора."""
    user_data = context.user_data
    new_word = await save_word(user_data["word"], user_data["translate"])
    await update.message.reply_text(
        f"Save word to db{new_word.id}",
        reply_markup=markup,
    )
    user_data.clear()
    return ConversationHandler.END


async def not_save_word_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    await update.message.reply_text(
        f"Not save word to db",
        reply_markup=markup,
    )
    user_data.clear()
    return ConversationHandler.END


async def start_learn(update: Update, context) -> int:
    logger.warning("start learn")
    word = await get_word()
    context.user_data["word"] = word.english
    context.user_data["translate"] = word.russian
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"word: {context.user_data['translate']}",
        reply_markup=ReplyKeyboardRemove()
    )
    return ORIGIN


async def check_translate(update: Update, context) -> int:
    user_data = context.user_data
    text = update.message.text.lower()
    if text == user_data['word']:
        text_answer = "right"
    else:
        text_answer = "wrong: " + user_data['word']
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_answer,
        reply_markup=markup
    )
    return ConversationHandler.END


WORD, TRANSTATE, DONE = range(3)
ORIGIN, SECOND = range(2)


def run():
    conv_handler_add = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^Add word$"), start_add_word)],
        states={
            WORD: [MessageHandler(filters.Regex("^.*$"), add_word), ],
            TRANSTATE: [MessageHandler(filters.Regex("^.*$"), add_translate_word)],
            DONE: [MessageHandler(filters.Regex("^Yes$"), save_word_to_db),
                   MessageHandler(filters.Regex("^No$"), not_save_word_to_db)]

        },
        fallbacks=[],
    )
    conv_handler_learn = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^Start learn$"), start_learn)],
        states={
            ORIGIN: [MessageHandler(filters.Regex("^.*$"), check_translate), ],

        },
        fallbacks=[],
    )
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(conv_handler_add)
    application.add_handler(conv_handler_learn)
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^List$"), list_words))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()
