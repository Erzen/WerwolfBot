import discord
from discord import Member

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
            command = arguments[0]
            arguments.remove(command)
            if command == "createGame":
                self.create_game(message, arguments)
            elif command == "join":
                self.join_game(message, arguments)
            elif command == "addPlayer":
                self.add_player(message, arguments)
            elif command == "listPlayers":
                self.list_players(message, arguments)
            elif command == "close":
                self.close(message, arguments)
            elif command == "kick":
                self.kick(message, arguments)
            elif command == "next":
                self.next(message, arguments)
            elif command == "back":
                self.back(message, arguments)


    def create_game(self, message, arguments):
        print("create game")
        game = self.get_game(message.author)
        game_id = ' '.join(arguments)
        if not game and game_id not in self.games:
            self.games[game_id] = Game(game_id, message.author.id)
        else:
            print("Du hostest bereits ein Spiel oder die GameId ist bereits in benutzung!")

    def get_game(self, identifier):
        if identifier not in self.games:
            for key in self.games:
                game = self.games[key]
                if isinstance(identifier, Member):
                    if game.host_id == identifier.id:
                        return game
                else:
                    if game.host_id == identifier:
                        return game
            return None
        else:
            return self.games[identifier]

    def close(self, message, arguments):
        game = self.get_game(message.author)
        del self.games[game.game_id]

    def join_game(self, message, arguments):
        print("join_game")
        game_id = ' '.join(arguments)
        if game_id in self.games:
            self.games[game_id].add_player_id(message.author.id)
        else:
            print("Game existiert nicht!")

    def add_player(self, message, arguments):
        print("add_player")
        game = self.get_game(message.author)
        if not game:
            print("Du hostest derzeit kein Spiel!")
            return
        for mention in message.mentions:
            game.add_player_id(mention.id)

    def list_players(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            for player in game.players:
                print(discord.utils.get(message.server.members, id=player))
        else:
            print("Du hostest kein Spiel")

    def next(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            game.next_phase()

    def back(self, message, arguments):
        game = self.get_game(message.author)
        if game:
            game.previous_phase()

    def kick(self, message, arguments):
        game = self.get_game(message.author)
        if not game:
            print("Spiel existiert nicht")
            return
        for member in message.mentions:
            game.remove_player(member.id)
