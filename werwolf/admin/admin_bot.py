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
        await member.send("Hey {}, :heart:-lich willkommen in unserer Community! Schön, dass du her gefunden hast. <:WolfHeart:561592501257895936>\n\
Der Server Werwolf steht grundsätzlich für das Gesellschaftsspiel \"Werwölfe von Düsterwald\". \
Wir spielen fast täglich auf dem Server. Neben Werwolf bieten wir noch andere Spiele, wie Secret Hitler\
, Werwolf Vollmondnacht/Morgengrauen, skribbl.io usw. an. Diese sowie alles Weitere findest du links unter \
\"Regeln und Infos\". Fühl dich wie zu Hause - bei Unklarheiten einfach fragen. Wir freuen uns, bald mit dir\
 zu spielen! <:HappyTessa:490482340116561921>".format(member.nick if member.nick else member.name))