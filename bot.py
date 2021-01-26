token = "ODAxOTAxMjQyNDI2NzIwMzA4.YAnaug.hwyfnFkQ6y02Xuf63Vy-kOm3-q8"
db = {}
import discord
import os
import requests
import json
import random
# from replit import db
# from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    db["encouragements"].append(encouraging_message)
    # encouragements.append(encouraging_message)
    # db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
@client.event
async def delete_encouragment(index, message):
    try: 
        db['encouragements'].pop(db['encouragements'].index(index))
        await  message.channel.send(index + ' is succesfully deleted!')
    except :
        await message.channel.send('Not found')


#  encouragements = db["encouragements"]
#   if len(encouragements) > index:
#     del encouragements[index]
#     db["encouragements"] = encouragements

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
    if "encouragements" in db.keys():
        options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        try:
            index = (msg.split("$del ",1)[1])
            await delete_encouragment(index, message)
        except :
            await message.channel.send

        
        encouragements = []
        if "encouragements" in db.keys():
            index = (msg.split("$del ",1)[1])
            await delete_encouragment(index, message)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        # encouragements = []
        try:
            await message.channel.send(db["encouragements"])
        except :
            await message.channel.send('The list is empty rn'+'[]')
        
        # if "encouragements" in db.keys():
        #     encouragements = db["encouragements"]
        # await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]
        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")
    
# if 

# keep_alive()
client.run(token)