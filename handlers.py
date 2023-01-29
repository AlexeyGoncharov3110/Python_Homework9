from aiogram import types
from loader import dp
from random import randint
max_count = 150
total = 0
new_game = False


@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Привет {name} , если хочешь поиграть '
                         ' отправь сообщение : /new_game '
                         'Для настройки колличества конфет на столе напиши в сообщении /set и кол-во конфет в цифрах')


@dp.message_handler(commands=['new_game'])
async def mes_new_game(message: types.Message):
    global total
    global new_game
    global max_count
    total = max_count
    new_game = True
    first_move=randint(0,1)
    if first_move:
        await message.answer(f'Игра началась. Первым ходит {message.from_user.first_name} ')
    else:
        await message.answer(f'Игра началась. Первым ходит Ботяра ')
        await bot_turn(message)



@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global max_count
    global new_game
    name = message.from_user.first_name
    count = message.text.split()[1]
    if not new_game:
        if count.isdigit():
            max_count = int(count)
            await message.answer(f'Конфет теперь {max_count} штук ')
        else:
            await message.answer(f'{name} ,  напишите цифрами ')
    else:
        await message.answer(f'{name} , нельзя менять правила во время игры  ')


@dp.message_handler()
async def mes_take_candy(message: types.Message):
    global total
    global new_game
    name = message.from_user.first_name
    count = message.text
    if new_game:
        if message.text.isdigit() and 0 < int(message.text) < 29:
            total -= int(message.text)
            if total <= 0:
                await message.answer(f'УРРРААА {name} ты победил ')
                await message.answer(f'Если хочешь продолжить отправь сообщение :  /new_game'
                                     ' Если хочешь поменять кол-во конфет на столе ,отправь сообщение /set и кол-во конфет')
                new_game = False
            else:
                await message.answer(f'{name} взял  {message.text} конфет '
                                     f' на столе осталось {total}')
                await bot_turn(message)
        else:
            await message.answer(f'{name} возьмите от 1 до 28 конфет')


async def bot_turn(message: types.Message):
    global total
    global new_game
    bot_take = 0
    if 0 < total < 29:
        bot_take = total
        total -= bot_take
        await message.answer(f'Бот взял  {bot_take} конфет и победил .\n'
                             'Если хочешь продолжить отправь сообщение :  /new_game .\n'
                             'Если хочешь поменять кол-во конфет на столе ,отправь сообщение : /set и кол-во конфет')
        new_game = False
    else:
        remainder = total % 29
        bot_take = remainder if remainder != 0 else 28
        total -= bot_take
        await message.answer(f'Бот взял  {bot_take} конфет '
                             f' на столе осталось {total}')
