from utils.Keyboards import *
from aiogram import Dispatcher,  types
from utils.create_bot import bot
from utils.work_with_base import add_user_and_date_in_base

# @dp.callback_query_handler(text='examples')
async def example_call(callback: types.CallbackQuery):
    id_1 = callback.message.chat.id
    await add_user_and_date_in_base(id_1)
    await callback.message.answer(emojis.encode(f"Здесь можно посмотреть примеры техник")
                                  , parse_mode='MARKDOWN', reply_markup=example_kb)
    await callback.answer()

# @dp.callback_query_handler(text='example_1')
async def example_1_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f' 1-ГЖ. 2-ДТ. 3-КХ. 4-ЧЩ. 5-ПБ. 6-ШЛ. 7-СЗ. 8-ВФ. 9-РЦ. '
                                                f'0-НМ.\n1608 - год '
                                                f'изобретения телескопа:telescope: . 1608 = 16 и 08. (Г)аи(ш)ник '
                                                f'неводом вытащил телескоп. '
                                                f'Г-1,Ш-6. Н-0, В-8. Гаишник:oncoming_police_car:  и '
                                                f'невод:fishing_pole_and_fish: '
                                                f' -ключевые слова, первые две согласных которых зашифрованы в цифры.'),
                                  parse_mode='MARKDOWN', reply_markup=inlineexample_1_1kb)
    await callback.answer()


# @dp.callback_query_handler(text='example_2')
async def example_2_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Если Вам необходимо запомнить сложное словосочетание '
                                                f'(международная конвенция),'
                                                f' достаточно просто запомнить слова, близкие по значению к '
                                                f'запоминаемым: '
                                                f'международный :earth_asia: - мировой, конвенция :scroll: - условие.'),
                                  reply_markup=cancel_kb)
    await callback.answer()


# @dp.callback_query_handler(text='example_3')
async def example_3_def(callback: types.CallbackQuery):
    await callback.message.answer(emojis.encode(f'Необходимо запомнить два слова КОТ :cat:  и МОЛОКО '
                                                f':baby_bottle: . '
                                                f'Связь при ассоциации должна быть необычной, нестандартной, '
                                                f'невероятной. '
                                                f'\n КОТ плавает:swimmer:  в стакане с МОЛОКОМ.'),
                                  parse_mode='MARKDOWN', reply_markup=cancel_kb)
    await callback.answer()

async def example_1_1def(callback: types.CallbackQuery):
    await bot.send_photo(chat_id=callback.message.chat.id, photo='https://coollib.com/i/55/425555/i_047.jpg')
    await callback.message.answer(f'У вас есть таблица. \n'
                                  f'Например, вы хотите запомнить дату изобретения '
                                                f'телескопа – 1608 год.\n'
                                                f'1)	Разбиваете дату по 2 цифры – 16 и 08\n'
                                                f'2)	Берете первое число – 16.'
                                                f'Смотрите, какой буквой шифруется цифра «1» - Г или Ж \n'
                                                f'Цифра «6» – П или Б. \n'
                                                f'Итак, теперь вам надо придумать слово, в котором первые две согласные '
                                                f'будут либо: ГП, ГБ, ЖП, ЖБ.\n'
                                                f'Под это подходят слова – гол, гольф, жулик, глаз. \n'
                                                f'То есть число 16 у нас зашифровано как глаз, потому что в ЦБК Г  = 1, а Л = 6'
                                                ,reply_markup=inlineexample_1_2kb)
    await callback.answer()

async def example_1_2def(callback: types.CallbackQuery):
    await callback.message.answer(f'3)	Берем второе число и действуем также 08\n'
                                                f'0 – «Н» или М»\n'
                                                f'8 – «В» или «Ф»\n'
                                                f'Под это подходят слова НаВоз или МаФия\n'
                                                f'Пусть вы выбрали Глаз – для зашифровки 16, Мафия – для зашифровки 08.\n'
                                                f'Тогда вам достаточно cвязать "глаз, новости и телескоп", чтобы запомнить 1608 год.'
                                                ,reply_markup=cancel_kb)
    await callback.answer()

def register_handlers_examples(dp: Dispatcher):
    dp.register_callback_query_handler(example_call, state = '*', text='examples')
    dp.register_callback_query_handler(example_2_def, state='*', text='example_2')
    dp.register_callback_query_handler(example_3_def, state='*', text='example_3')
    dp.register_callback_query_handler(example_1_def, state='*', text='example_1')
    dp.register_callback_query_handler(example_1_1def, state='*', text='example_1_1')
    dp.register_callback_query_handler(example_1_2def, state='*', text='example_1_2')
