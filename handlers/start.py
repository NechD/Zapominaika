from utils.Keyboards import *
from utils.work_with_base import *
from aiogram import Dispatcher, types
from handlers import global_variables as gv
from aiogram.dispatcher.filters import Text
from utils.create_bot import bot

#@dp.message_handler(commands=['start'])
async def send_welcome1(message: types.Message):
    gv.us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    await save_user_in_base(gv.us_id, us_name, us_sname, username)
    await message.reply(emojis.encode("Привет! :wave:\n Перед тем как мы начнем учиться я хочу спросить,"
                                      "ты знаешь, что такое мнемоправила? \n"),
                                        reply_markup=kb_menu_do_you_know)


#Да
async def send_welcome_yes(message: types.Message):
    gv.us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    await message.reply(emojis.encode("Отлично! :muscle: \n "
                                      "Мы поможем тебе натренировать применение мнемо-правил\n"),
                        reply_markup = types.ReplyKeyboardRemove())

    await bot.send_message(chat_id =message.from_user.id,
                           text=emojis.encode("Краткое инфо по разделам:\n"
                                               "Техники🎒 - покажет мнемо-техники\n"
                                      "Примеры📔 - посмотреть примеры под мнемо-техники \n"
                                      "Темы👁 - выбрать тему для запоминания \n"
                                      "Тренировка💪 - отточить свои знания на наборах вопросов\n"
                                      "Мнемо-правила📜 -  создать/посмотреть/отредактировать созданные правила\n"
                                      "Статистика📈 - посмотреть процент усвоения темы \n"
                                      "Удачи!"),
                                      reply_markup=inline_kb)

#нет
async def send_welcome_no(message: types.Message):
    gv.us_id = message.from_user.id
    await bot.send_message(chat_id =message.from_user.id,
                           text=emojis.encode(
                               "Мнемонические правила – это то, что поможет тебе запомнить информацию просто"),
                           reply_markup=kb_how)

async def send_welcome_no2(message: types.Message):
    gv.us_id = message.from_user.id
    await bot.send_sticker(chat_id =message.from_user.id,
                           sticker='CAACAgIAAxkBAAEGgeJjfPmV8XztCxueTBR-Ul0m7Q8lwQACLQADtZQwNWSdPYwrZTPGKwQ')
    await bot.send_message(chat_id =message.from_user.id,
                           text=emojis.encode(
                               "Вы берете неудобную для запоминания информацию и превращаете ее в легко усваиваемые образы"),
                           reply_markup=kb_start_show_examples)

async def send_welcome_no3(message: types.Message):
    gv.us_id = message.from_user.id
    await bot.send_message(chat_id =message.from_user.id,
                           text="Известная запоминалка цветов радуги🌈\n"
                                "«Каждый Охотник Желает Знать, Где Сидит Фазан» \n"
                                "Форма Италии похожа на сапог \n \n"
                                "Вы  строите ассоциации того, что надо запомнить с тем, что вы хорошо помните.\n"
                                "Мнемоправила бывают разные: стихи, песни, визуальные образы",
                           reply_markup=kb_start_how_you_can_helpme)

async def send_welcome_no4(message: types.Message):
    gv.us_id = message.from_user.id
    await bot.send_message(chat_id =message.from_user.id,
                           text="Мы предлагаем описание техник, примеры, а также начать тренироваться их применять.\n"
                                "Например, выучить флаги, страны, определения.",
                           reply_markup=kb_start_no_finish)

# ВЫЗОВ МЕНЮ
#@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    gv.us_id = message.from_user.id
    await message.reply(emojis.encode("Привет :wave:\n Выберите, пожалуйста, меню: \n"),
                                        reply_markup=inline_kb)

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(send_welcome1, commands=['start'])
    dp.register_message_handler(send_welcome_yes, Text(equals=["да💫", 'Погнали!▶️']))
    dp.register_message_handler(send_welcome_no, Text(equals="нет👂"))
    dp.register_message_handler(send_welcome_no2, Text(equals="как? 👀"))
    dp.register_message_handler(send_welcome_no3, Text(equals="а есть примеры правил?🐺"))
    dp.register_message_handler(send_welcome_no4, Text(equals="И как вы мне поможете разобраться❓"))
    dp.register_message_handler(send_help, commands=['help'])
