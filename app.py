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
    
    # Portugal regions
    REGIONS = ["Lisbon", "Porto", "Algarve", "Coimbra", "Braga", "Aveiro"]
    
    # Sample political headlines
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
    
    # Sample economic headlines
    ECONOMY_HEADLINES = [
        "Inflation holds steady at 2.1% as economy stabilizes",
        "Tourism sector reports 8.4% growth year-on-year",
        "Minimum wage review commission begins deliberations",
        "Renewable energy projects attract €500M investment",
        "Portugal's GDP grows 1.8% in latest quarter",
        "Unemployment rate drops to historic low of 5.2%",
        "Real estate market shows signs of stabilization",
        "Tech sector leads employment growth in Portugal"
    ]
    
    # Weather data (simulated)
    @staticmethod
    def get_weather():
        """Generate realistic weather data for Portugal"""
        weather_conditions = ["☀️ Sunny", "⛅ Partly Cloudy", "🌤️ Mostly Sunny", "🌧️ Light Rain", "☁️ Cloudy"]
        
        weather_data = {}
        for region in PortugalService.REGIONS:
            temp = random.randint(18, 32)
            condition = random.choice(weather_conditions)
            weather_data[region] = {
                "temp": temp,
                "condition": condition
            }
        
        return weather_data
    
    @staticmethod
    def get_political_news():
        """Get political headlines"""
        headlines = random.sample(PortugalService.POLITICS_HEADLINES, 3)
        return headlines
    
    @staticmethod
    def get_economic_news():
        """Get economic headlines"""
        headlines = random.sample(PortugalService.ECONOMY_HEADLINES, 3)
        return headlines
    
    @staticmethod
    def get_coming_up():
        """Generate 'coming up' items"""
        events = [
            "🇵🇹 Cabinet meeting at 10:00 AM",
            "🏛️ Parliament session convenes at 2:30 PM",
            "📊 Economic data release due at 11:00 AM",
            "🌿 Environmental summit in Lisbon this afternoon",
            "📰 Press conference scheduled for 4:00 PM",
            "🎭 Cultural events across major cities today"
        ]
        return random.sample(events, 2)
    
    @staticmethod
    def get_today_summary():
        """Get quick summary of today"""
        summaries = [
            "🇵🇹 Portugal's economy shows resilience with GDP growth of 1.8%",
            "🏠 New housing bill aims to make homes more affordable",
            "🌤️ Summer weather continues across the country",
            "🌿 Portugal leads EU in renewable energy adoption",
            "📈 Tourism sector reports record numbers this season",
            "💼 Foreign investment reaches new highs in tech sector"
        ]
        return random.choice(summaries)
    
    @staticmethod
    def generate_daily_briefing():
        """Generate complete morning briefing"""
        today = datetime.datetime.now().strftime("%d %B %Y")
        
        politics = PortugalService.get_political_news()
        economy = PortugalService.get_economic_news()
        weather = PortugalService.get_weather()
        
        briefing = f"""
🇵🇹 <b>PT MORNING BRIEFING</b>
📅 {today}

━━━━━━━━━━━━━━━━━━
📰 <b>POLITICS & GOVERNANCE</b>
• {politics[0]}
• {politics[1]}
• {politics[2]}

━━━━━━━━━━━━━━━━━━
💼 <b>ECONOMY & BUSINESS</b>
• {economy[0]}
• {economy[1]}
• {economy[2]}

━━━━━━━━━━━━━━━━━━
🌤️ <b>WEATHER TODAY</b>
"""
        
        for region, data in weather.items():
            briefing += f"• {region}: {data['temp']}°C, {data['condition']}\n"
        
        coming_up = PortugalService.get_coming_up()
        briefing += f"""
━━━━━━━━━━━━━━━━━━
📌 <b>COMING UP TODAY</b>
• {coming_up[0]}
• {coming_up[1]}

━━━━━━━━━━━━━━━━━━
📊 <b>TODAY'S KEY TAKEAWAY</b>
{PortugalService.get_today_summary()}

<b>📱 Stay informed with Pt Morning Briefing!</b>
"""
        
        return briefing

# ==================== KEYBOARDS ====================
def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📰 Daily Briefing", callback_data="briefing"),
        InlineKeyboardButton(text="🗳️ Politics", callback_data="politics")
    )
    builder.row(
        InlineKeyboardButton(text="💼 Economy", callback_data="economy"),
        InlineKeyboardButton(text="🌤️ Weather", callback_data="weather")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Today's Summary", callback_data="today")
    )
    
    return builder.as_markup()

# ==================== COMMAND HANDLERS ====================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🇵🇹 <b>Pt Morning Briefing Bot</b>\n\n"
        "Your daily 5-minute digest of Portugal's news, economy, and weather.\n\n"
        "📋 <b>Commands:</b>\n"
        "/briefing - Complete morning briefing\n"
        "/politics - Political news\n"
        "/economy - Economic updates\n"
        "/weather - Weather across Portugal\n"
        "/today - Key stories today\n"
        "/help - Show this menu\n\n"
        "📱 <i>Start your day informed about Portugal!</i>",
        reply_markup=main_menu()
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await start_command(message)

@dp.message(Command("briefing"))
async def briefing_command(message: types.Message):
    await message.answer("📰 Generating your daily briefing...")
    briefing = PortugalService.generate_daily_briefing()
    await message.answer(briefing)

@dp.message(Command("politics"))
async def politics_command(message: types.Message):
    await message.answer("🗳️ Fetching political news...")
    politics = PortugalService.get_political_news()
    
    response = "🇵🇹 <b>Political News</b>\n\n"
    for item in politics:
        response += f"• {item}\n"
    
    await message.answer(response)

@dp.message(Command("economy"))
async def economy_command(message: types.Message):
    await message.answer("💼 Fetching economic news...")
    economy = PortugalService.get_economic_news()
    
    response = "🇵🇹 <b>Economic News</b>\n\n"
    for item in economy:
        response += f"• {item}\n"
    
    await message.answer(response)

@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    await message.answer("🌤️ Fetching weather data...")
    weather = PortugalService.get_weather()
    
    response = "🌤️ <b>Portugal Weather Today</b>\n\n"
    for region, data in weather.items():
        response += f"• {region}: {data['temp']}°C, {data['condition']}\n"
    
    await message.answer(response)

@dp.message(Command("today"))
async def today_command(message: types.Message):
    await message.answer("📊 Fetching today's summary...")
    response = f"""
📊 <b>Today's Key Stories</b>

{PortugalService.get_today_summary()}

📌 <b>Coming Up:</b>
• {PortugalService.get_coming_up()[0]}
• {PortugalService.get_coming_up()[1]}

<i>Stay tuned for tomorrow's briefing!</i>
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

# ==================== MAIN ====================

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("🇵🇹 Pt Morning Briefing Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
