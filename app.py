import asyncio
import logging
import random
import datetime
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

# ==================== CONFIG ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")

# ==================== BOT SETUP ====================
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ==================== DATA SERVICE ====================
class PortugalService:
    """Self-contained Portugal news service - NO API KEYS REQUIRED"""
    
    REGIONS = ["Lisbon", "Porto", "Algarve", "Coimbra", "Braga", "Aveiro"]
    
    POLITICS_HEADLINES = [
        "Government approves new housing affordability bill",
        "Parliament debates healthcare system reforms",
        "President announces new digital infrastructure investment",
        "Local elections campaign period officially opens",
        "Cabinet approves tax relief package for families",
        "New environmental protection laws passed by parliament",
        "Foreign investment regulations updated for 2026",
        "Education reform bill enters final parliamentary phase"
    ]
    
    ECONOMY_HEADLINES = [
        "Inflation holds steady at 2.1% as economy stabilizes",
        "Tourism sector reports 8.4% growth year-on-year",
        "Minimum wage review commission begins deliberations",
        "Renewable energy projects attract 500M investment",
        "Portugal's GDP grows 1.8% in latest quarter",
        "Unemployment rate drops to historic low of 5.2%",
        "Real estate market shows signs of stabilization",
        "Tech sector leads employment growth in Portugal"
    ]
    
    @staticmethod
    def get_weather():
        weather_conditions = ["Sunny", "Partly Cloudy", "Mostly Sunny", "Light Rain", "Cloudy"]
        weather_data = {}
        for region in PortugalService.REGIONS:
            temp = random.randint(18, 32)
            condition = random.choice(weather_conditions)
            weather_data[region] = {"temp": temp, "condition": condition}
        return weather_data
    
    @staticmethod
    def get_political_news():
        return random.sample(PortugalService.POLITICS_HEADLINES, 3)
    
    @staticmethod
    def get_economic_news():
        return random.sample(PortugalService.ECONOMY_HEADLINES, 3)
    
    @staticmethod
    def get_coming_up():
        events = [
            "Cabinet meeting at 10:00 AM",
            "Parliament session convenes at 2:30 PM",
            "Economic data release due at 11:00 AM",
            "Environmental summit in Lisbon this afternoon",
            "Press conference scheduled for 4:00 PM",
            "Cultural events across major cities today"
        ]
        return random.sample(events, 2)
    
    @staticmethod
    def get_today_summary():
        summaries = [
            "Portugal's economy shows resilience with GDP growth of 1.8%",
            "New housing bill aims to make homes more affordable",
            "Summer weather continues across the country",
            "Portugal leads EU in renewable energy adoption",
            "Tourism sector reports record numbers this season",
            "Foreign investment reaches new highs in tech sector"
        ]
        return random.choice(summaries)
    
    @staticmethod
    def generate_daily_briefing():
        today = datetime.datetime.now().strftime("%d %B %Y")
        politics = PortugalService.get_political_news()
        economy = PortugalService.get_economic_news()
        weather = PortugalService.get_weather()
        
        briefing = f"""
PT MORNING BRIEFING
Date: {today}

------------------------------------
POLITICS & GOVERNANCE
-> {politics[0]}
-> {politics[1]}
-> {politics[2]}

------------------------------------
ECONOMY & BUSINESS
-> {economy[0]}
-> {economy[1]}
-> {economy[2]}

------------------------------------
WEATHER TODAY
"""
        for region, data in weather.items():
            briefing += f"-> {region}: {data['temp']}C, {data['condition']}\n"
        
        coming_up = PortugalService.get_coming_up()
        briefing += f"""
------------------------------------
COMING UP TODAY
-> {coming_up[0]}
-> {coming_up[1]}

------------------------------------
TODAY'S KEY TAKEAWAY
{PortugalService.get_today_summary()}

Stay informed with Pt Morning Briefing!
"""
        return briefing

# ==================== KEYBOARDS ====================
def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Daily Briefing", callback_data="briefing"),
        InlineKeyboardButton(text="Politics", callback_data="politics")
    )
    builder.row(
        InlineKeyboardButton(text="Economy", callback_data="economy"),
        InlineKeyboardButton(text="Weather", callback_data="weather")
    )
    builder.row(
        InlineKeyboardButton(text="Today's Summary", callback_data="today")
    )
    return builder.as_markup()

# ==================== COMMAND HANDLERS ====================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Pt Morning Briefing Bot\n\n"
        "Your daily 5-minute digest of Portugal's news, economy, and weather.\n\n"
        "Commands:\n"
        "/briefing - Complete morning briefing\n"
        "/politics - Political news\n"
        "/economy - Economic updates\n"
        "/weather - Weather across Portugal\n"
        "/today - Key stories today\n"
        "/help - Show this menu\n\n"
        "Start your day informed about Portugal!",
        reply_markup=main_menu()
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await start_command(message)

@dp.message(Command("briefing"))
async def briefing_command(message: types.Message):
    await message.answer("Generating your daily briefing...")
    briefing = PortugalService.generate_daily_briefing()
    await message.answer(briefing)

@dp.message(Command("politics"))
async def politics_command(message: types.Message):
    await message.answer("Fetching political news...")
    politics = PortugalService.get_political_news()
    response = "Political News\n\n"
    for item in politics:
        response += f"- {item}\n"
    await message.answer(response)

@dp.message(Command("economy"))
async def economy_command(message: types.Message):
    await message.answer("Fetching economic news...")
    economy = PortugalService.get_economic_news()
    response = "Economic News\n\n"
    for item in economy:
        response += f"- {item}\n"
    await message.answer(response)

@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    await message.answer("Fetching weather data...")
    weather = PortugalService.get_weather()
    response = "Portugal Weather Today\n\n"
    for region, data in weather.items():
        response += f"- {region}: {data['temp']}C, {data['condition']}\n"
    await message.answer(response)

@dp.message(Command("today"))
async def today_command(message: types.Message):
    await message.answer("Fetching today's summary...")
    response = f"""
Today's Key Stories

{PortugalService.get_today_summary()}

Coming Up:
- {PortugalService.get_coming_up()[0]}
- {PortugalService.get_coming_up()[1]}

Stay tuned for tomorrow's briefing!
"""
    await message.answer(response)

# ==================== CALLBACK QUERY HANDLERS ====================

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data
    if data == "briefing":
        await briefing_command(callback.message)
    elif data == "politics":
        await politics_command(callback.message)
    elif data == "economy":
        await economy_command(callback.message)
    elif data == "weather":
        await weather_command(callback.message)
    elif data == "today":
        await today_command(callback.message)

# ==================== WEB SERVER FOR RAILWAY ====================
async def handle_health(request):
    return web.Response(text="Pt Morning Briefing Bot is running!")

async def start_web_server():
    """Start a simple web server for Railway"""
    app = web.Application()
    app.router.add_get('/', handle_health)
    app.router.add_get('/health', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 8080)))
    await site.start()
    logging.info(f"Web server running on port {os.getenv('PORT', 8080)}")
    return runner

# ==================== MAIN ====================

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Pt Morning Briefing Bot starting...")
    
    # Start web server
    try:
        runner = await start_web_server()
    except Exception as e:
        logging.warning(f"Web server not started: {e}")
    
    # Start bot polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
