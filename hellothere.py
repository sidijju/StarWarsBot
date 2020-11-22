# bot.py
import os
import random
import asyncio

import discord
from discord.ext import commands

from utilities import *

bot = commands.Bot(command_prefix='$')

responses = read_responses()
aliases = read_character_aliases()
character_quotes = read_character_quotes()

opening_scrolls = {1: ["Turmoil has engulfed the Galactic Republic.",
                       "The taxation of trade routes to outlying star systems is in dispute.",
                       "Hoping to resolve the matter with a blockade of deadly battleships, the greedy Trade Federation has stopped all shipping to the small planet of Naboo.",
                       "While the congress of the Republic endlessly debates this alarming chain of events, the Supreme Chancellor has secretly dispatched two Jedi Knights, the guardians of peace and justice in the galaxy, to settle the conflict . . . "],
                   2: ["There is unrest in the Galactic Senate.",
                       "Several thousand solar systems have declared their intentions to leave the Republic.",
                       "This Separatist movement, under the leadership of the mysterious Count Dooku, has made it difficult for the limited number of Jedi Knights to maintain peace and order in the galaxy.",
                       "Senator Amidala, the former Queen of Naboo, is returning to the Galactic Senate to vote on the critical issue of creating an ARMY OF THE REPUBLIC to assist the overwhelmed Jedi...."],
                   3: ["War! The Republic is crumbling under attacks by the ruthless Sith Lord, Count Dooku.",
                       "There are heroes on both sides.",
                       "Evil is everywhere.",
                       "In a stunning move, the fiendish droid leader, General Grievous, has swept into the Republic capital and kidnapped Chancellor Palpatine, leader of the Galactic Senate.",
                       "As the Separatist Droid Army attempts to flee the besieged capital with their valuable hostage, two Jedi Knights lead a desperate mission to rescue the captive Chancellor..."],
                   4: ["It is a period of civil war.",
                       "Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.",
                       "During the battle, rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet.",
                       "Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy...."],
                   5: ["It is a dark time for the Rebellion.",
                       "Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy.",
                       "Evading the dreaded Imperial Starfleet, a group of freedom fighters led by Luke Skywalker have established a new secret base on the remote ice world of Hoth.",
                       "The evil lord Darth Vader, obsessed with finding young Skywalker, has dispatched thousands of remote probes into the far reaches of space..."],
                   6: ["Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt.",
                       "Little does Luke know that the GALACTIC EMPIRE has secretly begun construction on a new armored space station even more powerful than the first dreaded Death Star.",
                       "When completed, this ultimate weapon will spell certain doom for the small band of rebels struggling to restore freedom to the galaxy..."]}

luke = ["I’ll never turn to the dark side. You’ve failed, your highness. I am a Jedi, like my father before me.",
        "It's not impossible. I used to bullseye womp rats in my T-16 back home, they're not much bigger than two meters."]
qui_gon = ["There’s always a bigger fish.",
           "The ability to speak does not make you intelligent."]
yoda = ["Do. Or do not. There is no try.",
        "When gone am I, the last of the Jedi will you be. The Force runs strong in your family. Pass on what you have learned.",
        "Fear is the path to the Dark Side. Fear leads to anger; anger leads to hate; hate leads to suffering. I sense much fear in you.",
        "Into exile I must go. Failed I have",
        ]
han_solo = ["Never tell me the odds!",
            "I know.",
            "Over my dead body.",
            "Hokey religions and ancient weapons are no match for a good blaster at your side, kid.",
            "You know, sometimes I amaze even myself"]
obi_wan = ["The Force will be with you. Always.",
           "If you define yourself by your power to take life, your desire to dominate, to possess, then you have nothing.",
           "You have become the very thing you swore to destroy",
           "Only a Sith deals in absolutes.",
           "You can’t win, Darth. If you strike me down, I shall become more powerful than you can possibly imagine.",
           "These aren’t the droids you’re looking for.",
           "So uncivilized.",
           "That's...why I'm here",
           "You were right about one thing, Master. The negotiations were short."]
