import json

import discord


class MyClient(discord.Client):

    __slots__ = [ 'logChannel' ]

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("The bot is ready!")
        await bot.change_presence(game=discord.Game(name="Making a    bot"))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == bot.user:
            return

        if message.content[:1] == "/":
            command = message.content[1:]
            if command == "setupChannel":
                self.logChannel = message.channel
                await bot.send_message(self.logChannel, "The Channel {} was setup!".format(self.logChannel))
            elif command == "print":
                await bot.send_message(self.logChannel, "Erfolgreich")
            else:
                await bot.send_message(message.channel, "pong1!")

        if message.content == "Hello":
            await bot.say("World")

    async def on_member_join(self, member):
        await bot.send_message(self.logChannel, "{} joined the Server!".format(member))

    async def on_member_remove(self, member):
        await bot.send_message(self.logChannel, "{} left the Server!".format(member))

    async def on_voice_state_update(self, before, after):
        if before.voice_channel and not after.voice_channel :
            await bot.send_message(self.logChannel, "{}({}) disconnected from {}".format(before, before.name, before.voice_channel))

        elif not before.voice_channel and after.voice_channel:
            await bot.send_message(self.logChannel, "{}({}) joined {}".format(after, after.name, after.voice_channel))

        elif before.voice_channel and after.voice_channel and before.voice_channel != after.voice_channel:
            await bot.send_message(self.logChannel, "{} ({}) moved from {} to {}".format(after, after.name, before.voice_channel, after.voice_channel))

bot = MyClient()
with open('./auth.json') as f:
    fileContent = f.read()
    bot.run(json.loads(fileContent)['token'])