from aiogram import Bot, Dispatcher, executor, types
import os
from test import get_position

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readline()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

images_dir = './images/'


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(msg: types.Message):

    welcome_message = 'Здравствуйте!'
    welcome_message += '\nПо вашей картинке я могу определить: ВСЁ'
    welcome_message += '\nПрикрепите картинку с изображением самолёта. После этого я верну вам его параметры.'
    welcome_message += '\n\nСервис работает в тестовом режиме'

    await msg.reply(welcome_message)

def main_process():
    photo = images_dir + 'image.jpg'
    try:
        params = get_position([photo]) #[{'value': 42}]
        print('\tSUCCESS')
    except:
        print('\tERROR')
        params = []
    os.remove(photo)
    return params

# Загружаем фото
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(msg):
    try:
        await msg['photo'][-1].download(images_dir + 'image.jpg')
        # await bot.send_message(msg.from_user.id, 'Изображение загружено!')
    except:
        await bot.send_message(msg.from_user.id, 'ALARM! Изображение не загружено')
        return
    try:
        params = main_process()
    except:
        await bot.send_message(msg.from_user.id, 'ALARM! Ошибка обработки')
        return

    for item in params:
        resp = ''
        for key, value in item.items():
            resp += f'{key}: {value}\n'
        await bot.send_message(msg.from_user.id, resp)

@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        # appeal_to_map(msg.text)
        
        # await bot.send_photo(msg.from_user.id, msg.photo)
        await bot.send_message(msg.from_user.id, 'Обращение получено.')
    except:
        await bot.send_message(msg.from_user.id, 'Возможно, самолёт не найден...')


if __name__ == '__main__':
    executor.start_polling(dp)
