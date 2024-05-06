from createbot import *
import sys
sys.path.append('../')
import bot_handlers


async def on_startup(_):
    print('бот запустился')


bot_handlers.reg_handlers.register_reg_handlers(dp=dp)
bot_handlers.states_handlers.register_states_handler(dp=dp)
bot_handlers.main_handlers.register_main_handler(dp=dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

