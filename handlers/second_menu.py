from utils.keyboards import *
from aiogram import Dispatcher, types
from utils.work_with_base import add_user_and_date_in_base

async def process_exam_menu(callback: types.CallbackQuery):
    id_1 = callback.message.chat.id
    await add_user_and_date_in_base(id_1)
    await callback.message.answer("Доступны следующие команды: \n"
                                  "Тренировка - для проверки знаний \n"
                                  "Правила - посмотреть свои мнемонические правила",
                                  reply_markup=exam_kb)
    await callback.answer()

def register_handlers_second_menu(dp: Dispatcher):
    dp.register_callback_query_handler(process_exam_menu, state = '*', text='exam_btn')