darth_vader = ["I find your lack of faith disturbing.",
               "Just for once, let me look on you with my own eyes.",
               "This is where the fun begins.",
               "He was too dangerous to be kept alive.",
               "Be careful not to *choke* on your aspirations, Director.",
               "LIAR!",
               "If you're not with me, then you're my enemy",
               "Now this is pod-racing!",
               "NOOOOOOOOOOOOOOOOOOOOO",
               "Pray I don't alter it any further.",
               "I don't like sand. It's coarse and rough and irritating and it gets everywhere."]
mace_windu = ["Not yet",
              "He's too dangerous to be kept alive!"]
darth_sidious = ["Now, young Skywalker, you will die.",
                 "Execute Order 66.",
                 "Your arrogance blinds you, Master Yoda. Now you will experience the full power of the Dark Side.",
                 "I have waited a long time for this moment, my little green friend",
                 "Darth Vader will become more powerful than either of us",
                 "No, no, no! YOU WILL DIIEEEE!",
                 "I love democracy",
                 "We will watch your career with great interest"]
princess_leia = ["Why, you stuck-up, half-witted, scruffy-looking nerf herder!",
                 "You came in that thing? You're braver than I thought."]
padme = ["So this is how liberty dies. With thunderous applause.", "You're breaking my heart. You're going down a path I can't follow."]
jar_jar = ["Yousa should follow me now, okeeday?", "Mesa called Jar Jar Binks, mesa your humble servant!"]

allcharacters = [luke, qui_gon, yoda, han_solo, obi_wan, darth_vader, mace_windu, darth_sidious, princess_leia, padme, jar_jar]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "$help" == message.content.lower():
        response = ["$openings <movie number or name (1-6)> ---> opening scroll of specified movie",
                    "$random ---> random quote",
                    "$<character name> ---> random quote from character",
                    "  current characters --> luke, qui gon, yoda, han solo, obi wan, vader, mace windu, sidious, leia, padme, jar jar",
                    "<quote> ---> response (if in database)"]
        for resp in response:
            await message.channel.send(resp)

    elif "alter" in message.content.lower():
        await message.channel.send("Pray I don't alter it any further.")

    elif len(message.content) > 0 and message.content[0] == '$' and "opening" in message.content.lower()[1:]:
        if "1" in message.content.lower()[1:] or "the phantom menace" in message.content.lower()[1:]:
            scrolls = opening_scrolls[1]
        elif "2" in message.content.lower()[1:] or "attack of the clones" in message.content.lower()[1:]:
            scrolls = opening_scrolls[2]
        elif "3" in message.content.lower()[1:] or "revenge of the sith" in message.content.lower()[1:]:
            scrolls = opening_scrolls[3]
        elif "4" in message.content.lower()[1:] or "a new hope" in message.content.lower()[1:]:
            scrolls = opening_scrolls[4]
        elif "5" in message.content.lower()[1:] or "the empire strikes back" in message.content.lower()[1:]:
            scrolls = opening_scrolls[5]
        elif "6" in message.content.lower()[1:] or "return of the jedi" in message.content.lower()[1:]:
            scrolls = opening_scrolls[6]
        else:
            scrolls = []

        for response in scrolls:
            await message.channel.send(response)
            await asyncio.sleep(1)


    elif len(message.content) > 0 and message.content[0] == '$':
        if message.content[1:] == 'random':
            response = random.choice(random.choice(allcharacters))
        else:
            key = message.content.lower()[1:]
            character = aliases[key]
            if character is not None:
                response = random.choice(character_quotes[character])
            else:
                response = "Invalid input"
        await message.channel.send(response)

    elif message.content.lower() in responses:
        for response in responses[message.content.lower()]:
            await message.channel.send(response)
            await asyncio.sleep(1)

bot.run(os.environ['DISCORD_TOKEN'])
