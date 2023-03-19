import sqlite3
import random as r
from datetime import date


async def db_start():
    global conn, cursor
    conn = sqlite3.connect('all_in_one_base.db', check_same_thread=False)
    cursor = conn.cursor()


async def save_user_in_base(user_id: int, user_name: str, user_surname: str, username: str):
    user = cursor.execute(f"SELECT * FROM user_id_base WHERE user_id = '{user_id}'").fetchone()
    if not user:
        cursor.execute('INSERT INTO user_id_base (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                       (user_id, user_name, user_surname, username))
        conn.commit()
    else:
        print('user in base')
    today = date.today()
    user_today = cursor.execute(f"SELECT * "
                                f"FROM active_users "
                                f"WHERE user_id = '{user_id}' and date_interaction = '{today}'").fetchone()
    if not user_today:
        print("user wasn't in base today")
        cursor.execute('INSERT INTO active_users (user_id, date_interaction) VALUES (?, ?)', (user_id, today))
        conn.commit()
        print("user added to base")
    else:
        print('today user already work with bot')


async def select_all_themes_from_base():
    all_themes = cursor.execute('SELECT DISTINCT theme FROM questions_base').fetchall()
    all_themes = [i[0] for i in all_themes]
    print(all_themes)
    return all_themes


async def select_questions_for_theme(chosen_theme):
    cursor.execute(
        f"SELECT question_id, question, right_answer, link FROM questions_base WHERE theme = '{chosen_theme}'")
    dict_ques_answ = cursor.fetchall()
    r.shuffle(dict_ques_answ)
    return dict_ques_answ


async def show_my_rule(us_id, question_id):
    user_rule_from_base = cursor.execute(f"SELECT mnemonic_rule FROM user_rules_2 WHERE user_id = "
                                         f"'{us_id}' AND question_id = '{question_id}'").fetchone()
    if not user_rule_from_base:
        return False
    user_rule_from_base = str(*user_rule_from_base)
    return user_rule_from_base


async def select_everything_for_rule(question_id):
    cursor.execute(
        f"SELECT question_id, question, right_answer, link FROM questions_base WHERE question_id = '{question_id}'")
    row_with_question_from_base = cursor.fetchone()
    return row_with_question_from_base


async def show_all_my_rules(chosen_theme, us_id):
    all_rules = cursor.execute(f"SELECT question, right_answer, mnemonic_rule, link "
                               f"FROM questions_base INNER JOIN user_rules_2 "
                               f"ON questions_base.question_id = user_rules_2.question_id "
                               f"WHERE mnemonic_rule IS NOT NULL "
                               f"AND theme = '{chosen_theme}'"
                               f"AND user_id = '{us_id}'").fetchall()
    return all_rules


async def update_my_rule(pravilo, us_id, question_id):
    cursor.execute(f"UPDATE user_rules_2 SET mnemonic_rule == ? WHERE user_id  == ? AND question_id  == ? ",
                   (pravilo, us_id, question_id))
    conn.commit()


async def create_my_rule(us_id, question_id, pravilo):
    cursor.execute('INSERT INTO user_rules_2 (user_id, question_id, mnemonic_rule) VALUES (?, ?, ?)',
                   (us_id, question_id, pravilo))
    conn.commit()


async def is_there_question_in_base(quest_to_create_rule, chosen_theme):
    cursor.execute(f"SELECT question_id "
                   f"FROM questions_base "
                   f"WHERE question = '{quest_to_create_rule}' "
                   f"AND theme = '{chosen_theme}' ")
    is_there_this_question = cursor.fetchone()
    return is_there_this_question


async def take_question_formulate(chosen_theme):
    cursor.execute(f"SELECT question_for_theme "
                   f"FROM theme_question "
                   f"WHERE theme = '{chosen_theme}'")
    take_question_itog = str(*cursor.fetchone())
    return take_question_itog


async def add_user_and_date_in_base(user_id: int):
    today = date.today()
    user_today = cursor.execute(f"SELECT * "
                                f"FROM active_users "
                                f"WHERE user_id = '{user_id}' and date_interaction = '{today}'").fetchone()
    if not user_today:
        print("user wasn't in base today")
        cursor.execute('INSERT INTO active_users (user_id, date_interaction) VALUES (?, ?)', (user_id, today))
        conn.commit()
        print("user added to base")
    else:
        print('today user already work with bot')


async def get_number_users_per_day(day):
    today = day
    user_today = cursor.execute(f"SELECT user_id "
                                f"FROM active_users "
                                f"WHERE date_interaction = '{today}'").fetchall()
    print(user_today)
    print(len(user_today))
    return (len(user_today))


async def add_question_to_base(user_id, question_id, quantity_right_answers, theme, quantity_answers=1):
    today = date.today()
    is_there_this_question = cursor.execute(f"SELECT * "
                                            f"FROM statistics_question "
                                            f"WHERE user_id = '{user_id}' "
                                            f"and question_id = '{question_id}'").fetchall()
    print(is_there_this_question)
    if not is_there_this_question:
        print('no question in base')
        cursor.execute(
            'INSERT INTO statistics_question (user_id, question_id, quantity_answers, quantity_right_answers,  theme) VALUES (?, ?,?, ?, ? )',
            (user_id, question_id, quantity_answers, quantity_right_answers, theme))
        conn.commit()
        print("user and his question add to base")
    else:
        user_id, question_id, quantity_answers_in_base, quantity_right_answers_in_base, theme = is_there_this_question[
            0]
        quantity_right_answers_final = quantity_right_answers + quantity_right_answers_in_base
        quantity_answers_final = quantity_answers_in_base + quantity_answers
        print(f'quantity_answers_final {quantity_answers_final}')
        cursor.execute(
            f"UPDATE statistics_question SET quantity_answers = '{quantity_answers_final}', quantity_right_answers = '{quantity_right_answers_final}' "
            f"WHERE user_id  = '{user_id}' AND question_id  = '{question_id}'")
        conn.commit()


async def get_statistics_right_answers(user_id, theme):
    select_from_base = cursor.execute(f"SELECT question_id "
                                      f"FROM statistics_question "
                                      f"WHERE user_id = '{user_id}' and (quantity_right_answers/quantity_answers) > 0.5 "
                                      f"AND theme = '{theme}'").fetchall()
    return select_from_base


# all_questions = len(cursor.execute(f"SELECT question_id FROM questions_base WHERE theme = '{theme}'").fetchall())
# return (right_answers*100/all_questions)

async def get_statistics_all_answers(user_id, theme):
    select_from_base_all_answers = cursor.execute(f"SELECT question_id "
                                                  f"FROM statistics_question "
                                                  f"WHERE user_id = '{user_id}'"
                                                  f"AND theme = '{theme}'").fetchall()
    return select_from_base_all_answers


async def get_statistics_get_all_questions(user_id, theme):
    all_questions = cursor.execute(f"SELECT question_id "
                                   f"FROM questions_base "
                                   f"WHERE theme = '{theme}'").fetchall()
    print(all_questions)
    return all_questions


async def get_uncorrest_statics(user_id, theme):
    select_from_base_uncorrect_questions = cursor.execute(f"SELECT question_id "
                                                          f"FROM statistics_question "
                                                          f"WHERE user_id = '{user_id}' and (quantity_right_answers*10/quantity_answers)<5 "
                                                          f"AND theme = '{theme}'").fetchall()
    uncorrest_ans = select_from_base_uncorrect_questions
    print(f' bad {uncorrest_ans}')
    return uncorrest_ans


async def get_statistics_get_good_questions(user_id, theme):
    select_from_base_good_questions = cursor.execute(f"SELECT question_id "
                                                     f"FROM statistics_question "
                                                     f"WHERE user_id = '{user_id}' and (quantity_right_answers*10/quantity_answers) >= 5 "
                                                     f"AND theme = '{theme}'").fetchall()
    correct_ans = select_from_base_good_questions
    print(f' good_ques {correct_ans}')
    return correct_ans
