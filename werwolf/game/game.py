import random

from werwolf.game.player import Player


class Game():
    def __init__(self, game_id, host, emoji, invite_message, **options):
        super(Game, self).__init__(**options)
        self.host = host
        self.game_id = game_id
        self.phase = "inviting"
        self.players = []
        self.pool_list = []
        self.invite_message = invite_message
        self.invite_emoji = emoji

    __slots__ = ['game_id', 'host', 'players', 'phase', 'pool_list', 'invite_emoji', 'invite_message']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    def __str__(self):
        return "Game({}, {}, {}, {})".format(self.game_id, self.host, self.invite_emoji, self.invite_message)

    async def add_player(self, member, channel):
        if self.phase == "inviting":
            player_already_invited = 0
            for player in self.players:
                if member == player.member:
                    player_already_invited = 1
                    break

            for role in member.guild.roles:
                if role.name == 'Lebendig':
                    await member.add_roles(role)
            if player_already_invited == 0:
                self.players.append(Player(member))
                #self.players.sort(key=member.nick)
                if channel is not None:
                    await channel.send("Spieler '{}' hinzugefügt!".format(member.nick if member.nick else member.name))

            else:
                self.host.send("Der Spieler ist dem Spiel bereits beigetreten")
        else:
            self.host.send("Es können in der aktuellen Phase keine weiteren Spieler hinzugefügt werden dummy!")

    async def kill_player(self, member, channel):
        if self.phase == "gaming":
            for role in member.guild.roles:
                if role.name == 'Lebendig':
                    await member.remove_roles(role)
                if role.name == 'Tot':
                    await member.add_roles(role)

            await channel.send("Spieler '{}' ist gestorben!".format(member.nick if member.nick else member.name))
        else:
            await channel.send("Das Spiel hat noch nicht begonnen. Hör auf schon jetzt Leute zu töten!")

    async def revive_player(self, member, channel):
        if self.phase == "gaming":
            for role in member.guild.roles:
                if role.name == 'Lebendig':
                    await member.add_roles(role)
                if role.name == 'Tot':
                    await member.remove_roles(role)

            await channel.send("Spieler '{}' ist wieder auferstanden!".format(member.nick if member.nick else member.name))
        else:
            await channel.send("Das Spiel hat noch nicht begonnen. Hör auf schon jetzt Leute wieder zubeleben!")


    async def remove_player(self, member):
        for player in self.players:
            if player.member == member:
                for role in member.guild.roles:
                    if role.name == 'Lebendig' or role.name == 'dörfler':
                        await member.remove_roles(role)
                self.players.remove(player)

    def set_pool(self, pool_list):
        self.pool_list = pool_list

    async def next_phase(self):
        if self.phase == "inviting":
            if len(self.players) > len(self.pool_list):
                await self.host.send("Zu wenige Rollen für die Anzahl der Spieler")
                return
            random.shuffle(self.pool_list)
            for i in range(0,len(self.players)):
                player_name = self.players[i].member.nick if self.players[i].member.nick else self.players[i].member.name
                self.players[i].role = self.pool_list[i]
                await self.host.send("{0} {1}".format(player_name, self.players[i].role))
                try:
                    await self.players[i].member.send("{}".format(self.players[i].role))
                except:
                    await self.host.send("Error player {} cannot receive Message".format(player_name))



            self.phase = "gaming"
            await self.host.send("phase: {}".format(self.phase))


    async def previous_phase(self):
        if self.phase == "gaming":
            self.phase = "inviting"
            await self.host.send("phase: {}".format(self.phase))

    __repr__ = __str__
