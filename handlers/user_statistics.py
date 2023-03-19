from utils.Keyboards import *
from utils.work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from handlers.FSM import *
from utils.create_bot import bot
from handlers import global_variables as gv



#@dp.callback_query_handler(text='statistics_btn')
async def statistics_btn_menu(callback: types.CallbackQuery):
    await bot.send_message(chat_id= callback.message.chat.id,
                           text=emojis.encode(
                               "Выберите по какой теме посмотреть % усвоения"),
                           reply_markup=kb_subjects)
    await Form.user_statistics.set()


#Вывод статы по теме
#@dp.callback_query_handler(state ='user_statistics')
async def statistics_theme(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    gv.us_id = message.from_user.id
    right_answers = await get_statistics_right_answers(gv.us_id, answer)
    right_answers = len(right_answers)
    all_answers = await get_statistics_all_answers(gv.us_id, answer)
    all_answers = len(all_answers)
    all_questions = await get_statistics_get_all_questions(gv.us_id, answer)
    all_questions = len(all_questions)
    usvoenie_temi = round(right_answers*100/all_questions, 2)
    otv_na_vopr = round(right_answers*100/all_questions, 2)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Процент усвоения темы {usvoenie_temi}% \n\n'
                                f'Количество ответов(с верностью более 50%) {right_answers} из {all_answers} отвеченных \n\n'
                                f'Всего дано ответов на {all_answers} из {all_questions} содержащихся в базе вопросов')






def register_handlers_user_stat(dp: Dispatcher):
    dp.register_callback_query_handler(statistics_btn_menu, state = '*', text='statistics_btn')
    dp.register_message_handler(statistics_theme, state=Form.user_statistics)


