# bot.py
import os
import random
import asyncio
import dotenv
import re

import discord
from discord import app_commands

from utilities import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

allcharacters = ["luke", "quigon", "yoda", "hansolo", "obiwan", "darthvader", "macewindu", "darthsidious", "leia", "padme", "jarjar", "hondo", "c3po"]

responses = read_responses()
character_quotes = read_character_quotes(allcharacters)
opening_scrolls = read_scrolls()
class StarWarsBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.read_msg = intents.message_content

    async def on_ready(self):
        await tree.sync()
        print(f'{self.user.name} has connected to Discord')
        print(f'Currently connected to {len(self.guilds)} servers')

    async def on_message(self, message):
        if self.read_msg:
            msg = message.content.lower()
            channel = message.channel

            if message.author == self.user:
                return

            elif "alter" in msg:
                await channel.send("Pray I don't alter it any further.")        

            elif msg in responses:
                for response in responses[msg]:
                    await channel.send(response)
                    await asyncio.sleep(1)

bot = StarWarsBot()
tree = app_commands.CommandTree(bot)

@tree.command(name = "random", description = "print a random quote from a random Star Wars character")
async def random_quote(interaction: discord.Interaction):
    response = random.choice(character_quotes[random.choice(allcharacters)])
    await interaction.response.send_message(response)

@tree.command(name = "random-character", description = "print a random quote from chosen Star Wars character")
@app_commands.choices(name=[app_commands.Choice(name=allcharacters[i], value=allcharacters[i]) for i in range(len(allcharacters))])
async def random_character_quote(interaction: discord.Interaction, name: app_commands.Choice[str]):
    response = random.choice(character_quotes[name.value])
    await interaction.response.send_message(response)

@tree.command(name = "openings", description = "print the opening scroll of the requested Star Wars movie (the three trilogies) based on number")
async def openings(interaction: discord.Interaction, number: app_commands.Range[int, 1, 9]):
    if number in opening_scrolls.keys():
        scrolls = opening_scrolls[number]
        await interaction.response.send_message("Printing scroll")
        for resp in scrolls:
            await interaction.followup.send(resp)
            await asyncio.sleep(1)

@tree.command(name = "openings-name", description = "print the opening scroll of the requested Star Wars movie (the three trilogies) based on name")
@app_commands.choices(name=[
        app_commands.Choice(name="The Phantom Menace", value='1'),
        app_commands.Choice(name="Attack of the Clones", value='2'),
        app_commands.Choice(name="Revenge of the Sith", value='3'),
        app_commands.Choice(name="A New Hope", value='4'),
        app_commands.Choice(name="The Empire Strikes Back", value='5'),
        app_commands.Choice(name="Return of the Jedi", value='6'),
        app_commands.Choice(name="The Force Awakens", value='7'),
        app_commands.Choice(name="The Last Jedi", value='8'),
        app_commands.Choice(name="The Rise of Skywalker", value='9')
        ])
async def openings_name(interaction: discord.Interaction, name: app_commands.Choice[str]):
    key = int(name.value)
    if key in opening_scrolls.keys():
        scrolls = opening_scrolls[key]
        await interaction.response.send_message("Printing scroll")
        for resp in scrolls:
            await interaction.followup.send(resp)
            await asyncio.sleep(1)

bot.run(os.environ.get('DISCORD_TOKEN'))
