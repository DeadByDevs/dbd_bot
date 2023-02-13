import discord

# dotenv import
import os
from dotenv import load_dotenv

# load dotenv 
load_dotenv() 

# import token from .env
token = os.getenv("bot_token")

# discord bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# @client.command()
# async def embed(ctx):
#     embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
#     await ctx.send(embed=embed)
       
    if message.content.startswith('!ping'):
        await message.channel.send('pong')
         
    if message.content.startswith('!cursed'):
        await message.channel.send('the box, you opened it, you fool, you opened the box and now you must pay the price for your foolishness and ignorance and stupidity')
        
    if message.content.startswith('!yassin'):
        await message.channel.send('@Ilyn moi le grand myers je sais que tu vas craquer et t acheter un nouveau mac avant la fin de la semaine')
        
client.run(token)
