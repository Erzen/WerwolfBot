import datetime

from werwolf.utils import file_util, diff_util


class ServerLog():
    def __init__(self, client, **options):
        super(ServerLog, self).__init__(**options)
        backup = file_util.load_object('ServerLog.pkl')
        print("{} imported from Backup".format(backup))
        self.log_channel_id = None if not backup else backup.log_channel_id
        self.discord_client = client
        self.log_channel = None

    __slots__ = ['log_channel', 'discord_client', 'log_channel_id']

    def __setstate__(self, state):
        self.log_channel_id = state['log_channel_id']

    def __getstate__(self):
        state = {'log_channel_id': self.log_channel_id}
        return state

    def set_log_channel(self, logChannel):
        self.log_channel = logChannel
        self.log_channel_id = logChannel.id
        file_util.save_object(self, "ServerLog.pkl")

    #     Called when the client is done preparing the data received from Discord. Usually after login is successful and
    #     the Client.servers and co. are filled up.
    #
    #     Warning
    #
    #     This function is not guaranteed to be the first event called. Likewise, this function is not guaranteed to
    #     only be called once. This library implements reconnection logic and thus will end up calling this event whenever a
    #     RESUME request fails.
    async def on_ready(self):
        self.log_channel = None if not self.log_channel_id else self.discord_client.get_channel(self.log_channel_id)
        print("ServerLog ready")

    # Called when a message is created and sent to a server.
    # Parameters:	message – A Message of the current message.
    async def on_message(self, message):
        if (message.author.id != 411643310848081921 and #Fukano
            message.author.id != 232838719818825728 and #Erzen
            message.author.id != 267744603371733002):   #Linn
            return
        if message.content[:1] == "/":
            command = message.content[1:]
            if command == "setupChannel":
                self.set_log_channel(message.channel)
                await self.log_channel.send("The Channel {} was setup!".format(self.log_channel))
            elif command == "testChannel":
                if self.log_channel:
                    await self.log_channel.send("Channel erfolgreich getestet!")
                else:
                    await self.log_channel.send("Channel test ist Fehlgeschlagen!")


    # main log method with timestamp and user identification
    async def log_event(self, user, message):
        if self.log_channel:
            await self.log_channel.send("`{0}`\n{1} ({2}) {3}".format(datetime.datetime.utcnow(), user.nick if user.nick else user.name, user, message))

    # Called when a Member joins a Server.
    # Parameters:	member – The Member that joined.
    async def on_member_join(self, member):
        await self.log_event(member, "joined the Server!")

    # Called when a Member leaves a Server.
    # Parameters:	member – The Member that left.
    async def on_member_remove(self, member):
        await self.log_event(member, "left the Server!")

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
        if before.roles != after.roles:
            removed_roles = list(set(before.roles) - set(after.roles))
            added_roles = list(set(after.roles) - set(before.roles))
            if len(added_roles) > 0:
                await self.log_event(before, "got role(s) **__{0}__** added".format(self.extract_role_names(added_roles)))
            if len(removed_roles) > 0:
                await self.log_event(before, "got role(s) **__{0}__** removed".format(self.extract_role_names(removed_roles)))
        if before.nick != after.nick:
            await self.log_event(before, "nickname changed from:__**{0}**__ to: __**{1}**__".format(before.nick if before.nick else before.name, after.nick if after.nick else after.name))

    def extract_role_names(self, roles):
        role_names = []
        for role in roles:
            role_names.append(role.name)
        return ", ".join(role_names)

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
    async def on_voice_state_update(self, user, before, after):
        if before.channel and not after.channel :
            await self.log_event(user, "disconnected from __**{0.channel.mention}**__".format(before))
        elif not before.channel and after.channel:
            await self.log_event(user, "joined __**{0.channel.mention}**__".format(after))
        elif before.channel and after.channel and before.channel != after.channel:
            await self.log_event(user, "moved from __**{0.channel.mention}**__ to __**{1.channel.mention}**__".format(before, after))

    # Called when a message is deleted. If the message is not found in the Client.messages cache, then these events will
    # not be called. This happens if the message is too old or the client is participating in high traffic servers.
    # To fix this, increase the max_messages option of Client.
    #
    # Note: you need audittrail-access to figure out who deleted the Message
    #
    # Parameters:	message – A Message of the deleted message.
    async def on_message_delete(self, message):
        await self.log_event(message.author, " got his message '{0.content}' in {0.channel.mention} deleted".format(message))

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
        if before.content != after.content:
            await self.log_event(after.author, "hat folgende Nachricht bearbeitet:\n{}".format(diff_util.format_diff_text(before.content, after.content)))

    # Called when a message has a reaction added to it. Similar to on_message_edit, if the message is not found in the Client.messages cache, then this event will not be called.
    #
    # Note:
    #   To get the message being reacted, access it via Reaction.message.
    # Parameters:
    #
    # reaction – A Reaction showing the current state of the reaction.
    # user – A User or Member of the user who added the reaction.
    async def on_reaction_add(self, reaction, user):
        await self.log_event(user, "added the reaction {0.emoji} to __**{0.message.author}**__' message".format(reaction))

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
        await self.log_event(user, "removed the reaction {0.emoji} from __**{0.message.author}**__'s message".format(reaction))

    # Called when a message has all its reactions removed from it. Similar to on_message_edit, if the message is not found in the Client.messages cache, then this event will not be called.
    # Parameters:
    #
    #     message – The Message that had its reactions cleared.
    #     reactions – A list of Reactions that were removed.
    async def on_reaction_clear(self, message, reactions):
        await self.log_event(message.author, "got all reaction to his message cleared")

    # Called when a Member gets banned from a Server.
    #
    # You can access the server that the member got banned from via Member.server.
    # Parameters:	member – The member that got banned.
    async def on_member_ban(self, guild, member):
        await self.log_event(member, "got banned")

    # Called when a User gets unbanned from a Server.
    # Parameters:
    #
    # server – The server the user got unbanned from.
    # user – The user that got unbanned.
    async def on_member_unban(self, member):
        await self.log_event(member, "got unbanned")


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
        return


    # Called when a Server creates a new Role.
    #
    # To get the server it belongs to, use Role.server.
    # Parameters:	role – The Role that was created.
    async def on_guild_role_create(self, role):
        return

    # Called when a Server deletes a new Role.
    #
    # To get the server it belongs to, use Role.server.
    # Parameters:	role – The Role that was deleted.
    async def on_guild_role_delete(self, role):
        return

    # Called when a Role is changed server-wide.
    # Parameters:
    #
    # before – The Role that updated with the old info.
    # after – The Role that updated with the updated info.
    async def on_guild_role_update(self, before, after):
        return


    # Called when a Server adds or removes Emoji.
    # Parameters:
    #
    # before – A list of Emoji before the update.
    # after – A list of Emoji after the update.
    async def on_guild_emojis_update(self, guild, before, after):
        return

    #------------------------------Log-Specific Events--------------------------------------------------

    # Called when a Server is either created by the Client or when the Client joins a server.
    # Parameters:	server – The class:Server that was joined.
    async def on_guild_join(self, server):
        return

    # Called when a Server is removed from the Client.
    #
    # This happens through, but not limited to, these circumstances:
    #
    # The client got banned.
    # The client got kicked.
    # The client left the server.
    # The client or the server owner deleted the server.
    #
    # In order for this event to be invoked then the Client must have been part of the server to begin with. (i.e. it is part of Client.servers)
    # Parameters:	server – The Server that got removed.
    async def on_guild_remove(self, server):
        return




