from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import BlackJackLogic as bj
import ServiceFunctuons as serf
import main as m

async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.username != m.gameSessions[update.effective_chat.id].players[0].name:
        return
    await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=m.gameSessions[update.effective_chat.id].last_start_message_id, text=f"Присоединяйтесь к игре, девочки! \nJoined player: \n{m.gameSessions[update.effective_chat.id].players[0].name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="GAME НАЧАТА")
    await serf.go_next(update, context)

async def join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if sum(1 for x in m.gameSessions[update.effective_chat.id].players if x.name == query.from_user.username)>0:
        return
    m.gameSessions[update.effective_chat.id].players.append(bj.Player(query.from_user.username, m.gameSessions[update.effective_chat.id]))
    keyboard = [
        [InlineKeyboardButton("Join", callback_data='join')],
        [InlineKeyboardButton("Start", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    result = "Присоединяйтесь к игре, девочки! \nJoined players: \n"
    for i in range(0,len(m.gameSessions[update.effective_chat.id].players)):
        result += f"{m.gameSessions[update.effective_chat.id].players[i].name}\n"
    await query.edit_message_text(text=result, reply_markup=reply_markup)

async def hit_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.username != m.gameSessions[update.effective_chat.id].current_player.name:
        return
    if m.gameSessions[update.effective_chat.id].current_player.hit() == True:
        if m.gameSessions[update.effective_chat.id].current_player.win == True:
            await query.edit_message_text(text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()} \n \nПобедил, хуйлуша")
        if m.gameSessions[update.effective_chat.id].current_player.win == False:
            await query.edit_message_text(text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()} \n \nПроиграл, хуйлуша")
        await serf.go_next(update, context)
        return
    keyboard = [
        [InlineKeyboardButton("Hit", callback_data='hit')],
        [InlineKeyboardButton("Stand", callback_data='stand')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}", reply_markup=reply_markup)

async def stand_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.username != m.gameSessions[update.effective_chat.id].current_player.name:
        return
    await query.edit_message_text(text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}")
    await serf.go_next(update, context)