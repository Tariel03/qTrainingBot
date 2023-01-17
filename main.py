import urllib

import telebot
from telebot import types

bot = telebot.TeleBot("5483861993:AAHs6ueq6_Wd4jenlmMuEKzapHXb4DW7gUA")

import database
import pymysql
from connector import host, dbName, Port, Pass, User

try:
    connection = pymysql.connect(
        host=host,
        port=Port,
        user=User,
        password=Pass,
        database=dbName,
        cursorclass=pymysql.cursors.DictCursor

    )
except Exception as ex:
    print(ex)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f"  Привет, {message.from_user.first_name} {message.from_user.last_name}"
    bot.send_message(message.chat.id, mess, parse_mode="html")
    # bot.send_message(message.chat.id, "Выберите для продолжения : ")
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    mangaButton = types.KeyboardButton("/manga")
    animeButton = types.KeyboardButton("/anime")
    characterButton = types.KeyboardButton("/character")
    chooseButton = types.KeyboardButton("/id")
    markup.add(mangaButton, animeButton, chooseButton, characterButton)
    sticker = open("helloNaruto.webp", "rb")
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Begin by choosing: ", reply_markup=markup)


@bot.message_handler(commands=["clear"])
def delete_message(message):
    message_ids = {}
    chat_id = message.chat.id

    message_id = bot.send_message(chat_id, message.text).message_id

    if chat_id in message_ids.keys():
        message_ids[chat_id].append(message_id)
    else:
        message_ids[chat_id] = [message_id]
    for message_id in message_ids[chat_id]:
        bot.delete_message(chat_id, message_id)


@bot.message_handler(commands=['id'])
def get_id(message):
    bot.send_message(message.chat.id, f"Your id {message.from_user.id}", parse_mode="html")
    user = message.from_user
    bot.send_message(message.chat.id, user)
    database.insert(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                    str(message.from_user.is_bot))


@bot.message_handler(commands=["character"])
def get_character(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    engButton = types.InlineKeyboardButton("Sasuke", callback_data="Sasuke")
    rusButton = types.InlineKeyboardButton("Naruto", callback_data="Naruto")
    shikimaruButton = types.InlineKeyboardButton("Shikimaru",callback_data="Shikimaru")
    itachiButton = types.InlineKeyboardButton("Itachi",callback_data="Itachi")
    painButton = types.InlineKeyboardButton("Pain",callback_data="Pain")
    obitoButton = types.InlineKeyboardButton("Obito",callback_data="Obito")
    kakashiButton = types.InlineKeyboardButton("Kakashi",callback_data="Kakashi")
    markup.add(engButton, rusButton,shikimaruButton,itachiButton,painButton,obitoButton,kakashiButton)
    bot.send_message(message.chat.id, "Begin by choosing: ", reply_markup=markup)


@bot.message_handler(content_types=["text"])
@bot.edited_message_handler(content_types=['text'])
def get_message(message):
    if "manga" in message.text:
        # sticker = open("itachi.webp", "rb")
        # bot.send_sticker(message.chat.id, sticker)
        markup = types.InlineKeyboardMarkup(row_width=2)
        engButton = types.InlineKeyboardButton("English", callback_data="english")
        rusButton = types.InlineKeyboardButton("Russian", callback_data="russian")
        markup.add(engButton, rusButton)
        bot.send_message(message.chat.id, "Begin by choosing: ", reply_markup=markup)
    elif "anime" in message.text:
        # sticker = open("coloreditachi.webp", "rb")
        # bot.send_sticker(message.chat.id, sticker)
        markup = types.InlineKeyboardMarkup(row_width=2)
        engButton = types.InlineKeyboardButton("English", callback_data="English")
        rusButton = types.InlineKeyboardButton("Russian", callback_data="Russian")
        markup.add(engButton, rusButton)
        bot.send_message(message.chat.id, "Begin by choosing: ", reply_markup=markup)
    elif message.text == "dice":
        bot.send_dice(message.chat.id, reply_to_message_id=message.message_id, emoji='🎲')
    elif message.text == "basket":
        bot.send_dice(message.chat.id, reply_to_message_id=message.message_id, emoji="🏀")
    elif message.text == "foot":
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_dice(message.chat.id, reply_to_message_id=message.message_id, emoji="⚽", reply_markup=markup)
    elif "done" in message.text:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id, timeout=10)
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Your id {message.from_user.id}", parse_mode="html")
        user = message.from_user
        bot.send_message(message.chat.id, user)
        database.insert(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                        str(message.from_user.is_bot))
    elif message.text == 'check':
        rows = database.select(message.chat.id)
        dict = rows[0]
        print(rows)
        if message.from_user.last_name == dict["last_name"]:
            bot.send_message(message.chat.id, "Success")

        else:
            bot.send_message(message.chat.id, "Fail")
    elif message.text == 'character':
        markup = types.InlineKeyboardMarkup(row_width=2)
        engButton = types.InlineKeyboardButton("Sasuke", callback_data="Sasuke")
        rusButton = types.InlineKeyboardButton("Naruto", callback_data="Naruto")
        shikimaruButton = types.InlineKeyboardButton("Shikimaru", callback_data="Shikimaru")
        itachiButton = types.InlineKeyboardButton("Itachi", callback_data="Itachi")
        painButton = types.InlineKeyboardButton("Pain", callback_data="Pain")
        obitoButton = types.InlineKeyboardButton("Obito", callback_data="Obito")
        kakashiButton = types.InlineKeyboardButton("Kakashi", callback_data="Kakashi")
        markup.add(engButton, rusButton, shikimaruButton, itachiButton, painButton, obitoButton, kakashiButton)
    #
    #
    # else:


