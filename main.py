from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import configparser
import ButtonFunctions as butf
import CommandFunctions as comf

gameSessions = {}

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('CONFIG.ini')
    tkn = config.get('BaseSection', 'TOKEN')
    application = ApplicationBuilder().token(tkn).build()

    start_handler = CommandHandler('start', comf.start)
    application.add_handler(start_handler)
    stop_handler = CommandHandler('stop', comf.stop)
    application.add_handler(stop_handler)
    application.add_handler(CallbackQueryHandler(butf.start_button, pattern = 'start'))
    application.add_handler(CallbackQueryHandler(butf.join_button, pattern = 'join'))
    application.add_handler(CallbackQueryHandler(butf.hit_button, pattern = 'hit'))
    application.add_handler(CallbackQueryHandler(butf.stand_button, pattern = "stand"))

    application.run_polling()
