# AeroFlex в Челябинске

Хакатон по ИИ в Челябинске - 1-е место

_19-21 ноября 2021_

Команда __AeroFlex__ (Москва):
* Илья Никитюк
* Илья Волков
* Константин Науменко
* Максим Алексюк


## Содержание репозитория

* `bot.py` - файл с реализацией телеграмм-бота
* `aircraft.py`
* `camera.py`
* `get_param.py`
* `get_angle_aircraft.py`
* `predict_angle.py`
* `train_baseline_ver_3.ipynb` - обучение нейросети для нахождения углов

## Установка

Создадим новое окружение и установим все необходимые пакеты:

```console
foo@bar$ python3 -m venv flex
foo@bar$ source flex/bin/activate
(flex) foo@bar$ pip install -r requirements.txt
```

## Запуск

Запуск телеграмм-бота
```console
(flex) foo@bar$ python bot.py
```

Запуск работы алгоритма
```console
(flex) foo@bar$ python get_param.py <image.jpg>
```

## Демонстрация
Ссылка на демонстрацию работы телеграмм-бота
> https://youtu.be/hVb8tYyJ_nE
