from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import BlackJackLogic as bj
import main as m

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if m.gameSessions.get(update.effective_chat.id) == None or not m.gameSessions[update.effective_chat.id].isGame:
        keyboard = [
            [InlineKeyboardButton("Join", callback_data='join')],
            [InlineKeyboardButton("Start", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        temp = await context.bot.send_message(chat_id=update.effective_chat.id,
                                              text=f"Присоединяйтесь к игре, девочки! \nJoined player: \n{update.message.from_user.username}",
                                              reply_markup=reply_markup)
        m.gameSessions[update.effective_chat.id] = bj.GameSession(update.message.from_user.username, temp.message_id)
    elif m.gameSessions[update.effective_chat.id].isGame:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="СОСИТЕ, TACO NIGGERS!!!!")
        return

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if m.gameSessions.get(update.effective_chat.id) == None or not m.gameSessions[update.effective_chat.id].isGame:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="АЛЁ ИГРА НЕ ИДЕТ УЁБИЩЕ, СЪЕБАЛ ПОКА Я НЕ ВЫЛЕЗ ИЗ ЭКРАНА И НЕ ОТЪЕБАЛ ТЕБЯ")
        return
    else:
        m.gameSessions[update.effective_chat.id].reset()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Можете начинать, я уже без штанов")
        return