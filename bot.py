import discord
import os
import openai

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ENV Variablen
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    user_message = message.content

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        await message.channel.send(response.choices[0].message.content)
    except Exception as e:
        await message.channel.send("⚠️ Fehler bei der Antwort.")
        print(e)

client.run(DISCORD_TOKEN)
