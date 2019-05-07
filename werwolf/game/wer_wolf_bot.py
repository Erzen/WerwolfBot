import re

from discord import Member, User, Emoji

from werwolf.game.game import Game
from werwolf.utils import file_util


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
            if command == "createGame":
                await self.create_game(message, arguments)
            elif command == "join":
                await self.join_game(message, arguments)
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
            elif command == "leave":
                await self.leave_game(message, arguments)
            elif command == "next":
                await self.next(message, arguments)
            elif command == "back":
                await self.back(message, arguments)
            elif command == "pool":
                self.create_pool(message, arguments)
            elif command == "leader":
                await self.change_game_leader(message, arguments)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.discord_client.user and user != self.discord_client.user:
            game = self.get_game_with_message(reaction.message)
            if game is not None:
                if game.invite_emoji == reaction.emoji:
                    await game.add_player(user, None)

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.author == self.discord_client.user and user != self.discord_client.user:
            game = self.get_game_with_message(reaction.message)
            if game is not None:
                if game.invite_emoji == reaction.emoji:
                    await game.remove_player(user)

    async def create_game(self, message, arguments):
        game = self.get_game(message.author)
        game_id = arguments[0]
        del arguments[0]
        emojis = self.find_emojis(game_id, message.server)
        emoji = None if len(emojis) == 0 else emojis[0]
        game_id = str(emoji) if emoji else game_id

        if not game and game_id not in self.games:
            text = ' '.join(arguments)
            invite_message = None
            if emoji is not None:
                if text is None or text == '':
                    text = "Hallo @everyone es wurde ein Spiel geöffnet reacted auf diese Nachricht mit dem emoji {} um dabei zu sein!".format(emoji)
                invite_message = await self.discord_client.send_message(message.channel, "{}".format(text))
                await self.discord_client.add_reaction(invite_message, emoji)
            self.games[game_id] = Game(game_id, message.author, emoji, invite_message, self.discord_client)

            await self.discord_client.send_message(message.channel, "Spiel '{}' wurde erstellt.".format(game_id))
        else:
            await self.discord_client.send_message(message.channel, "Du hostest bereits ein Spiel oder die GameId ist bereits in benutzung!")

    def find_emojis(self, argument, server):
        found_emojis = []
        colon_emojis = re.findall(r'<:([a-zA-Z0-9_%&+-]+):([0-9]+)>', argument)
        for colon_emoji in colon_emojis:
            found_emojis.append(Emoji(name=colon_emoji[0], id=colon_emoji[1], server=server, require_colons=True, managed=False))
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
        for role in message.server.roles:
            if role.name == 'Lebendig' or role.name == 'Tot':
                for player in game.players:
                    await self.discord_client.remove_roles(player.member, role)

        del self.games[game.game_id]
        await self.discord_client.send_message(message.channel, "Das Spiel '{}' wurde beendet!".format(game.game_id))


    async def join_game(self, message, arguments):
        game_id = ' '.join(arguments)
        if game_id in self.games:
            await self.games[game_id].add_player(message.author, None)
        else:
            await self.discord_client.send_message(message.channel, "Game existiert nicht!")

    async def add_player(self, message, arguments):
        game = self.get_game(message.author)
        if not game:
            await self.discord_client.send_message(message.channel, "Du hostest derzeit kein Spiel!")
            return
        for mention in message.mentions:
            await game.add_player(mention, message.channel)

    async def kill_player(self, message, arguments):
        game = self.get_game(message.author)
        if not game:
            await self.discord_client.send_message(message.channel, "Du hostest derzeit kein Spiel!")
            return
        for mention in message.mentions:
            await game.kill_player(mention, message.channel)

    async def revive_player(self, message, arguments):
        game = self.get_game(message.author)
        if not game:
            await self.discord_client.send_message(message.channel, "Du hostest derzeit kein Spiel!")
            return
        for mention in message.mentions:
            await game.revive_player(mention, message.channel)

    async def list_players(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            playerNames = []
            for player in game.players:
                playerNames.append(player.member.nick if player.member.nick else player.member.name)
            await self.discord_client.send_message(message.channel, "Mitspieler:\n{}".format('\n'.join(playerNames)))

        else:
            await self.discord_client.send_message(message.channel, "Du hostest kein Spiel")

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
        if not game:
            await self.discord_client.send_message(message.channel, "Spiel existiert nicht")
            return
        for member in message.mentions:
            await game.remove_player(member)

    async def leave_game(self, message, arguments):
        game_id = ' '.join(arguments)
        if game_id in self.games:
            await self.games[game_id].remove_player(message.author)
        else:
            await self.discord_client.send_message(message.channel, "Game existiert nicht!")

    async def change_game_leader(self, message, arguments):
        game = self.get_game(message.author)
        for member in message.mentions:
            game.host = member
            break

    def create_pool(self, message, arguments):
        game = self.get_game(message.author)
        role_list = []
        role_count = 1
        for argument in arguments:
            if argument.isdigit():
                role_count = int(argument)
            else:
                for x in range(0, role_count):
                    role_list.append(argument)
                role_count = 1
        game.set_pool(role_list)