@bot.inline_handler(lambda request: request.request == 'text')
def query_text(request):
    serviceurl = 'https://www.google.com/maps/search/?api=1&'
    address = request
    url = serviceurl + urllib.parse.urlencode({'query': address})
    bot.answer_inline_query(request.id, url)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # animation = open("rikaAnimated.tgs", "rb")
    # bot.send_animation(call.message.chat.id, animation, duration=30)
    try:
        if call.data == "Russian":
            markUp = types.InlineKeyboardMarkup(row_width=4)
            animego_button = types.InlineKeyboardButton("animego", url="https://animego.org/anime/naruto-102")
            jutsu_button = types.InlineKeyboardButton("jutsu", url="https://jut.su/naruuto/season-1/")
            animevost_button = types.InlineKeyboardButton("animevost",
                                                          url='https://animevost.org/tip/tv/5-naruto-shippuuden12.html')
            markUp.add(animego_button, animevost_button, jutsu_button)
            bot.send_message(call.message.chat.id, "Go go go", reply_markup=markUp)

        elif call.data == 'English':
            markUp = types.InlineKeyboardMarkup(row_width=4)
            zoro_button = types.InlineKeyboardButton("zoro", url="https://zoro.to/naruto-shippuden-355?ref=search")
            animix_button = types.InlineKeyboardButton("animix", url="https://animixplay.to/v1/naruto")
            markUp.add(animix_button, zoro_button)
            bot.send_message(call.message.chat.id, "Go go go", reply_markup=markUp)
            bot.register_next_step_handler(call.message, get_message)

        elif call.data == 'russian':
            markUp = types.InlineKeyboardMarkup(row_width=3)
            mangalib_button = types.InlineKeyboardButton("mangalib", url='https://mangalib.me/naruto?section=info')
            remanga_button = types.InlineKeyboardButton("remanga", url='https://remanga.org/manga/naruto')
            mangachan_button = types.InlineKeyboardButton('mangachan',
                                                          url="https://manga-chan.me/manga/3170-naruto.html")
            markUp.add(mangalib_button, remanga_button, mangachan_button)
            bot.send_message(call.message.chat.id, "Here are some web-sites for you", reply_markup=markUp)



        elif call.data == 'english':
            markUp = types.InlineKeyboardMarkup(row_width=3)
            kakalot_button = types.InlineKeyboardButton("mangakakalot", url='https://mangakakalot.to/naruto-567')
            owl_button = types.InlineKeyboardButton("mangaowl", url='https://mangaowls.net/single/841/naruto')
            markUp.add(kakalot_button, owl_button)
            bot.send_message(call.message.chat.id, "Here are some web-sites for you", reply_markup=markUp)

        elif call.data == "Sasuke":
            sticker = open("sasuke.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)

        elif call.data == "Naruto":
            sticker = open("naruto.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)

        elif call.data == "Itachi":
            sticker = open("itachi.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)
        elif call.data == "Shikimaru":
            sticker = open("shikimaru.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)
        elif call.data == "Pain":
            sticker = open("pain.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)
        elif call.data == "Kakashi":
            sticker = open("kakashi.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)
        elif call.data == "Obito":
            sticker = open("obito.webp", "rb")
            bot.send_sticker(call.message.chat.id, sticker)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Thanks for the answer!",
                              reply_markup=None)
    except Exception as e:
        print(repr(e))


bot.infinity_polling(timeout=100)
