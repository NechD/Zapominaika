import emojis
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from handlers.global_variables import VariablesHandler
from handlers.FSM import Form
from utils.create_bot import bot
from utils.keyboards import (cancel_kb, correct_kb, kb_subjects,
                             rule_kb_create_rule, rule_kb_main_menu,
                             rule_kb_more_rules)
from utils.work_with_base import (add_user_and_date_in_base, create_my_rule,
                                  is_there_question_in_base,
                                  select_everything_for_rule,
                                  select_questions_for_theme,
                                  show_all_my_rules, show_my_rule,
                                  take_question_formulate, update_my_rule)


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
    await message.reply(emojis.encode("Отлично!"), reply_markup=types.ReplyKeyboardRemove())
    await message.reply(emojis.encode(f'Тема установлена "{gv.chosen_theme}"\n'), reply_markup=rule_kb_main_menu)
    await state.finish()


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


async def rules_show(
    callback: types.CallbackQuery,
    var_handler: VariablesHandler
):
    """Отправляет все мнемонические правила."""
    var_handler.all_rules = await show_all_my_rules(var_handler.chosen_theme, var_handler.us_id)
    await callback.message.answer(f'Будут показаны мнемонические правила по теме: {var_handler.chosen_theme}')
    if var_handler.all_rules:
        all_rules_f = var_handler.all_rules[0:5]
        if var_handler.chosen_theme != 'флаг-страна':
            for_print2 = [
                (f"Вопрос: {var_handler.question_formulate} '{question}'?, \n "
                 f"Ответ: {answer}, \n "
                 f"Мнемо-правило: {rule} \n"
                 ) for question, answer, rule, link in all_rules_f
            ]
            await callback.message.answer(
                '\n'.join(for_print2),
                reply_markup=rule_kb_more_rules,
                parse_mode='MARKDOWN')
        else:
            for one_rule in all_rules_f:
                var_handler.question, answer, rule, link = one_rule
                await bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=link,
                )
                await callback.message.answer(
                    f'Вопрос: {var_handler.question_formulate} {var_handler.question}? \n'
                    f'Ответ: {answer}, \n'
                    f'Мнемо-правило: {rule} \n',
                )
            await callback.message.answer(
                'Показать еще правила?',
                reply_markup=rule_kb_more_rules,
                parse_mode='MARKDOWN',
            )
        var_handler.all_rules = var_handler.all_rules[5:]
    else:
        await callback.message.answer('У вас нет мнемо-правил')
