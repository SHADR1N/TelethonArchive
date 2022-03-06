import configparser
from telethon import TelegramClient, events
from pprint import pprint
import os
import os.path


if os.path.exists(path = './Answer') == False:
    os.mkdir(path = './Answer')

config = configparser.ConfigParser()
config.read("Config.ini")


api_id = config['Settings']['api_id']
api_hash = config['Settings']['api_hash']
username = config['Settings']['username']
depth = int(config['Settings']['depth'])

client = TelegramClient(username, api_id, api_hash)
client.start()

async def dump_all_participants(): 
    async for dialog in client.iter_dialogs():
        offset = 0
        data = []
        print(dialog.name)
        async for (messages) in client.iter_messages(dialog.id):
            try:
                if dialog.entity.username:
                    username = dialog.entity.username
                else:
                    username = None
                    name = dialog.name
                date = messages.date
                text = messages.message
                text = text.replace('  ', ' ')
                text = text.replace('  ', ' ')
                text = text.replace('  ', ' ')
                text = text.replace('  ', ' ')
                text = text.replace('\n', ' ')

                if username == None:
                    row = [str(date), str(name), str(text)]
                else:
                    row = [str(date), f'@{str(username)}', str(text)]

                data.append(row)

                offset += 1
                if offset >= depth:
                    break

            except:
                offset += 1
                if offset >= depth:
                    break

        if username == None:
            n = []
            for i in name:
                if i.isalpha() or i.isdigit() == True:
                    n.append(i) 
            names = ''.join(n)

        else:
            names = username

        for row in data:
            row = ' | '.join(row)
            with open(f'Answer/{names}.txt', 'a', encoding = 'utf-8') as f:
                f.write(f'{row}\n')
                f.close()

with client:
    client.loop.run_until_complete(dump_all_participants())