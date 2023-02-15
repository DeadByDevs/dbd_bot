import discord
import sys
import os
import requests
from dotenv import load_dotenv
import numpy as np
import PIL
from PIL import Image
from io import BytesIO


# load dotenv 
load_dotenv() 

# env variables
token = os.getenv("bot_token")
url = os.getenv("api_url")

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

# requests
    randommap = requests.get(url + '/map').json()
    survivor = requests.get(url + '/survivor').json()
    killer = requests.get(url + '/killer').json()
    survivorset = requests.get(url + '/perk/survivor/set').json()
    killerset = requests.get(url + '/perk/killer/set').json()
    survivorone = requests.get(url + '/perk/survivor/single').json()
    killerone = requests.get(url + '/perk/killer/single').json()

    def embedDataSet(dataSet):
        filteredData = ""
        for item in dataSet:
            filteredData += "**" + item["perk_name"] + "**" + ' from ' + item['name'] + "\n" + "\n"
        return discord.Embed(title="Here is your set", description=filteredData)

# take the 4 images and put them in a row 

    def createImageArray(dataReceived):
        imageArray = []
        for element in dataReceived:
            imageArray.append(element["icon_url"])
        return imageArray

    def createImage(urls, output_file):
        # Download the images
        responses = [requests.get(url) for url in urls]

        # Open the images with Pillow
        images = [Image.open(BytesIO(response.content)) for response in responses]

        # Combine the dimensions of the source images
        width = images[0].width + images[1].width
        height = images[2].height + images[3].height

        # Create a new image with the combined dimensions
        result = Image.new('RGB', (width, height))

        # Paste the source images into the new image
        result.paste(im=images[0], box=(0, 0))
        result.paste(im=images[1], box=(images[0].width, 0))
        result.paste(im=images[2], box=(0, images[0].height))
        result.paste(im=images[3], box=(images[2].width, images[1].height))

        # Save the merged image to a file
        result.save(output_file, quality=95)

    def deleteJpgFiles(image):
        os.remove(image)
        
# commands
    if message.content.startswith('!test'):
        await message.channel.send('test')
        
    if message.content.startswith('!ping'):
        await message.channel.send('pong')
    
    if message.content.startswith('!cursed'):
        await message.channel.send('the box, you opened it, you fool, you opened the box and now you must pay the price for your foolishness and ignorance and stupidity')
        
    if message.content.startswith('!help'):
        embed = discord.Embed(title="Here is the list of commands", description="!random map : get random map \n !random survivor : get random survivor \n !random killer : get random killer \n !survivor set : get 4 random survivor perks \n !killer set : get 4 random killer perks \n !survivor one : get 1 random survivor perks \n !killer one : get 1 random killer perks \n", color=0x00ff00)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('!random map'):
        embed = discord.Embed(title=randommap["name"], color=0xffff00)
        mapimage = randommap["maps"][0]
        embed.set_image(url=mapimage['thumbnail'])
        await message.channel.send(embed=embed)
        
    if message.content.startswith('!random survivor'):
        perk = survivorone[0]
        embed = discord.Embed(title=perk['name'], color=0x00ff00)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('!random killer'):
        perk = killerone[0]
        embed = discord.Embed(title=perk['name'], color=0xff0000)
        await message.channel.send(embed=embed)
        
    if message.content.startswith('!survivor set'):
        embed = embedDataSet(survivorset)
        createImage(createImageArray(survivorset), "survivorPerks.jpg")
        file = discord.File("survivorPerks.jpg", filename="survivorPerks.jpg")
        embed.set_image(url="attachment://survivorPerks.jpg")
        await message.channel.send(embed=embed, file=file)
        deleteJpgFiles('survivorPerks.jpg')
        
    if message.content.startswith('!killer set'):
        embed = embedDataSet(killerset)
        createImage(createImageArray(killerset), "killerPerks.jpg")
        file = discord.File("killerPerks.jpg", filename="killerPerks.jpg")
        embed.set_image(url="attachment://killerPerks.jpg")
        await message.channel.send(embed=embed, file=file)
        deleteJpgFiles('killerPerks.jpg')
        
    if message.content.startswith('!survivor one'):
        perk = survivorone[0]
        embed = discord.Embed(title=perk["perk_name"], description=perk['name'], color=0x00ff00)
        embed.set_image(url=perk["icon_url"])
        await message.channel.send(embed=embed)
        
    if message.content.startswith('!killer one'):
        perk = killerone[0]
        embed = discord.Embed(title=perk["perk_name"], description=perk['name'], color=0xff0000)
        embed.set_image(url=perk["icon_url"])
        await message.channel.send(embed=embed)
        
        
client.run(token)
