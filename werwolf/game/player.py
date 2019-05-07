
class Player():
    def __init__(self, member, **options):
        super(Player, self).__init__(**options)
        self.member = member
        self.role = None
        self.state = "alive"
        self.impediments = []

    __slots__ = ['member', 'role', 'state', 'impediments']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    # def __str__(self):
    #     return "{0.member.nick}".format(self)