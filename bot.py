import discord
import openai
import os

# Discord-Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ENV-Variablen laden
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
channel_id_raw = os.getenv("CHANNEL_ID")

# Debug-Ausgaben
print("🔍 CHANNEL_ID (roh):", channel_id_raw)

if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN fehlt!")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY fehlt!")

if not channel_id_raw:
    raise ValueError("❌ CHANNEL_ID fehlt!")

CHANNEL_ID = int(channel_id_raw)
openai.api_key = OPENAI_API_KEY

# Begrüßungsnachricht beim Start
@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("👋 Hey! Ich bin **Kalle**, dein KI-Bot rund ums **Trading**. Stell mir gerne deine Frage!")

# Nachricht beantworten
@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    user_input = message.content.strip()

    # Befehle wie ! oder / ignorieren
    if user_input.startswith("!") or user_input.startswith("/"):
        return

    # Schlüsselwörter für Trading-Erkennung
    TRADING_KEYWORDS = [
        "trading", "aktien", "krypto", "chart", "forex", "börsen", "analyse", "bollinger", "bb", "moo",
        "macd", "moving average", "gleitender durchschnitt", "order", "trend", "support", "resistance",
        "short", "long", "zeiteinheit", "indikator", "candlestick", "breakout", "pullback", "signal"
    ]

    # Nur antworten, wenn Trading-Bezug erkannt
    if not any(keyword in user_input.lower() for keyword in TRADING_KEYWORDS):
        return

    print(f"💬 Frage erkannt: {user_input}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist Kalle, ein freundlicher, professioneller Trading-Coach. "
                        "Du erklärst Trading-Konzepte einfach und verständlich, von Anfängerwissen bis zu fortgeschrittenen Techniken. "
                        "Gib präzise Antworten zu Themen wie Orderarten, Indikatoren (MACD, BB, MA), Risikomanagement oder Marktverhalten. "
                        "Sprich klar, sachlich und mit Beispielen – ohne Fachjargon."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        await message.channel.send(f"📈 {reply}")

    except Exception as e:
        print("❌ OpenAI Fehler:", e)
        await message.channel.send("⚠️ Es gab ein Problem mit meiner Antwort. Versuch es später nochmal.")

# Bot starten
client.run(DISCORD_TOKEN)
