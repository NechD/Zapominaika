from utils.Keyboards import *
from utils.work_with_base import *
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from handlers.FSM import *
from utils.create_bot import bot
from handlers import global_variables as gv



#@dp.callback_query_handler(text='rules_btn')
async def rules_btn_menu(callback: types.CallbackQuery):
    await callback.message.answer(f'Выберите тему, на которую вы будете смотреть/создавать правила '
                                  , reply_markup=kb_subjects)
    await Form.chose_theme_for_rule.set()
    await callback.answer()


async def chose_theme_rules(message: types.Message, state: FSMContext):
    gv.us_id = message.from_user.id
    await add_user_and_date_in_base(gv.us_id)
    answer = message.text.lower()
    gv.chosen_theme = answer
    gv.question_formulate = await take_question_formulate(gv.chosen_theme)
    await message.reply(emojis.encode("Отлично!"), reply_markup = types.ReplyKeyboardRemove())
    await message.reply(emojis.encode(f'Тема установлена "{gv.chosen_theme}"\n'), reply_markup=rule_kb)
    await state.finish()



#@dp.callback_query_handler(state ='*', text='fast_rule1')
async def fast_create_rule(callback: types.CallbackQuery):
    global question, question_create, question_create_answer, question_id
    global flag
    print(gv.question_id)
    question_id, question_create, question_create_answer, *other = await select_everything_for_rule(gv.question_id)
    us_id = callback.message.from_user.id
    user_rule_from_base = await show_my_rule(us_id, question_id)
    if user_rule_from_base:
        await callback.message.answer(f'Ваше текущее мнемоническое правило {user_rule_from_base}',
                                      f'Cейчас создадим новое, если вы не хотите, нажмите /cancel',
                                      reply_markup=cancel_kb)
        flag = 'update_pravilo'
        await Form.mem_rule_crt.set()
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {gv.chosen_theme} \n'
                                      f'Вопрос: {gv.question_formulate} "{gv.question}"?\n'
                                      f'Ответ: {question_create_answer} \n')
    else:
        await callback.message.answer(f'Введите правило\n'
                                      f'Тема: {gv.chosen_theme} \n'
                                      f'Вопрос: {gv.question_formulate} "{gv.question}"? \n'
                                      f'Ответ: {question_create_answer} \n')
        await Form.mem_rule_crt.set()
        flag = 'create_pravilo'
    await callback.answer()



