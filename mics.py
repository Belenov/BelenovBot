from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import Database

# Bot API (Telegram Bot) \\ telegram - BotFather
API_TOKEN = "1893727909:AAHu2rUINfsAlOqKEASRhkhSLpBcRS-I8nM"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Client API (User Bot) \\ https://my.telegram.org/auth
## You can create a fake telegram to verify users. Also, don't forget to make your linked api account an administrator!
### https://goo.su/aD60
API_ID = "YOUR_API_ID" 
API_HASH = "YOUR_API_HASH"
# Channel ID 
## You can find out the chat's ID through the Get My ID bot by forwarding a message from the channel.
CHANNEL_ID = YOUR_CHANNEL_ID
# Database setting
db = Database("database.db")
# Schedule
scheduler = AsyncIOScheduler()
INTERVAL = 10  # Check interval in seconds
#Payment - Yootoken(You can choose another payment system in BotFather)
YOOTOKEN = 'YOUR_YOOTOKEN'
# Message
offerta = "Offertory \n Your text could have been here"
setnickname = "Enter your username!"
registerturn = "You are already registered!"
nameuser = "Your nickname: "
tech = "Technical staff: write him your problem with the related payment."
faq = "This bot provides an opportunity to purchase a subscription to a closed channel."
banlist = set('@/*#!$%^?\[]-_)+=;`~.,<>\'"|')