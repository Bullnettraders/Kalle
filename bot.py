import discord
import os
from openai import OpenAI

# Discord-Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Damit neue Mitglieder getrackt werden
client = discord.Client(intents=intents)

# Umgebungsvariablen laden
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
channel_id_raw = os.getenv("CHANNEL_ID")

print("🔍 CHANNEL_ID (roh):", channel_id_raw)

# Überprüfen der Variablen
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN fehlt!")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY fehlt!")

if not channel_id_raw:
    raise ValueError("❌ CHANNEL_ID fehlt!")

CHANNEL_ID = int(channel_id_raw)
client_openai = OpenAI(api_key=OPENAI_API_KEY)

# Begrüßte Nutzer (einfach im Speicher, reset bei Neustart)
user_greeted = set()

# Begrüßung bei Bot-Start
@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("👋 Hey! Ich bin **Kalle**, dein KI-Bot rund ums **Trading**. Von den Grundlagen bis zu Strategien – stell mir deine Frage!")

# Nachrichtenverarbeitung
@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    user_input = message.content.strip()

    # User zum ersten Mal? Begrüßung
    if message.author.id not in user_greeted:
        user_greeted.add(message.author.id)
        await message.channel.send(f"👋 Hey {message.author.mention}! Ich bin **Kalle**, dein KI-Bot rund ums **Trading**. Stell mir gerne deine Frage!")

    # Bot-Kommandos ignorieren
    if user_input.startswith("!") or user_input.startswith("/"):
        return

    # Trading-Keywords
    TRADING_KEYWORDS = [
        "trading", "aktien", "krypto", "chart", "forex", "börsen", "analyse",
        "bollinger", "bb", "moo", "macd", "moving average", "gleitender durchschnitt",
        "order", "orderart", "tp", "sl", "stop loss", "take profit", "trailing stop",
        "trades", "backtest", "strategie", "trend", "pullback", "breakout", "support",
        "resistance", "einstieg", "ausstieg", "psychologie", "risiko", "money management",
        "chartmuster", "scalping", "daytrading", "swing", "indikator", "rsi", "ema", "sma",
        "volumen", "candlestick", "doppeltop", "flagge", "dreieck", "tradingplan"
    ]

    if not any(keyword in user_input.lower() for keyword in TRADING_KEYWORDS):
        return

    print(f"💬 Frage erkannt: {user_input}")

    try:
        # GPT-Antwort holen
        chat_completion = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist Kalle, ein erfahrener Trading-Coach. "
                        "Beantworte Fragen rund ums Trading fundiert, verständlich und mit Beispielen. "
                        "Erkläre Themen wie: TP, SL, Trailing Stop, Orderarten, Chartmuster, Strategien "
                        "(Scalping, Breakout, Swing), Risiko- & Money Management, Trading-Psychologie, Indikatoren (MACD, RSI, BB, MA), "
                        "Tradingpläne und mehr. Sprich einfach, sachlich und hilfreich für Anfänger & Fortgeschrittene."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()

        if not reply or reply.strip() == "":
            await message.channel.send("❓ Dazu habe ich leider keine klare Antwort. Formuliere deine Frage gerne etwas anders oder genauer.")
        else:
            formatted_reply = f"""📊 **Kalles Antwort**

{reply}

---
💬 *Du hast weitere Fragen? Frag mich einfach nochmal!*"""
            await message.channel.send(formatted_reply)

    except Exception as e:
        print("❌ Fehler bei OpenAI:", e)
        await message.channel.send("❓ Dazu habe ich leider keine klare Antwort. Formuliere deine Frage gerne etwas anders oder genauer.")

# Bot starten
client.run(DISCORD_TOKEN)
