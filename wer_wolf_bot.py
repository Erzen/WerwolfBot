

import discord

TOKEN = 'deinen token hier reinkopieren'

client = discord.Client()
@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a    bot"))
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "World")
client.run(TOKEN)