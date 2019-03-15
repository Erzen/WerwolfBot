from werwolf.game.player import Player

class Game():
    def __init__(self, game_id, host_id, **options):
        super(Game, self).__init__(**options)
        self.host_id = host_id
        self.game_id = game_id
        self.phase = "inviting"
        self.players = []

    __slots__ = ['game_id', 'host_id', 'players', 'phase']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    def add_player_id(self, player_id):
        if self.phase == "inviting":
            if player_id not in self.players:
                self.players.append(Player(player_id))
            else:
                print("Der Spieler ist dem Spiel bereits beigetreten")
        else:
            print("Es können in der aktuellen Phase keine weiteren Spieler hinzugefügt werden dummy!")

    def remove_player(self, player_id):
        for player in self.players:
            if player.member_id == player_id:
                self.players.remove(player)

    def next_phase(self):
        if self.phase == "inviting":
            self.phase = "gaming"


    def previous_phase(self):
        if self.phase == "gaming":
            self.phase = "inviting"