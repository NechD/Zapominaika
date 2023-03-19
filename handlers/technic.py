from utils.Keyboards import *
from aiogram import Dispatcher,  types
from utils.work_with_base import add_user_and_date_in_base


# @dp.callback_query_handler(text='technic1')
async def technic_call(callback: types.CallbackQuery):
    id_1 = callback.message.chat.id
    await add_user_and_date_in_base(id_1)
    await callback.message.answer(emojis.encode(f"В нашем боте используются следующие техники запоминания\n"
                                                "1. :slot_machine: Метод ЦБК \n"
                                                "Краткое описание: Техника основана на условном соответствии между "
                                                "согласными буквами и цифрами "
                                                " от :zero:  до :nine: . "
                                                " Дату необходимо перевести в слова, а из слов составить фразу "
                                                "связанную с запоминаемой датой \n "
                                                "\n"
                                                "2. :loop: Метод синонимов \n"
                                                "Краткое описание: Техника основана на построении связной "
                                                "цепочки:chains: "
                                                "между словом которое необходимо запомнить со словами схожими по "
                                                "значению и лексическому толкованию с запоминаемым словом. \n "
                                                "\n"
                                                "3.  :wavy_dash:  Метод Ассоциаций \n"
                                                "Краткое описание: Метод основан на построении связи между двумя "
                                                "или более явлениями - "
                                                "Так, например, когда вы видите идущего с лыжами человека — вы "
                                                "вспоминаете о зиме (иными словами, "
                                                " лыжи:snowboarder:  ассоциируются с зимой:cold_face:\n ")
                                  , parse_mode='MARKDOWN', reply_markup=technic_kb)
    await callback.answer()


def register_handlers_technic(dp: Dispatcher):
    dp.register_callback_query_handler(technic_call, state = '*', text='technic1')

