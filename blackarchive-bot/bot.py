```python
import logging
import os
from flask import Flask, request, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    Dispatcher
)

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = os.getenv(BOT_TOKEN)  # Токен из переменной окружения
ADMIN_ID = 1279885111
WEBHOOK_URL = os.getenv(WEBHOOK_URL, httpsyour-bot.vercel.appwebhook)  # Замени после деплоя

# База данных (в памяти)
products = {
    1 {name 💎 В-баксы Fortnite, price 100, desc 1000 V-bucks (ключ активации)},
    2 {name 🔑 Minecraft Premium, price 500, desc Лицензионный ключ для Java Edition},
    3 {name 🎮 Steam Wallet, price 200, desc Код пополнения на 5$}
}

users_carts = {}
orders = {}

# Инициализация Flask
app = Flask(__name__)

# Инициализация Telegram Application
bot_app = Application.builder().token(TOKEN).build()

# Обработчики команд и callback'ов
async def start(update Update, context ContextTypes.DEFAULT_TYPE)
    Упрощённое приветствие с кнопкой перехода в Mini App
    user = update.effective_user
    text = f🎮 Привет, {user.first_name}!nДобро пожаловать в наш магазин.nНажми кнопку ниже, чтобы открыть каталог товаров 👇

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(🛒 Перейти в магазин, web_app=WebAppInfo(url=httpstelegram-miniapp-ecru.vercel.app))]
    ])

    if update.message
        await update.message.reply_text(text, reply_markup=keyboard)
    elif update.callback_query
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def my_orders(update Update, context ContextTypes.DEFAULT_TYPE)
    Показывает заказы пользователя
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    user_orders = {kv for k,v in orders.items() if v['user_id'] == user_id}
    
    if not user_orders
        await query.edit_message_text(
            📦 У вас пока нет заказов.,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(🛒 В каталог, callback_data=catalog)],
                [InlineKeyboardButton(🔙 В меню, callback_data=back)]
            ])
        )
        return
    
    orders_text = 📦 Ваши заказыnn
    for order_id, order in user_orders.items()
        orders_text += (
            f🔹 Заказ #{order_id}n
            f   Статус {order['status']}n
            f   Сумма {sum(products[pid]['price']qty for pid, qty in order['items'].items())}₽nn
        )
    
    await query.edit_message_text(
        orders_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(🔙 Назад, callback_data=back)]
        ])
    )

async def admin_panel(update Update, context ContextTypes.DEFAULT_TYPE)
    Админ-панель
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID
        await query.edit_message_text(⛔ Доступ запрещен!)
        return
    
    await query.edit_message_text(
        ⚙ Админ-панель,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(📊 Статистика, callback_data=admin_stats)],
            [InlineKeyboardButton(📦 Все заказы, callback_data=admin_orders)],
            [InlineKeyboardButton(🔙 Назад, callback_data=back)]
        ])
    )

async def admin_stats(update Update, context ContextTypes.DEFAULT_TYPE)
    Статистика для админа
    query = update.callback_query
    await query.answer()
    
    total_orders = len(orders)
    total_revenue = sum(
        sum(products[pid]['price']qty for pid, qty in order['items'].items())
        for order in orders.values()
    )
    
    await query.edit_message_text(
        f📊 Статистикаnn
        f• Всего заказов {total_orders}n
        f• Общая выручка {total_revenue}₽n
        f• Товаров в каталоге {len(products)},
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(🔙 Назад, callback_data=admin)]
        ])
    )

async def admin_orders(update Update, context ContextTypes.DEFAULT_TYPE)
    Список всех заказов для админа
    query = update.callback_query
    await query.answer()
    
    if not orders
        await query.edit_message_text(
            📦 Нет активных заказов.,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(🔙 Назад, callback_data=admin)]
            ])
        )
        return
    
    orders_text = 📦 Все заказыnn
    for order_id, order in orders.items()
        user = await context.bot.get_chat(order['user_id'])
        orders_text += (
            f🔹 #{order_id} - {user.first_name}n
            f   Статус {order['status']}n
            f   Сумма {sum(products[pid]['price']qty for pid, qty in order['items'].items())}₽nn
        )
    
    await query.edit_message_text(
        orders_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(🔙 Назад, callback_data=admin)]
        ])
    )

async def back_handler(update Update, context ContextTypes.DEFAULT_TYPE)
    Обработчик кнопки 'Назад'
    await start(update, context)

# Регистрация обработчиков
bot_app.add_handler(CommandHandler(start, start))
bot_app.add_handler(CallbackQueryHandler(my_orders, pattern=^my_orders$))
bot_app.add_handler(CallbackQueryHandler(admin_panel, pattern=^admin$))
bot_app.add_handler(CallbackQueryHandler(admin_stats, pattern=^admin_stats$))
bot_app.add_handler(CallbackQueryHandler(admin_orders, pattern=^admin_orders$))
bot_app.add_handler(CallbackQueryHandler(back_handler, pattern=^back$))

# Webhook endpoint
@app.route('webhook', methods=['POST'])
async def webhook()
    update = Update.de_json(request.get_json(), bot_app.bot)
    if update
        await bot_app.process_update(update)
    return Response(status=200)

@app.route('')
def health_check()
    return Bot is running!

# Инициализация бота
async def init_bot()
    await bot_app.initialize()
    await bot_app.bot.set_webhook(WEBHOOK_URL)

# Запуск для локального тестирования
if __name__ == __main__
    import asyncio
    asyncio.run(init_bot())
    app.run(debug=True)
```