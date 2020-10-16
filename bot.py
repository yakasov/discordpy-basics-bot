"""
Discord bot written in Python.
Tested and working in 3.7.4 and 3.8.0.
Code written to PEP-8 standards.

Requirements:
discord: for bot to run
youtube-dl: for sing_yt() and download()

Author - yakasov
"""

from datetime import date
from time import gmtime, strftime
from asyncio import sleep
from subprocess import Popen
import socket
import random
import os

from discord.ext import tasks
from discord.utils import get
import discord
import audio_functions as music

client = discord.Client()
ADMIN_ID =  # Replace with ID of user who has extra power over bot
BOT_ID =  # Replace with ID of bot itself
# Replace with auto-get feature?
BIRTHDAY_CHANNEL_ID =  # Replace of channel to send birthdays to
PREFIX = '*'


def clear():
    """Clear console when called."""
    os.system('cls')


def get_file(location):
    """Return contents of file at {location}."""
    with open(location, 'r') as file:
        result = file.read()
        file.close()
    return result


def write_file(location, content):
    """Write contents to file at {location}."""
    with open(location, 'w') as file:
        file.write(content)
        file.close()


PRESENCE_DELAY = 4  # Too low a delay will cause Discord to stop updating presence

TODAY = date.today()
TODAY_FORMATTED = TODAY.strftime('%d/%m')
CACHE_TIME = get_file('resources/cache')

# Load commands file into memory on startup
COMMANDS = get_file('resources/commands')
BIRTHDAYS_RAW = get_file('resources/birthdays').split('\n')
BIRTHDAYS = []
for line in BIRTHDAYS_RAW:
    if '#' not in line:
        BIRTHDAYS.append(line.split(" "))
BIRTHDAYS.pop()  # Adds a blank value add the end, I don't know why yet
# Probably because Atom adds a blank line at the end of the file


async def check_birthdays():
    """Check to see if it's someone's birthday! Uses birthday file from resources."""
    bday_channel = client.get_channel(BIRTHDAY_CHANNEL_ID)
    for person in BIRTHDAYS:
        if person[1] == TODAY_FORMATTED:
            if CACHE_TIME != str(TODAY_FORMATTED):
                await bday_channel.send(f'Happy Birthday, {person[0]}! \
({client.get_user(int(person[2])).mention})')
                write_file('resources/cache', TODAY_FORMATTED)


async def get_pfp(message):
    """Get profile picture of user given ID. If no ID, use author."""
    if len(message.content) == 7:
        await message.channel.send(message.author.avatar_url)
    elif 'ANYONE' in message.content.upper():
        await message.channel.send(random.choice(message.guild.members).avatar_url)
    else:
        try:
            user_obj = client.get_user(int(message.content.split(' ')[1]))
            await message.channel.send(user_obj.avatar_url)
        except AttributeError:  # Argument is not a valid ID (but still integer)
            pass
        except ValueError:  # Argument is not an integer
            pass


async def get_all_pfps(message):
    """Sends all profile pictures for everyone in server.
       Only usable by ADMIN_ID.
    """
    if message.author.id == ADMIN_ID:
        for user in message.guild.members:
            await message.channel.send(user.avatar_url)


async def change_nick(message):
    """Change bot nickname for current guild."""
    try:
        await message.guild.get_member(BOT_ID).edit(
            nick=message.content.replace(f'{PREFIX}setnick ', ''))
    except discord.errors.HTTPException:  # Occurs when Discord gets upset with the bot
        await message.channel.send('Nickname must be 32 characters or fewer in length.')


async def change_presence(message):
    """Change bot game presence."""
    await client.change_presence(activity=discord.Game(
        message.content.replace(f'{PREFIX}setstatus ', '')))


async def get_commands(message):
    """Send all commands from commands file using get_file()."""
    await message.channel.send(COMMANDS)


async def restart(message):  # This isn't a great way of restarting the bot
    """Restart bot."""  # But it's the best I could figure out
    if message.author.id == ADMIN_ID:
        Popen('python bot.py')
        raise SystemExit


async def stop(message):
    """Stop bot."""
    if message.author.id == ADMIN_ID:
        raise SystemExit


@ tasks.loop(seconds=PRESENCE_DELAY * 2)
async def rolling_presence():
    """Rotate rich presence through functions below on certain delay."""
    # await functions here
    await sleep(PRESENCE_DELAY)


@ client.event
async def on_ready():
    """Run when bot has connected to Discord successfully."""
    clear()
    print(f'Connected and ready to go!\nCurrent date is {TODAY_FORMATTED}')
    await check_birthdays()
    # await rolling_presence.start()
    # Anything after the above line will NOT get executed


@ client.event
async def on_message(message):
    """Run when a command has been sent in a channel the bot can see."""
    if not message.author.bot:
        print(f'\n{strftime("[%Y-%m-%d %H:%M:%S] ", gmtime())}\
SERVER: {message.guild.name} | CHANNEL: {message.channel}\n{message.author}: {message.content}')

        cmd = message.content.upper()
        #  words = cmd.split(' ')

        responses = {
            # TEXT RESPONSES
            'GOOD BOT': ':)',
            'BAD BOT': f'bad {str(message.author)[:-5]}',

            # OBJECT / ATTRIBUTE RESPONSES
            f'{PREFIX}GETPFP': get_pfp,

            # FUNCTION RESPONSES
            f'{PREFIX}GETALL': get_all_pfps,
            f'{PREFIX}SETNICK': change_nick,
            f'{PREFIX}SETSTATUS': change_presence,
            f'{PREFIX}COMMANDS': get_commands,

            # MUSIC RESPONSES
            f'{PREFIX}JOIN': music.join_author_vc,
            f'{PREFIX}SINGYT': music.sing_yt,
            f'{PREFIX}STOP': music.stop_audio,
            f'{PREFIX}DISCONNECT': music.leave_vc,

            # ADMIN RESPONSES
            f'{PREFIX}RESTART': restart,
            f'{PREFIX}STOPPLS': stop
        }

        for key in responses:
            if f' {key} ' in f' {cmd} ' or f'{PREFIX}{key} ' in f'{cmd} ':
                # Surround key + cmd in spaces in case of it being start or end of message
                # No start space required for prefix commands
                res = responses[key]
                if callable(res):  # If res is callable, execute as a function and don't send
                    try:
                        await res(message, client)
                    except TypeError:  # This is a dumb workaround
                        await res(message)
                else:
                    try:
                        await message.channel.send(res)
                    except discord.errors.HTTPException:
                        await message.channel.send(
                            'Error sending message back - maybe it was too long?')
                break


token = get_file('resources/token.discord')
client.run(token)
