
class Player():
    def __init__(self, member_id, **options):
        super(Player, self).__init__(**options)
        self.member_id = member_id
        self.role = None
        self.state = "alive"
        self.impediments = []

    __slots__ = ['member_id', 'role', 'state', 'impediments']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None