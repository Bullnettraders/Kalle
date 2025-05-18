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

# Debug-Ausgabe zur Diagnose
print("🔍 DISCORD_TOKEN gesetzt:", bool(DISCORD_TOKEN))
print("🔍 OPENAI_API_KEY gesetzt:", bool(OPENAI_API_KEY))
print("🔍 CHANNEL_ID (roh):", channel_id_raw)

# Fehlerprüfung
if not DISCORD_TOKEN:
    raise ValueError("❌ Umgebungsvariable DISCORD_TOKEN fehlt!")

if not OPENAI_API_KEY:
    raise ValueError("❌ Umgebungsvariable OPENAI_API_KEY fehlt!")

if not channel_id_raw:
    raise ValueError("❌ Umgebungsvariable CHANNEL_ID fehlt!")

try:
    CHANNEL_ID = int(channel_id_raw)
except ValueError:
    raise ValueError("❌ CHANNEL_ID muss eine gültige Zahl sein!")

# OpenAI konfigurieren
openai.api_key = OPENAI_API_KEY

# Bot bereit
@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")

# Nachrichtenverarbeitung
@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    user_input = message.content
    print(f"💬 Nachricht empfangen: {user_input}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content.strip()
        await message.channel.send(reply)
    except Exception as e:
        print("❌ Fehler bei OpenAI:", e)
        await message.channel.send("⚠️ Fehler bei der Antwort. Bitte versuch es später erneut.")

# Bot starten
client.run(DISCORD_TOKEN)
