import requests
from bs4 import BeautifulSoup
from datetime import date

from aiogram import Dispatcher, types, executor, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "5851969331:AAEAtYFo47kZLH5OFKw5_RKrRE_Buj8hjq8"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
date = date.today()

MSG = f"Курс валют на {date}:"


button_1 = KeyboardButton(text="/Currency")

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_1)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    await bot.send_message(message.chat.id,
                           f'Привет, {user_name}! Я - бот ExchangeRate, я помогу тебе узнать курс валюты. '
                           f'Чтобы узнать текущий курс, нажмите кнопку',
                           reply_markup=keyboard)


def main():
    dollar_rub = 'https://www.banki.ru/products/currency/cb/'
    btc_dollar = 'https://myfin.by/crypto-rates/bitcoin-usd'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15'}

    full_page = requests.get(dollar_rub, headers=headers)
    full_page1 = requests.get(btc_dollar, headers=headers)

    soup1 = BeautifulSoup(full_page.content, 'html.parser')
    soup2 = BeautifulSoup(full_page1.content, 'html.parser')

    convert_usd = soup1.findAll("tr", {"data-test": "currency-table-row", "data-currency-code": "USD",
                                       "data-currency-name": "Доллар США"})
    arr_usd = convert_usd[0].text.split()
    usd = round(float(arr_usd[4]), 2)

    usd_change = str(arr_usd[5])[0:5].replace(",", ".")
    usd_indicator = float(str(arr_usd[5])[1:5].replace(",", "."))

    convert_euro = soup1.findAll("tr", {"data-test": "currency-table-row", "data-currency-code": "EUR",
                                        "data-currency-name": "Евро"})
    arr_euro = convert_euro[0].text.split()
    euro = round(float(arr_euro[3]), 2)

    euro_change = str(arr_euro[4])[0:5].replace(",", ".")
    euro_indicator = float(str(arr_euro[4])[1:5].replace(",", "."))

    convert_btc = soup2.findAll("div", {"class": "birzha_info_head_rates"})
    arr_btc_change = soup2.findAll("div", {"class": "col-md-6 col-xs-12"})

    btc_change = str(arr_btc_change)[290:295]
    btc_indicator = float(str(arr_btc_change)[292:297])

    arr_btc = convert_btc[0].text.split()
    btc = float(arr_btc[0][:-1])

    alert = ""

    if btc_indicator > 10:
        alert += "Резкое изменение btc❗️"

    if usd_indicator > 5:
        alert += "Резкое изменение usd❗️"

    if euro_indicator > 5:
        alert += "Резкое изменение euro❗️"

    currency_tup = (MSG, '\n' + alert, '\n'"💰Курс доллара: " + str(usd) + "₽" + "   (" + str(usd_change) + "%)",
                    '\n' "💰Курс евро: " + str(euro) + "₽" + "   (" + str(euro_change) + "%)", '\n' "💰Курс биткоина: ",
                    str(btc) + "$" + "   (" + str(btc_change) + "%)")
    currency = ''.join(currency_tup)

    return str(currency)


@dp.message_handler(commands=['Currency'])
async def currency_command(message: types.Message):
    await bot.send_message(message.chat.id, main())
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=['text'])
async def handle_text(message):
    if message.text:
        await bot.send_message(message.chat.id, "Извините, я вас не понимаю")
        await bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp),
    main()
