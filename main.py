import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = [
  'sad',
  'unhappy',
  'depressed',
  'depressing',
  'angry',
  'mad',
  'anxious',
  'anxiety',
  'miserable',
  'mess',
]

starter_encouragements = [
  'Chear up', 'Hang in there', 'You are a great person'
]

convo = ['good', 'better', 'alright', 'okay']

if 'responding' not in db.keys():
  db['responding'] = True


def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return (quote)


def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]


def delete_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$Hi'):
    await message.channel.send('Hi there! How can I help?')

  if message.content.startswith('$Inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options = options + list(db['encouragements'])

      if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(options))

  if message.content.startswith('$Add'):
    encouraging_message = message.content.split('$Add ', 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('New encouraging message added')

  if message.content.startswith('$Del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = message.content.split('$Del ', 1)[1]
      delete_encouragements(index)
      encouragements = db['encouragements']
      await message.channel.send(encouragements)

  if any(word in message.content for word in convo):
    await message.channel.send('Glad I could help :)')

  if message.content.startswith('$List'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if message.content.startswith('responding'):
    value = message.content.split('responding ', 1)[1]

    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on')
    else:
      db['responding'] = False
      await message.channel.send('Responding is off')


keep_alive()
client.run(os.environ['TOKEN'])
