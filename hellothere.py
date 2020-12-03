# bot.py
import os
import random
import asyncio

import discord
from discord.ext import commands

from utilities import *

bot = commands.Bot(command_prefix='$')

allcharacters = ["luke", "quigon", "yoda", "hansolo", "obiwan", "darthvader", "macewindu", "darthsidious", "leia", "padme", "jarjar", "hondo", "c3po"]

responses = read_responses()
aliases = read_character_aliases()
character_quotes = read_character_quotes(allcharacters)
opening_scrolls = read_scrolls()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    print(f'Currently connected to {len(bot.guilds)} servers')

@bot.event
async def on_message(message):
    msg = message.content.lower()
    channel = message.channel

    if msg == "vote":
        await channel.send("I vote in affirmation of the resolution")
    if "start a warsaw vote" in msg:
        await channel.send("I initiate a vote to warsaw the aforementioned person")

    if message.author == bot.user:
        return

    if "$help" == msg:
        response = ["$openings <movie number or name (1-6)> ---> opening scroll of specified movie",
                    "$random ---> random quote",
                    "$<character name> ---> random quote from character",
                    "  current characters --> luke, qui gon, yoda, han solo, obi wan, vader, mace windu, sidious, leia, padme, jar jar, c-3po, and hondo ohnaka",
                    "<quote> ---> response (if in database)"]
        for resp in response:
            await channel.send(resp)

    elif "alter" in msg:
        await channel.send("Pray I don't alter it any further.")

    elif len(msg) > 0 and '$openings' in msg:
        request = msg[9:].strip()
        scrolls = []
        if request in opening_scrolls.keys():
            scrolls = opening_scrolls[request]
        for response in scrolls:
            await channel.send(response)
            await asyncio.sleep(1)

    elif len(msg) > 0 and msg[0] == '$':
        if msg[1:] == 'random':
            response = random.choice(character_quotes[random.choice(allcharacters)])
        else:
            key = msg[1:]
            if key in aliases.keys():
                response = random.choice(character_quotes[aliases[key]])
            else:
                response = "Invalid input. Use $help for a list of valid commands."
        await channel.send(response)

    elif msg in responses:
        for response in responses[msg]:
            await channel.send(response)
            await asyncio.sleep(1)

bot.run(os.environ['DISCORD_TOKEN'])