# Показать правила
#@dp.callback_query_handler(text='rules_show_btn')
async def rules_show(callback: types.CallbackQuery):
        global all_rules
        all_rules = await show_all_my_rules(gv.chosen_theme, gv.us_id)
        await callback.message.answer(f'Будут показаны мнемонические правила по теме: {gv.chosen_theme}')
        if all_rules:
            all_rules_5_f = all_rules[0:5]
            if gv.chosen_theme not in ['флаг-страна']:
                for_print2 = [(f"Вопрос: {gv.question_formulate} '{question}'?, \n "
                               f"Ответ: {answer}, \n "
                               f"Мнемо-правило: {rule} \n") for question, answer, rule, link in all_rules_5_f]
                await callback.message.answer('\n'.join(for_print2), reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            else:
                for i in all_rules_5_f:
                    question, answer, rule, link = i
                    await bot.send_photo(chat_id=callback.message.chat.id, photo=link)
                    await callback.message.answer(f'Вопрос: {gv.question_formulate} {question}? \n'
                                                  f'Ответ: {answer}, \n'
                                                  f'Мнемо-правило: {rule} \n')
                await callback.message.answer('Показать еще правила?', reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            all_rules = all_rules[5:]
        else:
           await callback.message.answer(f'У вас нет мнемо-правил')


#@dp.callback_query_handler(text='rules_show_next_rules_btn')
async def rules_show_next_rules(callback: types.CallbackQuery):
    global all_rules
    if all_rules:
        all_rules_5_f = all_rules[0:5]
        if gv.chosen_theme not in ['флаг-страна']:
            for_print2 = [(f"Вопрос: {gv.question_formulate} '{question}'?, \n "
                           f"Ответ: {answer}, \n "
                           f"Мнемо-правило: {rule} \n ") for question, answer, rule, link in all_rules_5_f]
            await callback.message.answer('\n'.join(for_print2), reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            all_rules = all_rules[5:]
        else:
            for i in all_rules_5_f:
                question, answer, rule, link = i
                await bot.send_photo(chat_id=callback.message.chat.id, photo=link)
                await callback.message.answer(f'Вопрос: {gv.question_formulate} {question}? \n'
                                                  f'Ответ: {answer}, \n '
                                                  f'Мнемо-правило: {rule} \n')
                await callback.message.answer('Показать еще правила?', reply_markup=rule_kb_3, parse_mode='MARKDOWN')
            all_rules = all_rules[5:]
    else:
        await callback.message.answer('Мнемо-правил больше нет', reply_markup=rule_kb_3)




#@dp.callback_query_handler(text='rules_show_questions')
async def rules_create_show_next(callback: types.CallbackQuery):
    global dict_ques_answ
    prom = dict_ques_answ[0:5]
    for_print = [(f"Вопрос: {question}, "
                  f"Ответ: {answer}") for number, question, answer, *other in prom]
    await callback.message.answer('\n'.join(for_print), reply_markup=rule_kb_2, parse_mode='MARKDOWN')
    dict_ques_answ = dict_ques_answ[5:]


#@dp.callback_query_handler(text='rules_create_show_quest_btn')
async def rules_create_show_next_2(callback: types.CallbackQuery):
    global question
    global question_id
    global chosen_theme
    global dict_ques_answ
    await callback.message.answer(f'Сейчас вы создадите свое мнемоническое правило \n бот будет показывать по 5 '
                                  'вопросов и ответов, \n Для создания правила на '
                                  f'"создать правило" \n Тема: {gv.chosen_theme} ', reply_markup=rule_kb_2)
    if gv.chosen_theme:
        flag = True  # тема выбрана - печатаем с текстом "сгенерированы вопросы по теме"
    else:
        gv.chosen_theme = ('страна-столица')
        flag = False
    dict_ques_answ = await select_questions_for_theme(gv.chosen_theme)
    await callback.answer()

#@dp.callback_query_handler(text='rules_create_show_next_btn')
async def rules_create_show_next_3(callback: types.CallbackQuery):
    global dict_ques_answ
    prom = dict_ques_answ[0:5]
    if gv.chosen_theme not in ['флаг-страна', 'архитектура, понятия']:
        for_print = [(f"Вопрос: {gv.question_formulate} '{question}'?, "
                      f"Ответ: {answer}") for number, question, answer, *other in prom]
        await callback.message.answer('\n'.join(for_print), reply_markup=rule_kb_2, parse_mode='MARKDOWN')
        dict_ques_answ = dict_ques_answ[5:]
    else:
        for i in prom:
            number, question, answer, link = i
            if link:
                await bot.send_photo(chat_id=callback.message.chat.id, photo=link)
            await bot.send_message(chat_id=callback.message.chat.id, text=(f"Вопрос: {gv.question_formulate} '{question}'?, "))
            await callback.message.answer(f'Ответ: {answer}')
        await bot.send_message(chat_id=callback.message.chat.id,
                               text=(f"Хотите создать правило для одного из вопросов выше?"),
                               reply_markup = rule_kb_2)


#@dp.callback_query_handler(text='rules_create_btn')
async def create_button_1(callback: types.CallbackQuery):
    await callback.message.answer('Сейчас вы создадите мнемоническое правило')
    await Form.mem_rule.set()
    await callback.message.answer('Введите вопрос, для ответа на который хотите создать мнемо-правило, регистр неважен')
    await callback.answer()


# раздел "правила", проверка, что правила нет
#@dp.message_handler(state=Form.mem_rule)
async def rule_ask(message: types.Message, state: FSMContext):
    global question_create
    global question_id
    global question_create_answer
    global flag
    global must_find
    global us_id
    quest_to_create_rule = message.text
    is_there_this_question = await is_there_question_in_base(quest_to_create_rule, gv.chosen_theme)
    if is_there_this_question:
        question_id, question_create, question_create_answer, *other = await select_everything_for_rule(quest_to_create_rule)
        us_id = message.from_user.id
        user_rule_from_base = await show_my_rule(us_id, question_id)
        if user_rule_from_base:
            await message.answer(f'Ваше текущее мнемоническое правило {user_rule_from_base}'
                                          f'Cейчас создадим новое)')
            # возможно стоит прописать внутренний cancel для отмены конкретного действия
            flag = 'update_pravilo'
            await Form.mem_rule_crt.set()
            await message.answer('Теперь введите мнемо-правило')
        else:
            await message.answer(f'Тема: {gv.chosen_theme}\n'
                                 f'Вопрос: {question_create} \n Ответ: {question_create_answer}')
            await Form.mem_rule_crt.set()
            await message.answer('Введите мнемо-правило')
            flag = 'create_pravilo'
    else:
        await message.reply(emojis.encode('Данного вопроса нет в списке, попробуйте ещё раз. \nДля выхода нажмите'),
                            reply_markup=cancel_kb)



# раздел "правила", создание правила
#@dp.message_handler(state=Form.mem_rule_crt)
async def ust_pravilo(message: types.Message, state: FSMContext):
    global question_id
    global flag
    pravilo = message.text
    us_id =  message.from_user.id
    if flag == 'update_pravilo':
        await update_my_rule(pravilo, us_id, question_id)
        await message.reply(f'Мнемо-правило для {question_create} успешно обновлено "{pravilo}"')
        await state.finish()
        await message.reply(f'.', reply_markup=correct_kb)
    elif flag == 'create_pravilo':
        await create_my_rule(us_id, question_id, pravilo)
        await message.reply(f'Мнемо-правило для {question_create} успешно создано "{pravilo}"')
        await state.finish()
        await message.reply(f'.', reply_markup=correct_kb)

def register_handlers_rules(dp: Dispatcher):
    dp.register_callback_query_handler(rules_btn_menu, state = '*', text='rules_btn')
    dp.register_callback_query_handler(fast_create_rule, state='*', text='fast_rule1')
    dp.register_callback_query_handler(rules_show, state='*', text='rules_show_btn')
    dp.register_callback_query_handler(rules_show_next_rules, state='*', text='rules_show_next_rules_btn')
    dp.register_callback_query_handler(rules_create_show_next, state='*', text='rules_show_questions')
    dp.register_callback_query_handler(rules_create_show_next_2, state='*', text='rules_create_show_quest_btn')
    dp.register_callback_query_handler(rules_create_show_next_3, state='*', text='rules_create_show_next_btn')
    dp.register_callback_query_handler(create_button_1, state='*', text='rules_create_btn')
    dp.register_message_handler(rule_ask, state=Form.mem_rule)
    dp.register_message_handler(ust_pravilo, state=Form.mem_rule_crt)
    dp.register_message_handler(chose_theme_rules, state=Form.chose_theme_for_rule)
