""" bot initialization """

import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
    Filters,
    InlineQueryHandler,
    MessageHandler,
    Updater,
)
from telegram.ext import messagequeue as mq

from functions import sync_current_leagues, sync_game_current_league
from handlers import (
    get_game_start_twitch,
    get_tournament_info,
    help_me,
    ikb_subscribe,
    inlinequery,
    set_alarm,
    start,
)

from settings import PROXY, TOKEN

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


def main():
    # creating bot
    bot = Updater(TOKEN, use_context=True, request_kwargs=PROXY)

    # creating dispatcher
    dp = bot.dispatcher

    # creating job for regular sync database
    bot.job_queue.run_repeating(callback=sync_current_leagues, interval=3600, first=10)
    bot.job_queue.run_repeating(callback=sync_game_current_league, interval=3600, first=10)

    # creating write in log about start bot
    logging.info("Bot is run")

    # creating handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_me))
    dp.add_handler(
        MessageHandler(Filters.regex("OK, search informations about (.*)"), get_tournament_info)
    )
    dp.add_handler(CallbackQueryHandler(ikb_subscribe))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(
        CommandHandler("alarm", set_alarm, pass_args=True, pass_job_queue=True)
    )
    # run bot
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
