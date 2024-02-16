# Imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import keyboard
import time
import os
import random
import json
load_dotenv('.env')

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)

# Variables and stuff
connected = False
keys = [
    "esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "~", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "backspace",
    "tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "enter",
    "ctrl", "shift", "alt", "cmd", "windows", "space",
    "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\",
    "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",
    "numlock", "num/", "num*", "num-", "num+", "num0", "num1", "num2", "num3", "num4", "num5", "num6", "num7", "num8", "num9", "num.", "numenter",
    "insert", "home", "pageup", "delete", "end", "pagedown",
    "arrowleft", "arrowright", "arrowup", "arrowdown",
    "volumeup", "volumedown", "mute", "play", "stop", "next", "previous",
    "printscreen", "scrolllock", "pause", "break",
    "apps", "contextmenu", "browserback", "browserforward", "browserrefresh", "browserstop", "browsersearch", "browserfavorites", "browserhome",
    "mail", "media", "calculator", "launchapp1", "launchapp2",
    "sleep", "power", "wake", "monbrightnessup", "monbrightnessdown", "monbrightnessauto",
    "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "f21", "f22", "f23", "f24"
]
customkeys = []
embed = discord.embeds.Embed(title="InputsBot - Discord fuck up your pc", 
                                 description='''**Clarification**\n
                                 This bot will give users with a specific role the ability to send inputs to YOUR pc using YOUR keyboard virtually.\n
                                 **Usage**\n
                                 ;info - Shows this prompt\n
                                 ;cmds - Shows all keys users can use\n
                                 ;customcmds string key bool use_normal_cmds? - Add keys and specify if only to use those\n
                                 ;toggle - Enable/Disable the keyboard inputs (starts as disabled)
                                 ;string key (optional, max 5) int seconds - Send a command to the keyboard''')

# When bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Send a message whenever it joins a server
@bot.event
async def on_guild_join(guild):
    global embed
    news_channel_found = False
    for channel in guild.text_channels:
        if channel.type == discord.ChannelType.news:
            await channel.send(embed=embed)
            news_channel_found = True
            break
    
    if not news_channel_found:
        randChannel = random.choice(guild.text_channels)
        await randChannel.send(embed=embed)

# info command
@bot.command(name='info', help='')
async def info(ctx):
    global embed
    await ctx.send(embed=embed)

# cmds Command
@bot.command(name='cmds')
async def cmds(ctx):
    await ctx.reply(f"Basic: {keys}")
    await ctx.reply(f"Custom: {customkeys}")

# Add custom keys
@bot.command(name='customcmds')
async def customcmds(ctx, customkeylist):
    for key in customkeys:
        customkeys.append(key)
        await ctx.reply(f"Added: {key}")

# Toggle inputs
@bot.command(name='toggle')
async def toggle(ctx):
    global connected
    if connected:
        connected = False
        await ctx.reply("Disabled.")
    else:
        connected = True
        await ctx.reply("Enabled.")

# Send key to keyboard
async def send(ctx, key, time):
    if time == 0:
        keyboard.press_and_release(key)
    else:
        keyboard.press(key)
        time.sleep(time)
        keyboard.release(key)

# Get the key if conditions met
@bot.event
async def on_message(msg):
    if msg.author == bot:
        return
    
    if connected:
        if msg.content.startswith(':'):
            stripped_msg = msg.content[1:2]
            print(stripped_msg)
            for key in keys:
                if stripped_msg == key:
                    # Assures there's a space
                    numbers = msg.content[len(key) +  2:]
                    if numbers.isdigit() and int(numbers) <=  2:
                        print(f"{msg.author}: {stripped_msg} - {numbers}")
                        await send(msg, stripped_msg, int(numbers))
                        break
                    else:
                        print(f"{msg.author}: {stripped_msg} - 0")
                        await send(msg, stripped_msg,  0)
                        break

    await bot.process_commands(msg)

# Activate bot
bot.run(os.getenv('DISCORD_TOKEN'))
# https://discord.com/api/oauth2/authorize?client_id=1207707523549896704&permissions=2048&scope=bot