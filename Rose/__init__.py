# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

import asyncio
import time
from inspect import getfullargspec
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.types import Message
from Python_ARQ import ARQ
import asyncio
from pyrogram import Client
from config import *
import pymongo

SUPPORT_GROUP = "https://t.me/qiransupport" #If you Don't Know Codes Any error Fixing method please Don't change this.... ):


SUDOERS = SUDO_USERS_ID
LOG_GROUP_ID = LOG_GROUP_ID
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
DB_URI = BASE_DB
MONGO_URL = MONGO_URL

# Don't change this
OWNER_ID = "5069194822"

myclient = pymongo.MongoClient(DB_URI)
dbn = myclient["supun"]

# MongoDB client
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.wbb



async def load_sudoers():
    global SUDOERS
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

bot = Client("supun", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

bot.start()

app = Client("app2", bot_token=BOT_TOKEN, api_id=API_ID1, api_hash=API_HASH1)

app.start()

x = app.get_me()



BOT_ID = 5194020006
BOT_NAME = x.first_name + (x.last_name or "")
BOT_USERNAME = x.username
BOT_MENTION = x.mention
BOT_DC_ID = x.dc_id



#chatdb
chatsdb = db.chats


async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})


#eor help sessions
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
