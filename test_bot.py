import pytest
import asyncio
from unittest.mock import AsyncMock, Mock

import aiogram

import bot


@pytest.mark.asyncio
async def test_start_command():
    message = Mock()
    message.from_user.id = 1
    message.from_user.full_name = 'test'
    message.chat.id = 1
    message.text = 'test'
    aiogram.Bot.send_message = AsyncMock()
    button_1 = aiogram.types.KeyboardButton(text="/Currency")
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    await bot.start_handler(message)
    bot.bot.send_message.assert_called_with(message.chat.id,
                                            f'Привет, {message.from_user.full_name}! Я - бот ExchangeRate, я помогу тебе узнать курс валюты. '
                                            f'Чтобы узнать текущий курс, нажмите кнопку',
                                            reply_markup=keyboard)


@pytest.mark.asyncio
async def test_currency_command():
    message = Mock()
    message.from_user.id = 1
    message.from_user.full_name = 'test'
    message.chat.id = 1
    message.text = 'test'
    aiogram.Bot.send_message = AsyncMock()
    aiogram.Bot.delete_message = AsyncMock()
    button_1 = aiogram.types.KeyboardButton(text="/Currency")
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    bot.main = Mock()
    bot.main.return_value = 'test'
    await bot.currency_command(message)
    bot.bot.send_message.assert_called_with(message.chat.id, bot.main())
    bot.bot.delete_message.assert_called_with(message.chat.id, message.message_id)


@pytest.mark.asyncio
async def test_handle_text():
    message = Mock()
    message.from_user.id = 1
    message.from_user.full_name = 'test'
    message.chat.id = 1
    message.text = 'test'
    aiogram.Bot.send_message = AsyncMock()
    button_1 = aiogram.types.KeyboardButton(text="/Currency")
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    await bot.handle_text(message)
    bot.bot.send_message.assert_called_with(message.chat.id, "Извините, я вас не понимаю")
    bot.bot.delete_message.assert_called_with(message.chat.id, message.message_id)
