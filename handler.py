from aiogram import types
from create import dp
from aiogram.dispatcher import filters
from random import randint
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ikb = InlineKeyboardMarkup(row_width=3)
ikb1 = InlineKeyboardButton(text='Список команд',
                            callback_data='commands')
ikb2 = InlineKeyboardButton('Описание',
                            callback_data='description')
ikb3 = InlineKeyboardButton('Сыграть в игру',
                            callback_data='game')
                        
ikb.add(ikb1, ikb2).add(ikb3)

HELP_COMMAND = """
/start - запуск бота
/help - правила игры
"""
player_takes = 0
bot_takes = 0
candies = 150

@dp.message_handler(commands=['start'])
async def open_kb(message: types.Message):
    await message.answer('Привет! Добро пожаловать в мой бот-чат!',
                          reply_markup=ikb)
    await message.delete()
    file = open('db.csv', 'a')
    file.write(f'{message.from_user.first_name}, {message.from_user.id}, {message.text}\n')
    file.close()
    # await update.message.reply_text(f'/{datetime.datetime.now().time()}')

@dp.message_handler(commands=['help'])
async def mes_start(message: types.Message):
    await message.answer('Правила игры. На столе лежит 150 конфет. Можно взять любое число конфет от 1 до 28. \
    Выигрывает тот, кто возьмет конфеты последним.', reply_markup=ikb)
    await message.delete()


@dp.callback_query_handler()
async def callback_ikb(callback: types.CallbackQuery):
    if callback.data == 'commands':
        await callback.message.answer(HELP_COMMAND, reply_markup=ikb)
        await callback.message.delete()
    elif callback.data == 'description':
        await callback.message.answer('Я создан для игры в конфеты, и мне бы хотелось сыграть с тобой! Отправь /help, чтобы ознакомиться с правилами.', reply_markup=ikb)
        await callback.message.delete()
    if callback.data == 'game':
        await callback.message.answer('Супер! Давай сыграем! Кто ходит первым - я или ты?')
  

# РАБОЧИЙ КОД
@dp.message_handler(text=['Я', 'я', 'I', 'me', 'Me','z', 'Z'])
async def player_turn(message: types.Message):
    global candies
    candies = 150
    await message.answer('На столе лежит 150 конфет. Сколько конфет ты возьмешь?')
    player_first()

@dp.message_handler(text=['ты', 'Ты', 'You', 'you', 'бот','Бот'])
async def bot_turn(message: types.Message):
    await message.answer('Хорошо, я начну.')
    global bot_takes
    global candies
    candies = 150
    await message.answer(f'На столе лежит {candies} конфет')
    bot_takes = candies % 29 if candies % 29 != 0 else randint(1, 28)
    candies = candies - bot_takes
    await message.answer(f'Я взял {bot_takes} конфет. На столе осталось {candies} конфет')
    if candies == 0:
        await message.answer('Я выиграл!', reply_markup=ikb)
        candies = 150
    global player_takes
    if message.text.isdigit:
        player_takes = int(message.text)
        if player_takes < 0 or player_takes > 28:
            await message.answer(f'Так не пойдет! Нужно взять от 1 до 28 конфет. На столе осталось {candies} конфет')
            bot_turn()
            candies = candies
        elif player_takes > 0 or player_takes < 29:
            candies = candies - player_takes
            await message.answer(f'На столе осталось {candies} конфет')
        elif candies == 0:
            await message.answer('Ты выиграл!', reply_markup=ikb)
            candies = 150

  

@dp.message_handler()
async def player_first(message: types.Message):
    global player_takes
    global candies

    if message.text.isdigit:
        player_takes = int(message.text)
        if player_takes < 0 or player_takes > 28:
            await message.answer(f'Так не пойдет! Нужно взять от 1 до 28 конфет. На столе осталось {candies} конфет')
            player_first()
        elif player_takes > 0 or player_takes < 29:
            candies = candies - player_takes
            await message.answer(f'На столе осталось {candies} конфет')
        elif candies == 0:
            await message.answer('Ты выиграл!', reply_markup=ikb)
            candies = 150
        global bot_takes
        bot_takes =  candies % 29 if candies % 29 != 0 else randint(1, 28)
        candies = candies - bot_takes
        await message.answer(f'Я взял {bot_takes} конфет. На столе осталось {candies} конфет')
        if candies == 0:
            await message.answer('Я выиграл!', reply_markup=ikb)
            candies = 150
