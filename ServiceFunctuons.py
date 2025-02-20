import asyncio
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import BlackJackLogic as bj
import CommandFunctions as comf
import main as m


async def go_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if m.gameSessions[update.effective_chat.id].current_player_index >= len(m.gameSessions[update.effective_chat.id].players):
        await dealer(update, context)
        return
    m.gameSessions[update.effective_chat.id].current_player = m.gameSessions[update.effective_chat.id].players[m.gameSessions[update.effective_chat.id].current_player_index]
    m.gameSessions[update.effective_chat.id].current_player_index += 1
    if m.gameSessions[update.effective_chat.id].current_player.value_sum == 21:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}")
        await go_next(update, context)
    keyboard = [
        [InlineKeyboardButton("Hit", callback_data='hit')],
        [InlineKeyboardButton("Stand", callback_data='stand')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}", reply_markup=reply_markup)

async def dealer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m.gameSessions[update.effective_chat.id].current_player = bj.Player("Dealer", m.gameSessions[update.effective_chat.id])
    last_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}")
    last_message_id = last_message.message_id
    while m.gameSessions[update.effective_chat.id].current_player.value_sum < 17:
        await asyncio.sleep(random.randrange(3, 5))
        m.gameSessions[update.effective_chat.id].current_player.hit()
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id= last_message_id, text=f"{m.gameSessions[update.effective_chat.id].current_player.name} - Value: {m.gameSessions[update.effective_chat.id].current_player.value_sum} \n \n{m.gameSessions[update.effective_chat.id].current_player.represent_cards()}")
    await view_top(update, context)

async def view_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    winners = ""
    ties = ""
    losers = ""
    result = ""
    for i in m.gameSessions[update.effective_chat.id].players:
        if i.win == True or m.gameSessions[update.effective_chat.id].current_player.value_sum < i.value_sum < 21 or i.value_sum < 21 and m.gameSessions[update.effective_chat.id].current_player.value_sum > 21:
            winners += f"{i.name} - {i.value_sum}\n"
        elif m.gameSessions[update.effective_chat.id].current_player.value_sum == i.value_sum:
            ties += f"{i.name} - {i.value_sum}\n"
        elif i.value_sum < m.gameSessions[update.effective_chat.id].current_player.value_sum or i.value_sum > 21:
            losers += f"{i.name} - {i.value_sum}\n"
    if winners != "":
        result += "👬🏿Победители:\n" + winners + '\n'
    if ties != "":
        result += "🫃Ничья(лохохоли):\n" + ties + '\n'
    if losers != "":
        result += "👫Отсосавшие(натуралы):\n" + losers + '\n'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    await comf.stop(update, context)