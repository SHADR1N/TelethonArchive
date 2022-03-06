import configparser
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel, InputPeerUser
import os
import asyncio

config = configparser.ConfigParser()
config.read("Config.ini")


api_id = config['Settings']['api_id']
api_hash = config['Settings']['api_hash']
username = config['Settings']['username']
depth = int(config['Settings']['depth'])

client = TelegramClient(username, api_id, api_hash)
client.start()

async def dump_all_participants(): 
    data = []
    index = 0
    async for dialog in client.iter_dialogs():
        print(f'{index} - {dialog.name}')
        data.append(dialog.name)
        index += 1

    index = input('\nEnter index: ')
    async for dialog in client.iter_dialogs():
        if dialog.name == data[int(index)]:
            break
    await scrap_chat_member(dialog)
    return



async def scrap_chat_member(dialog):
    data = []
    offset_user = 0   
    limit_user = 100   
    all_participants = []   
    all_username = []

    filter_user = ChannelParticipantsSearch('')     
    while True:         
        participants = await client(GetParticipantsRequest(dialog,             
            filter_user, 
            offset_user, 
            limit_user, 
            hash=0))      
        if not participants.users:          
            break       
        all_participants.extend(participants.users)

        for username in participants.users: 
            if username.username:
                data.append('@'+username.username)


        offset_user += len(participants.users)    
        print('{} users collected'.format(offset_user))
        await asyncio.sleep(1)

    with open('users.txt', 'a+') as file:
        file.write('\n'.join(data))
    return



with client:
    client.loop.run_until_complete(dump_all_participants())


