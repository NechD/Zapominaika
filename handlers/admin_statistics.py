from utils.Keyboards import *
from utils.work_with_base import *
from aiogram import Dispatcher, types
from utils.create_bot import bot
from handlers.FSM import *
from aiogram.dispatcher import FSMContext


#@dp.message_handler(commands=['statistics738'])
async def show_statistics(message: types.Message):
    await message.reply(emojis.encode("Привет! Я могу тебе показать админскую статистику, выбери день в формате YYYY-MM-DD \n"),
                                        reply_markup=cancel_kb)
    await Form.admin_statistics.set()


async def send_statistics_day(message: types.Message, state: FSMContext):
    answer = message.text
    todayy = await get_number_users_per_day(answer)
    await bot.send_message(chat_id =message.from_user.id,
                           text=emojis.encode(f"Количество активных пользователей за дату: {todayy}"),
                           reply_markup=cancel_kb)
    await message.reply(f'Можете ввести ещё дату ', reply_markup = types.ReplyKeyboardRemove())



def register_handlers_admin_statistics(dp: Dispatcher):
    dp.register_message_handler(show_statistics, commands=['statistics738'], state='*')
    dp.register_message_handler(send_statistics_day, state=Form.admin_statistics)

