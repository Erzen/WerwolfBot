import json
import logging

from discord import Client, Game

from werwolf.game.wer_wolf_bot import WerwolfBot
from werwolf.log.server_log import ServerLog

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class MyClient(Client):
    __slots__ = [ 'serverLog', "werwolfBot"]

    def __init__(self, **options):
        super(MyClient, self).__init__(**options)
        self.serverLog = ServerLog(self)
        self.werwolfBot = WerwolfBot(self)
        #self.max_messages = 5000 # 5000 is the default value


    #     Called when the client is done preparing the data received from Discord. Usually after login is successful and
    #     the Client.servers and co. are filled up.
    #
    #     Warning
    #
    #     This function is not guaranteed to be the first event called. Likewise, this function is not guaranteed to
    #     only be called once. This library implements reconnection logic and thus will end up calling this event whenever a
    #     RESUME request fails.
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("The bot is ready!")
        await self.change_presence(activity=Game(name="Werwölfe von Düsterwald"))
        await self.serverLog.on_ready()
        await self.werwolfBot.on_ready()

    # Called when a message is created and sent to a server.
    # Parameters:	message – A Message of the current message.
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user:
            return
        try:
            await self.serverLog.on_message(message)
        except Exception as e:
            logger.exception(e)
        try:
            await self.werwolfBot.on_message(message)
        except Exception as e:
            logger.exception(e)


    # Called when a Member joins a Server.
    # Parameters:	member – The Member that joined.
    async def on_member_join(self, member):
        await self.serverLog.on_member_join(member)

    # Called when a Member leaves a Server.
    # Parameters:	member – The Member that left.
    async def on_member_remove(self, member):
        await self.serverLog.on_member_remove(member)

    # Called when a Member updates their profile.
    #
    # This is called when one or more of the following things change:
    #
    #     status
    #     game playing
    #     avatar
    #     nickname
    #     roles
    #
    # Parameters:
    #
    #     before – The Member that updated their profile with the old info.
    #     after – The Member that updated their profile with the updated info.
    async def on_member_update(self, before, after):
        await self.serverLog.on_member_update(before, after)

    # Called when a Member changes their voice state.
    #
    # The following, but not limited to, examples illustrate when this event is called:
    #
    # A member joins a voice room.
    # A member leaves a voice room.
    # A member is muted or deafened by their own accord.
    # A member is muted or deafened by a server administrator.
    #
    # Parameters:
    #
    # before – The Member whose voice state changed prior to the changes.
    # after – The Member whose voice state changed after the changes.
    async def on_voice_state_update(self, member, before, after):
        await self.serverLog.on_voice_state_update(member, before, after)

    # Called when a message is deleted. If the message is not found in the Client.messages cache, then these events will
    # not be called. This happens if the message is too old or the client is participating in high traffic servers.
    # To fix this, increase the max_messages option of Client.
    #
    # Parameters:	message – A Message of the deleted message.
    async def on_message_delete(self, message):
        await self.serverLog.on_message_delete(message)

    # Called when a message receives an update event. If the message is not found in the Client.messages cache, then these events will not be called. This happens if the message is too old or the client is participating in high traffic servers. To fix this, increase the max_messages option of Client.
    #
    # The following non-exhaustive cases trigger this event:
    #
    #     A message has been pinned or unpinned.
    #     The message content has been changed.
    #
    #     The message has received an embed.
    #             For performance reasons, the embed server does not do this in a “consistent” manner.
    #
    #     A call message has received an update to its participants or ending time.
    #
    # Parameters:
    #
    #     before – A Message of the previous version of the message.
    #     after – A Message of the current version of the message.
    async def on_message_edit(self, before, after):
        await self.serverLog.on_message_edit(before, after)

    # Called when a message has a reaction added to it. Similar to on_message_edit, if the message is not found in the Client.messages cache, then this event will not be called.
    #
    # Note:
    #   To get the message being reacted, access it via Reaction.message.
    # Parameters:
    #
    # reaction – A Reaction showing the current state of the reaction.
    # user – A User or Member of the user who added the reaction.
    async def on_reaction_add(self, reaction, user):
        try:
            await self.serverLog.on_reaction_add(reaction, user)
        except Exception as e:
            logger.exception(e)
        try:
            await self.werwolfBot.on_reaction_add(reaction, user)
        except Exception as e:
            logger.exception(e)


    # Called when a message has a reaction removed from it. Similar to on_message_edit, if the message is not found in the Client.messages cache, then this event will not be called.
    #
    # Note:
    #   To get the message being reacted, access it via Reaction.message.
    #
    # Parameters:
    #
    #   reaction – A Reaction showing the current state of the reaction.
    #   user – A User or Member of the user who removed the reaction.
    async def on_reaction_remove(self, reaction, user):
        try:
            await self.serverLog.on_reaction_remove(reaction, user)
        except Exception as e:
            logger.exception(e)
        try:
            await self.werwolfBot.on_reaction_remove(reaction, user)
        except Exception as e:
            logger.exception(e)

    # Called when a message has all its reactions removed from it. Similar to on_message_edit, if the message is not found in the Client.messages cache, then this event will not be called.
    # Parameters:
    #
    #     message – The Message that had its reactions cleared.
    #     reactions – A list of Reactions that were removed.
    async def on_reaction_clear(self, message, reactions):
        await self.serverLog.on_reaction_clear(message, reactions)

    # Called when a Member gets banned from a Server.
    #
    # You can access the server that the member got banned from via Member.server.
    # Parameters:	member – The member that got banned.
    async def on_member_ban(self, guild, member):
        await self.serverLog.on_member_ban(guild, member)

    # Called when a User gets unbanned from a Server.
    # Parameters:
    #
    # server – The server the user got unbanned from.
    # user – The user that got unbanned.
    async def on_member_unban(self, member):
        await self.serverLog.on_member_unban(member)

    # Called when a Server updates, for example:
    #
    #     Changed name
    #     Changed AFK channel
    #     Changed AFK timeout
    #     etc
    #
    # Parameters:
    #
    # before – The Server prior to being updated.
    # after – The Server after being updated.
    async def on_guild_update(self, before, after):
        await self.serverLog.on_guild_update(before, after)


    # Called when a Server creates a new Role.
    #
    # To get the server it belongs to, use Role.server.
    # Parameters:	role – The Role that was created.
    async def on_guild_role_create(self, role):
        await self.serverLog.on_guild_role_create(role)

    # Called when a Server deletes a new Role.
    #
    # To get the server it belongs to, use Role.server.
    # Parameters:	role – The Role that was deleted.
    async def on_guild_role_delete(self, role):
        await self.serverLog.on_guild_role_delete(role)

    # Called when a Role is changed server-wide.
    # Parameters:
    #
    # before – The Role that updated with the old info.
    # after – The Role that updated with the updated info.
    async def on_guild_role_update(self, before, after):
        await self.serverLog.on_guild_role_update(before, after)


    # Called when a Server adds or removes Emoji.
    # Parameters:
    #
    # before – A list of Emoji before the update.
    # after – A list of Emoji after the update.
    async def on_guild_emojis_update(self, guild, before, after):
        await self.serverLog.on_guild_emojis_update(guild, before, after)

with open('./auth.json') as f:
    fileContent = f.read()
    authDict = json.loads(fileContent)
    MyClient().run(authDict['token'])

# with open('./authFeco.json') as f:
#     fileContent = f.read()
#     authDict = json.loads(fileContent)
#     MyClient().run(authDict["email"],authDict["password"], bot=False)
