from discord import Client, Game

from server_log import ServerLog


class MyClient(Client):
    __slots__ = [ 'logChannel' , 'serverLog']

    def __init__(self, **options):
        super(MyClient, self).__init__(**options)
        self.logChannel = None
        self.serverLog = ServerLog(self)
        #self.max_messages = 5000 # 5000 is the default value

    # Bot Log-In
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("The bot is ready!")
        await self.change_presence(game=Game(name="Making a bot"))
        await self.serverLog.on_ready()

    # New Message
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user or \
           (message.author.id != '411643310848081921' and #Fukano
            message.author.id != '232838719818825728' and #Erzen
            message.author.id != '267744603371733002'):   #Linn
            return
        await self.serverLog.on_message(message)

    # User joined Server
    async def on_member_join(self, member):
        await self.serverLog.on_member_join(member)

    # User left the Server
    async def on_member_remove(self, member):
        await self.serverLog.on_member_remove(member)

    # User was updated
    async def on_member_update(self, before, after):
        await self.serverLog.on_member_update(before, after)

    # VoiceChannel and mute_state of User Changed
    async def on_voice_state_update(self, before, after):
        await self.serverLog.on_voice_state_update(before, after)

    # User's Message got deleted unknown by whom
    async def on_message_delete(self, message):
        await self.serverLog.on_message_delete(message)

    # User edited a Message
    async def on_message_edit(self, before, after):
        await self.serverLog.on_message_edit(before, after)

    # user did react to something
    async def on_reaction_add(self, reaction, user):
        await self.serverLog.on_reaction_add(reaction, user)

    # user removed reaction from something
    async def on_reaction_remove(self, reaction, user):
        await self.serverLog.on_reaction_remove(reaction, user)

    # user's message was cleared from all reactions
    async def on_reaction_clear(self, message, reactions):
        await self.serverLog.on_reaction_clear(message, reactions)