# -*- coding: utf-8 -*-
import re
from config import *
from asyncio import sleep
from aiofiles import open
from os import mkdir, remove
from vkbottle.api import API
from markovify import NewlineText
from random import choice, randint
from vkbottle.bot import Bot, Message
from vkbottle_types.objects import MessagesForward
from vkbottle.dispatch.rules.bot import ChatActionRule, FromUserRule

api = API(BOT_TOKEN)
bot = Bot(BOT_TOKEN)
chance = RESPONSE_CHANCE
greet = ""

#приветствие в чате
@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def invited(message: Message) -> None:
    """Приветствие при приглашении бота в беседу."""
    if message.group_id == -message.action.member_id:
        await message.answer(
            f"""Я родился!
{COMMANDS}""")

#список команд
@bot.on.message(text="/команды")
async def help(message: Message) -> None:
    await message.answer(COMMANDS)

#Установка шанса на ответ
async def setChance(message: Message) -> None:
    try:
        if(str.isnumeric(message.text.split(' ')[1])):
            global chance
            chance = int(message.text.split(' ')[1])
    except:
        pass
    print(chance) #debug
    await message.answer(f"темп ответа: {chance}")

#отправка решения шара
@bot.on.message(text="/шар")
async def getBall(message: Message) -> None:
    if(randint(0,10)%2):
        solution = "шар отвечает ДА"
    else: solution = "шар отвечает НЕТ"
    forward = MessagesForward(
        conversation_message_ids=[message.conversation_message_id],
        peer_id=message.peer_id,
        is_reply=True
    ).json()
    await message.answer(solution, forward=forward)

#Отправка пословицы
@bot.on.message(text=["/пословица"])
async def poslovitsa(message: Message) -> None:
    # Чтение базы пословиц
    async with open(f"db/poslovitsy.txt") as f:
        db = await f.read()
    db = db.strip().lower()
    # Задержка перед ответом
    await sleep(RESPONSE_DELAY)
    # Генерация пословицы
    text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())
    # Отправка пословицы
    await message.answer(sentence)
    async with open(f"db/poslovitsy.txt", "a") as f:
            await f.write(f"\n{sentence}")

@bot.on.message(text="Толя")
async def greeting(message: Message) -> None:
    api.messages
    global greet
    if(message.from_id == 216672318):
        greet = "батя, "
    else: greet = "и тебе тоже "
    async with open(f"db/greet.txt") as f:
        db = await f.read()
        db = db.strip().lower()
    # Генерация сообщения
    text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())
    await message.answer(greet+sentence)
    greet = ""

#Разбор основных сообщений
@bot.on.message(FromUserRule())
async def talk(message: Message) -> None:
    #peer_id = message.peer_id
    text = message.text.lower()
    # Задержка перед ответом
    await sleep(RESPONSE_DELAY)
    if (text.startswith("/шар")):
        return await getBall(message)
    if(text.startswith("/темп")):
        return await setChance(message)
    if(text.startswith("/команды")):
        return await help(message)
    if("толя" in text):
        return await greeting(message)
    if text:
        # Удаление пустых строк из полученного сообщения
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")
        # Преобразование [id1|@durov] в @id1
        #user_ids = tuple(set(pattern.findall(text)))
        #for user_id in user_ids:
        #    text = re.sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", text)
        # Создание папки db, если не создана
        try:
            mkdir("db")
        except FileExistsError:
            pass
        # Запись нового сообщения в историю беседы
        async with open(f"db/general.txt", "a") as f:
            await f.write(f"\n{text}")
        print(f"\n{text}")
    if (randint(1, 100) < chance):
        # Чтение истории беседы
        async with open(f"db/general.txt") as f:
            db = await f.read()
        db = db.strip().lower()
        # Генерация сообщения
        text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
        sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())
        await message.answer(sentence)

if __name__ == "__main__":
    #pattern = re.compile(r"\[id(\d*?)\|.*?]")
    bot.run_forever()
