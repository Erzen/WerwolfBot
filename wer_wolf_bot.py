import json

import discord


class MyClient(discord.Client):

    __slots__ = [ 'logChannel' ]

    # Bot Log-In
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("The bot is ready!")
        await bot.change_presence(game=discord.Game(name="Making a    bot"))

    # New Message
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == bot.user:
            return

        if message.content[:1] == "/":
            command = message.content[1:]
            if command == "setupChannel":
                self.logChannel = message.channel
                await bot.send_message(self.logChannel, "The Channel {} was setup!".format(self.logChannel.mention))
            elif command == "testChannel":
                if self.logChannel:
                    await bot.send_message(self.logChannel, "Channel erfolgreich getestet!")
                else:
                    await bot.send_message(message.channel, "Channel test ist Fehlgeschlagen!")
            else:
                await bot.send_message(message.author, "private Bestätigung")

    # User joined Server
    async def on_member_join(self, member):
        if self.logChannel:
            await bot.send_message(self.logChannel, "{0.mention} ({0.name}) joined the Server!".format(member))

    # User left the Server
    async def on_member_remove(self, member):
        if self.logChannel:
            await bot.send_message(self.logChannel, "{0.mention} ({0.name}) left the Server!".format(member))

    # VoiceChannel and mute_state of User Changed
    async def on_voice_state_update(self, before, after):
        if self.logChannel:
            if before.voice_channel and not after.voice_channel :
                await bot.send_message(self.logChannel, "{0.mention} ({0.name}) disconnected from {0.voice_channel.mention}".format(before))

            elif not before.voice_channel and after.voice_channel:
                await bot.send_message(self.logChannel, "{0.mention} ({0.name}) joined {0.voice_channel.mention}".format(after))

            elif before.voice_channel and after.voice_channel and before.voice_channel != after.voice_channel:
                await bot.send_message(self.logChannel, "{1.mention} ({1.name}) moved from {0.voice_channel.mention} to {1.voice_channel.mention}".format(before, after))

    # User's Message got deleted unknown by whom
    async def on_message_delete(self, message):
        if self.logChannel:
            await bot.send_message(self.logChannel, "{0.author.mention}'s ({0.author.name}) message '{0.content}' in {0.channel.mention} got deleted".format(message))

    # User edited a Message
    async def on_message_edit(self, before, after):
        if self.logChannel:
            await bot.send_message(self.logChannel, "{1.author.mention} ({1.author.name}) changed: '{0.content}' to '{1.content}' in {0.channel.mention}".format(before, after))



bot = MyClient()
with open('./auth.json') as f:
    fileContent = f.read()
    bot.run(json.loads(fileContent)['token'])