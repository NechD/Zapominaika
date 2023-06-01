from utils.keyboards import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

#@dp.callback_query_handler(state='*', text='cancel1')
async def cancel_call(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer("Вы вышли в главное меню\n",
                                  reply_markup=inline_kb)
    await callback.answer()

def register_handlers_cancel(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_call, state='*', text='cancel1')