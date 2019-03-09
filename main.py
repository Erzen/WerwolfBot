import json

from wer_wolf_bot import MyClient

with open('./auth.json') as f:
    fileContent = f.read()
    MyClient().run(json.loads(fileContent)['token'])