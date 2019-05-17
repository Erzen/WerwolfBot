from werwolf.utils import text
class AdminBot():
    def __init__(self, client, **options):
        super(AdminBot, self).__init__(**options)
        self.discord_client = client

    __slots__ = ['discord_client']

    def __setstate__(self, state):
        return

    def __getstate__(self):
        return None

    # discord_client Log-In
    async def on_ready(self):
        print("AdminBot ready")

    # Called when a Member joins a Server.
    # Parameters:	member – The Member that joined.
    async def on_member_join(self, member):
        await member.send(text.get_greeting_text(member))