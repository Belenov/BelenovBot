import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ChatMemberMember
from aiogram.types import ChatMemberLeft
from aiogram.types import ChatMemberAdministrator
from pyrogram.methods.messages import send_message
import markups as nav
import time
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.errors.exceptions import UserAdminInvalid
from mics import CHANNEL_ID, API_ID, API_HASH, INTERVAL, dp, db, scheduler, YOOTOKEN, API_TOKEN, offerta, setnickname, registerturn, nameuser, tech, faq, banlist
import warnings
from prettytable import from_db_cursor
import sqlite3
import threading
from colorama import Fore, Back, Style
from tqdm import tqdm
import sys



# Console Work
x = 30
current_ts = time.time()

# Disables spam in the console
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.ERROR)


app = Client(session_name="linux_desktop", api_id=API_ID, api_hash=API_HASH, app_version="0.1",
             device_model="Linux ARM x64", system_version="4.4.7", lang_code="ru")




logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


#  Time and translate date 
def days_to_seconds(days):
    return days * 24 * 60 * 60


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt


# Console


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT `id`,`user_id`,`nickname`,`time_sub` ,`signup` FROM `users`")
mytable = from_db_cursor(cursor)


def console(command, banner):
    time.sleep(10)
    banner == print(Back.GREEN + Fore.WHITE + Style.BRIGHT + '[SERVER] The console is up and running!' + Style.RESET_ALL)
    while True:
        time.sleep(1)
        command = str(input(Style.BRIGHT + "> "))
        if command == "table":
            print(mytable)
        elif command == "help":
            print(Style.BRIGHT + "+-----------------------+")
            print(Style.BRIGHT + "| help - Command output |")
            print(Style.BRIGHT + "| table - Data from DB  |")
            print(Style.BRIGHT + "+-----------------------+")
        elif command == "stop":
            babi = int(input(Back.RED +  Style.BRIGHT + "[SERVER] Are you sure you want to stop the bot?(Y/N)" + Style.RESET_ALL ))
            if babi == "Y":
                sys.exit()
            elif babi == "N":
                print(Back.RED +  Style.BRIGHT + "[SERVER] The bot will be stopped!" + Style.RESET_ALL )
            else:
                print(Back.RED +  Style.BRIGHT + "[SERVER] Unknown command!" + Style.RESET_ALL )
                return
        else: 
            print("Unknown command!")
        


con = threading.Thread(target=console, args=(x, current_ts))
con.start()


# Main code

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not (db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, offerta)
        await bot.send_message(message.from_user.id, setnickname)
    else:
        await bot.send_message(message.from_user.id, registerturn, reply_markup=nav.mainMenu)
        


@dp.message_handler()
async def bot_message(message: types.Message):
    user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    user_count = await dp.bot.get_chat_members_count(CHANNEL_ID)
    if message.chat.type == 'private':
        if message.text == '📃PROFILE':
            user_nickname = nameuser + db.get_nickname(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            zriteli = (f"\nThe number of participants in the channel: {user_count}")
            if not user_sub:
                user_sub = "No"
            user_sub = "\nSubscription: " + user_sub
            await bot.send_message(message.from_user.id, user_nickname + user_sub + zriteli)

        elif message.text == '💎SUBSCRIBE':
            await bot.send_message(message.from_user.id, "Choose how long you want to subscribe",
                                   reply_markup=nav.sub_inline_markup)

        elif message.text == '🛂LINK TO THE PRIVATE CHANNEL':
            if db.get_sub_status_new(message.from_user.id):
                if isinstance(user_status, ChatMemberLeft):
                    expire_date = datetime.now() + timedelta(days=1)
                    link = await bot.create_chat_invite_link(CHANNEL_ID, expire_date, 1)
                    await message.reply(link.invite_link, parse_mode="HTML")
                elif isinstance(user_status, ChatMemberMember):
                    await bot.send_message(message.from_user.id, "You are already in the channel!")
                elif isinstance(user_status, ChatMemberAdministrator):
                    expire_date = datetime.now() + timedelta(days=1)
                    link = await bot.create_chat_invite_link(CHANNEL_ID, expire_date, 1)
                    await bot.send_message(message.from_user.id, "You are an Administrator in the channel.")
                    await message.reply(link.invite_link, parse_mode="HTML")
            else:
                await bot.send_message(message.from_user.id, "Buy a subscription")


        elif message.text == '📝TECHNICAL SUPPORT':
            await bot.send_message(message.from_user.id, tech)

        elif message.text == '📋FAQ':
            await bot.send_message(message.from_user.id, faq)

        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 15:
                    await bot.send_message(message.from_user.id, "Nickname must not exceed 15 characters")
                elif set(message.text) & banlist:
                    await bot.send_message(message.from_user.id, "You drove a forbidden symbol")
                elif len(message.text) < 5:
                    await bot.send_message(message.from_user.id, "Nickname must not be less than 5 characters")

                else:
                    db.set_signup(message.from_user.id, "Done")
                    await bot.send_message(message.from_user.id, "Регистарция прошла успешна.",
                                           reply_markup=nav.mainMenu)
           



@dp.message_handler()
async def check_subscribers():
    async with app:
        for user in await app.get_chat_members(chat_id=CHANNEL_ID, limit=10000):
            user_id = user.user.id
            is_subscribed = db.get_sub_status(user_id)
            if not is_subscribed:
                try:
                    await app.kick_chat_member(CHANNEL_ID, user_id)
                    print(f"User {user_id} removed from the channel.")
                except UserAdminInvalid:
                    pass  


async def on_startup(dispatcher: Dispatcher):
    scheduler.add_job(check_subscribers, "interval", seconds=INTERVAL)
    scheduler.start()


# Payment

@dp.callback_query_handler(text="submonth")
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Subscription",
                           description="You subscribe for one month", payload="month_sub", provider_token=YOOTOKEN,
                           currency="RUB", start_parameter="test_bot", prices=[{"label": "Руб", "amount": 150000}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "You have been issued a one-month subscription!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)