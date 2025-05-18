import discord
import os
import openai

# Neue OpenAI Client API (ab Version 1.x)
from openai import OpenAI

# Discord Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ENV-Variablen laden
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
channel_id_raw = os.getenv("CHANNEL_ID")

# Debug-Ausgabe
print("🔍 CHANNEL_ID (roh):", channel_id_raw)

# Fehlerprüfungen
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN fehlt!")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY fehlt!")

if not channel_id_raw:
    raise ValueError("❌ CHANNEL_ID fehlt!")

CHANNEL_ID = int(channel_id_raw)

# OpenAI-Client initialisieren (ab v1.0)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

# Begrüßung bei Start
@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("👋 Hey! Ich bin **Kalle**, dein KI-Bot rund ums **Trading**. Stell mir gerne deine Frage!")

# Nachrichten behandeln
@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    user_input = message.content.strip()

    # Ignoriere Bot-Kommandos wie ! oder /
    if user_input.startswith("!") or user_input.startswith("/"):
        return

    # Trading-Keyword-Check
    TRADING_KEYWORDS = [
        "trading", "aktien", "krypto", "chart", "forex", "börsen", "analyse",
        "bollinger", "bb", "moo", "macd", "moving average", "gleitender durchschnitt",
        "order", "trend", "support", "resistance", "short", "long", "zeiteinheit",
        "indikator", "candlestick", "breakout", "pullback", "signal"
    ]

    if not any(keyword in user_input.lower() for keyword in TRADING_KEYWORDS):
        return  # Keine Antwort, wenn kein Trading-Bezug

    print(f"💬 Frage erkannt: {user_input}")

    try:
        # Neue GPT-Anfrage mit OpenAI 1.x
        chat_completion = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist Kalle, ein professioneller, freundlicher Trading-Coach. "
                        "Erkläre Trading-Themen von Grundlagen bis Fortgeschrittenem: "
                        "MACD, Bollinger Bands, gleitende Durchschnitte, Orderarten usw. "
                        "Sei klar, sachlich und verständlich – mit Beispielen, wenn sinnvoll."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()
        await message.channel.send(f"📈 {reply}")

    except Exception as e:
        print("❌ Fehler bei OpenAI:", e)
        await message.channel.send("⚠️ Es gab ein Problem mit meiner Antwort. Versuch es später nochmal.")
        
# Bot starten
client.run(DISCORD_TOKEN)
