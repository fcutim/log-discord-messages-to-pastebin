from discord.ext import commands
import discord
import requests

TOKEN = 'YOUR-DISCORD-BOT-TOKEN-HERE'
PASTEBIN_API_KEY = 'YOUR-PASTEBIN-KEY-HERE'

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

client.remove_command('help')
message_logs = []  # Eine Liste zum Speichern der Nachrichten

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.content.startswith('!start'):
        await message.channel.send('Die Aufzeichnung der Nachrichten hat begonnen.')
        message_logs.clear()  # Liste leeren, um von vorne zu beginnen

    elif message.content.startswith('!stop'):
        await message.channel.send('Die Aufzeichnung der Nachrichten wurde gestoppt.')
        if message_logs:
            text_to_upload = '\n'.join(message_logs)
            paste_url = upload_to_pastebin(text_to_upload)
            if paste_url:
                await message.channel.send('Die Nachrichten wurden erfolgreich auf Pastebin hochgeladen. Hier ist der Link: ' + paste_url)
            else:
                await message.channel.send('Fehler beim Hochladen der Nachrichten auf Pastebin.')

    else:
        message_logs.append(f"[{message.author.name}] {message.content}")

def upload_to_pastebin(text):
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': text
    }

    response = requests.post('https://pastebin.com/api/api_post.php', data=data)

    if response.status_code == 200:
        return response.text
    else:
        return None

client.run(TOKEN)
