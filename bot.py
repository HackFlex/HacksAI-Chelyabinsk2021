from aiogram import Bot, Dispatcher, executor, types
import os
from get_param import get_param

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.readline()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

images_dir = './images/'
image_file = 'image.jpg'


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(msg: types.Message):

    welcome_message = 'Здравствуйте!'
    welcome_message += '\nПрикрепите картинку с изображением самолёта. После этого я верну вам его параметры:'
    # welcome_message += '\nПо вашей картинке я могу определить:'
    welcome_message += '\n    * Расстояние до самолета'
    welcome_message += '\n    * Угол места'
    welcome_message += '\n    * Азимут'
    welcome_message += '\n    * Тангаж'
    welcome_message += '\n    * Крен'
    welcome_message += '\n    * Рысканье'
    welcome_message += '\n\nСервис работает в тестовом режиме! Подавайте на вход только 1 изображение'

    await msg.reply(welcome_message)

def main_process():
    photo = images_dir + image_file
    try:
        params = get_param([photo])
        print('\tSUCCESS')
    except:
        print('\tERROR')
        params = []
    os.remove(photo)
    return params

# Загружаем фото
@dp.message_handler(content_types=['photo', 'document'])
async def handle_docs_photo(msg):
    try:
        if 'photo' in msg:
            await msg['photo'][-1].download(images_dir + image_file)
        else:
            # await msg['document'][-1].download(images_dir + 'image.jpg')
            file_id = msg.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, images_dir + image_file)
    except:
        await bot.send_message(msg.from_user.id, 'ALARM! Изображение не загружено')
        return
    try:
        params = main_process()
    except:
        await bot.send_message(msg.from_user.id, 'ALARM! Ошибка обработки')
        return

    detect_path = './yolov5/runs/detect/'
    detect = os.listdir(detect_path)
    detect_help = []
    for i in detect:
        try:
            detect_help.append(int(i[3:]))
        except:
            pass
    detect_help.sort()
    detect = 'exp' + str(detect_help[-1])
    print(f'DETECT IN {detect}')
    detect_path = detect_path + detect + '/'
    await bot.send_photo(msg.from_user.id, types.input_file.InputFile(detect_path + image_file))

    for item in params:
        resp = ''
        for key, value in item.items():
            if key == 'Файл':
                continue
            if type(value) is float:
                value = f'{value:.4f}'
            resp += f'{key}:\t{value}\n'
            if key == 'Азимут':
                resp += '\n'
        await bot.send_message(msg.from_user.id, resp)

@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        await bot.send_message(msg.from_user.id, '/help')
    except:
        await bot.send_message(msg.from_user.id, 'Возможно, самолёт не найден...')


if __name__ == '__main__':
    executor.start_polling(dp)
