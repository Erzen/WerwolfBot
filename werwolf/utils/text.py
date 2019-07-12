def get_help_text():
    return "__**Commands für everyone**__\n\
```\n\
/createGame [Emoji] [Channel] [Text der Nachricht]\n\
- erstellt Spiel\n\
```\n\
__**Commands für Spielleitung**__\n\
```\n\
/addPlayer @Spieler @Spieler2\n\
- fügt Spieler dem Spiel zu\n\
``````\n\
/kill @Spieler @Spieler\n\
- nimmt dem Spieler Lebendig und setzt ihn auf Tot\n\
``````\n\
/revive @Spieler @Spieler\n\
- nimmt dem Spieler Tot und setzt ihn auf Lebendig\n\
``````\n\
/listPlayers\n\
- listet alle Spieler auf\n\
``````\n\
/close\n\
- beendet das Spiel und entfernt Lebendig und Tot\n\
``````\n\
/kick @Spieler1 @Spieler2\n\
- entfernt Spieler vom Spiel\n\
``````\n\
/pool 3 Werwolf Nutte Hexe Jäger 3 Dorfbewohner\n\
- erstellt einen Rollenpool der in der Phase 'gaming' verteilt wird\n\
``````\n\
/next\n\
- wechselt von Spielphase 'inviting' -> 'checking_roles' -> 'gaming' und verteilt Rollen bei 'gaming'\n\
``````\n\
/shuffle\n\
- während der Spielphase 'checking_roles' kann die Rollenverteilung nochmal durchmischt werden\n\
``````\n\
/back\n\
- wechselt zurück zur Phase 'inviting'\n\
``````\n\
/leader @Spieler\n\
- gibt die Spielleitung an @Spieler ab (noch buggy)\n\
```"

def get_greeting_text(member):
    return "Hey {}, :heart:-lich willkommen in unserer Community! Schön, dass du her gefunden hast. <:WolfHeart:561592501257895936>\n\
Der Server Werwolf steht grundsätzlich für das Gesellschaftsspiel \"Werwölfe von Düsterwald\". \
Wir spielen fast täglich auf dem Server. Neben Werwolf bieten wir noch andere Spiele, wie Secret Hitler\
, Werwolf Vollmondnacht/Morgengrauen, skribbl.io usw. an. Diese sowie alles Weitere findest du \
auf unserem Discord. Um Berechtigungen für alle Channel auf dem Server zu erhalten, reagiere im Channel <#463009130777411584> \
mit dem :white_check_mark:. Fühl dich wie zu Hause - bei Unklarheiten einfach fragen. Wir freuen uns, bald \
mit dir zu spielen! <:HappyTessa:490482340116561921>".format(member.nick if member.nick else member.name)
