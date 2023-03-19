from utils.Keyboards import *
from utils.work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from handlers.FSM import *
from handlers import global_variables as gv

#@dp.callback_query_handler(text='subject1')
async def show_subjects(callback: types.CallbackQuery):
    id_1 = callback.message.chat.id
    await add_user_and_date_in_base(id_1)
    await callback.message.answer('Выберите тему из предложенных', reply_markup=kb_subjects)
    await Form.chose_theme_btn.set()
    await callback.answer()


async def chose_theme(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    gv.chosen_theme = answer
    gv.question_formulate = await take_question_formulate(gv.chosen_theme)
    await message.reply(f'Тема установлена "{gv.chosen_theme}"', reply_markup = types.ReplyKeyboardRemove())
    await message.reply(f'Теперь вы можете начать заниматься', reply_markup=inline_kb)
    await state.finish()


def register_handlers_subjects(dp: Dispatcher):
    dp.register_message_handler(chose_theme, state = Form.chose_theme_btn)
    dp.register_callback_query_handler(show_subjects, state = '*', text='subject1')
