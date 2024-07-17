
from aiogram import Bot, Dispatcher, executor, types

token = '7171956426:AAFBAbddKaLN8UGkL5GCHE13StWrP6iX7Fk'
bot = Bot(token)
dp = Dispatcher(bot)

Start_markup = types.InlineKeyboardMarkup()

async def amsw(message: types.Message):
    answ = 'купи слона'
    await bot.send_message(message.chat.id, answ, parse_mode='HTML', reply_markup=Start_markup)


@dp.message_handler()
async def amsw(message: types.Message):
    answ = 'Все говорят ' + message.text + ' а ты купи слона'
    await bot.send_message(message.chat.id, answ, parse_mode='HTML', reply_markup=Start_markup)

executor.start_polling(dp)