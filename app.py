from aiogram import executor
from utils.work_with_base import *
from utils.create_bot import dp

async def on_startup(_):
    await db_start()


from handlers import subjects, start, cancel, technic, exam_train, rules, other, second_menu, examples, admin_statistics, user_statistics
cancel.register_handlers_cancel(dp)
start.register_handlers_start(dp)
second_menu.register_handlers_second_menu(dp)
subjects.register_handlers_subjects(dp)
technic.register_handlers_technic(dp)
examples.register_handlers_examples(dp)
exam_train.register_handlers_exam_train(dp)
rules.register_handlers_rules(dp)
admin_statistics.register_handlers_admin_statistics(dp)
user_statistics.register_handlers_user_stat(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
