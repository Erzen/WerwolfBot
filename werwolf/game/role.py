
class Role():
    def __init__(self, id, active_rounds, **options):
        super(Role, self).__init__(**options)
        self.id = id
        self.active_rounds = active_rounds

    __slots__ = ['id', 'active_rounds']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None