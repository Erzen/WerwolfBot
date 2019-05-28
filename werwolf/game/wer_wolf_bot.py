import re

from discord import Member, User, Emoji

from werwolf.game.game import Game
from werwolf.utils import file_util, text


class WerwolfBot():
    def __init__(self, client, **options):
        super(WerwolfBot, self).__init__(**options)
        backup = file_util.load_object('WerwolfBot.pkl')
        print("{} imported from Backup".format(backup))
        self.discord_client = client
        if backup:
            self.games = backup.games
        else:
            self.games = {}

    __slots__ = ['discord_client', 'games']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    # discord_client Log-In
    async def on_ready(self):
        print("WerwolfBot ready")

    # Commands
    async def on_message(self, message):
        if message.content[:1] == "/":
            arguments = message.content[1:].split(" ")
            arguments = list(filter(lambda a: a != '', arguments))
            command = arguments[0]
            arguments.remove(command)
            if command == "help":
                await self.whisper_help(message, arguments)
            if command == "createChat":
                await self.create_chat(message, arguments)
            elif command == "createGame":
                await self.create_game(message, arguments)
            elif command == "addPlayer":
                await self.add_player(message, arguments)
            elif command == "kill":
                await self.kill_player(message, arguments)
            elif command == "revive":
                await self.revive_player(message, arguments)
            elif command == "listPlayers":
                await self.list_players(message, arguments)
            elif command == "close":
                await self.close(message, arguments)
            elif command == "kick":
                await self.kick(message, arguments)
            elif command == "next":
                await self.next(message, arguments)
            elif command == "back":
                await self.back(message, arguments)
            elif command == "pool":
                await self.create_pool(message, arguments)
            elif command == "leader":
                await self.change_game_leader(message, arguments)

    async def whisper_help(self, message, arguments):
        await message.author.send(text.get_help_text())

    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.discord_client.user and user != self.discord_client.user:
            game = self.get_game_with_message(reaction.message)
            if game:
                if game.invite_emoji == reaction.emoji:
                    await game.add_player(user, None)

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.author == self.discord_client.user and user != self.discord_client.user:
            game = self.get_game_with_message(reaction.message)
            if game:
                if game.invite_emoji == reaction.emoji:
                    await game.remove_player(user)

    async def create_chat(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for role in game.pool_list:
                if role == arguments[0]:
                    get = 0
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")



    async def create_game(self, message, arguments):
        game = self.get_game(message.author)
        game_id = arguments[0]
        del arguments[0]
        emojis = self.find_emojis(game_id, message.guild)
        emoji = None if len(emojis) == 0 else emojis[0]
        game_id = str(emoji) if emoji else game_id

        if not game and game_id not in self.games:
            text = ' '.join(arguments)

            mentioned_channel = None
            for channel in message.channel_mentions:
                mentioned_channel = channel
                text = text.replace("{} ".format(mentioned_channel.mention), "").replace(" {}".format(mentioned_channel.mention), "").replace(mentioned_channel.mention, "")
                break
            if emoji is not None:
                if text is None or text == '':
                    text = "Hallo @everyone es wurde ein Spiel geöffnet reacted auf diese Nachricht mit dem emoji {} um dabei zu sein!".format(emoji)
                invite_message = await (message.channel if not mentioned_channel else mentioned_channel).send("{}".format(text))
                await invite_message.add_reaction(emoji)
                self.games[game_id] = Game(game_id, message.author, emoji, invite_message)
                await message.channel.send("Spiel '{}' wurde erstellt.".format(game_id))
            else:
                await message.channel.send("Der erste Parameter nach dem Command muss ein Emoji sein")
        else:
            await message.channel.send("Du hostest bereits ein Spiel oder die GameId ist bereits in benutzung!")

    def find_emojis(self, argument, server):
        found_emojis = []
        colon_emojis = re.findall(r'<:([a-zA-Z0-9_%&+-]+):([0-9]+)>', argument)
        for colon_emoji in colon_emojis:
            found_emojis.append(Emoji(guild=server, state=None, data={"require_colons":True, "managed":False, "id": colon_emoji[1], "name":colon_emoji[0]}))
        return found_emojis

    def get_game(self, identifier):
        if identifier not in self.games:
            for key in self.games:
                game = self.games[key]
                if isinstance(identifier, Member) or isinstance(identifier, User):
                    if game.host.id == identifier.id:
                        return game
                else:
                    if game.host.id == identifier:
                        return game
            return None
        else:
            return self.games[identifier]

    def get_game_with_message(self, message):
        for key in self.games:
            game = self.games[key]
            if game.invite_message.id == message.id:
                return game

    async def close(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for role in message.guild.roles:
                if role.name == 'Lebendig' or role.name == 'Tot':
                    for player in game.players:
                        await player.member.remove_roles(role)

            del self.games[game.game_id]
            await message.channel.send("Das Spiel '{}' wurde beendet!".format(game.game_id))
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")

    async def join_game(self, message, arguments):
        game_id = ' '.join(arguments)
        if game_id in self.games:
            await self.games[game_id].add_player(message.author, None)
        else:
            await message.channel.send("Game existiert nicht!")

    async def add_player(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for mention in message.mentions:
                await game.add_player(mention, message.channel)
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")

    async def kill_player(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for mention in message.mentions:
                await game.kill_player(mention, message.channel)
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")

    async def revive_player(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for mention in message.mentions:
                await game.revive_player(mention, message.channel)
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")


    async def list_players(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            playerNames = []
            for player in game.players:
                playerNames.append(player.member.nick if player.member.nick else player.member.name)
            await message.channel.send("Mitspieler:\n{}".format('\n'.join(playerNames)))
        else:
            await message.channel.send("Du hostest derzeit kein Spiel!")

    async def next(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            await game.next_phase()

    async def back(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            await game.previous_phase()

    async def kick(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for member in message.mentions:
                await game.remove_player(member)
                await message.channel.send("Der Spieler '{}' wurde vom Spiel '{}' gekickt.".format(member.nick if member.nick else member.name, game.invite_emoji))
        else:
            await message.channel.send("Spiel existiert nicht")

    async def leave_game(self, message, arguments):
        game_id = ' '.join(arguments)
        if game_id in self.games:
            await self.games[game_id].remove_player(message.author)
        else:
            await message.channel.send("Game existiert nicht!")

    async def change_game_leader(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for member in message.mentions:
                game.host = member
                break
        else:
            await message.channel.send("Game existiert nicht!")

    async def create_pool(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            role_list = []
            role_count = 1
            for argument in arguments:
                if argument.isdigit():
                    role_count = int(argument)
                    if role_count > 20:
                        role_count = 20
                else:
                    for x in range(0, role_count):
                        role_list.append(argument)
                    role_count = 1
            game.set_pool(role_list)
        else:
            await message.channel.send("Game existiert nicht!")
