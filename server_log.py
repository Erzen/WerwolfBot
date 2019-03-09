import datetime

import utility


class ServerLog():
    def __init__(self, client, **options):
        super(ServerLog, self).__init__(**options)
        backup = utility.load_object('ServerLog.pkl')
        print("{} imported from Backup".format(backup))
        self.log_channel_id = None if not backup else backup.log_channel_id
        self.bot = client
        self.log_channel = None

    __slots__ = ['log_channel', 'bot', 'log_channel_id']

    def __setstate__(self, state):
        self.log_channel_id = state['log_channel_id']

    def __getstate__(self):
        state = {'log_channel_id': self.log_channel_id}
        return state

    def set_log_channel(self, logChannel):
        self.log_channel = logChannel
        self.log_channel_id = logChannel.id
        utility.save_object(self, "ServerLog.pkl")

    # Bot Log-In
    async def on_ready(self):
        self.log_channel = None if not self.log_channel_id else self.bot.get_channel(self.log_channel_id)
        print("server_log ready")

    # Commands
    async def on_message(self, message):
        if (message.author.id != '411643310848081921' and #Fukano
            message.author.id != '232838719818825728' and #Erzen
            message.author.id != '267744603371733002'):   #Linn
            return
        if message.content[:1] == "/":
            command = message.content[1:]
            if command == "setupChannel":
                self.set_log_channel(message.channel)
                await self.bot.send_message(self.log_channel, "The Channel {} was setup!".format(self.log_channel))
            elif command == "testChannel":
                if self.log_channel:
                    await self.bot.send_message(self.log_channel, "Channel erfolgreich getestet!")
                else:
                    await self.bot.send_message(message.channel, "Channel test ist Fehlgeschlagen!")
            else:
                await self.bot.send_message(message.author, "private Bestätigung")


    # User joined Server
    async def on_member_join(self, member):
        await self.log_event(member, "joined the Server!")

    # User left the Server
    async def on_member_remove(self, member):
        await self.log_event(member, "left the Server!")

    # User was updated
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            await self.log_event(before, "roles changed from:\n{0}\n\nto:\n{1}".format(self.extract_role_names(before.roles), self.extract_role_names(after.roles)))
        if before.nick != after.nick:
            await self.log_event(before, "nickname changed from:\n{0}\n\nto:\n{1}".format(before.nick if before.nick else before.name, after.nick if after.nick else after.name))

    def extract_role_names(self, roles):
        role_names = None
        for role in roles:
            roleName = role.name
            if roleName == "@everyone":
                roleName = "@every_one"
            role_names = "{}\n{}".format(role_names, roleName)
        return role_names

    # VoiceChannel and mute_state of User Changed
    async def on_voice_state_update(self, before, after):
        if before.voice_channel and not after.voice_channel :
            await self.log_event(before, "disconnected from {0.voice_channel.mention}".format(before))
        elif not before.voice_channel and after.voice_channel:
            await self.log_event(after, "joined {0.voice_channel.mention}".format(after))
        elif before.voice_channel and after.voice_channel and before.voice_channel != after.voice_channel:
            await self.log_event(after, "moved from {0.voice_channel.mention} to {1.voice_channel.mention}".format(before, after))

    # User's Message got deleted unknown by whom
    async def on_message_delete(self, message):
        await self.log_event(message.author, " got his message '{0.content}' in {0.channel.mention} deleted".format(message))

    # User edited a Message
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            await self.log_event(after, "changed: '{0.content}' to '{1.content}' in {0.channel.mention}".format(before, after))

    # reaction added
    async def on_reaction_add(self, reaction, user):
        await self.log_event(user, "added the reaction {0.emoji} to {0.message.author}' message".format(reaction))

    # reaction removed
    async def on_reaction_remove(self, reaction, user):
        await self.log_event(user, "removed the reaction {0.emoji} from {0.message.author}'s message".format(reaction))

    # reaction cleared
    async def on_reaction_clear(self, message, reactions):
        await self.log_event(message.author, " got all reaction to his message cleared")

    # main log method with timestamp and user identification
    async def log_event(self, user, message):
        if self.log_channel:
            await self.bot.send_message(self.log_channel, "`{0}`\n{1.mention} ({1}) {2}".format(datetime.datetime.utcnow(), user, message))
