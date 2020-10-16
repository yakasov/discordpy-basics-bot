"""
All 'singing' functions ie downloading mp3s from YouTube and streaming them.
"""

import os
import discord
from discord import FFmpegPCMAudio
from discord.utils import get
from youtube_dl import YoutubeDL
import youtube_dl


async def join_author_vc(message, client):
    """Join voice channel of message author."""
    try:
        await message.author.voice.channel.connect()
    except AttributeError:
        await message.channel.send('Author not in a voice channel!')
    except discord.errors.ClientException:
        pass


async def sing_yt(message, client):
    """Played audio from YouTube given URL."""
    ydl_options = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'extractaudio': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '96',  # Highest bitrate Discord supports
        }],
    }
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    link = message.content.replace(f"{PREFIX}singyt ", "")

    try:
        channel_voice_stream = get(client.voice_clients, guild=message.guild)
        if not channel_voice_stream.is_playing():
            with YoutubeDL(ydl_options) as ydl:
                info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
            channel_voice_stream.play(FFmpegPCMAudio(url, **ffmpeg_options))
            channel_voice_stream.is_playing()
    except (AttributeError, discord.errors.ClientException) as ex:
        print(ex)
        await message.channel.send('Make sure the bot is connected to a voice channel first!')
    except (youtube_dl.utils.ExtractorError, youtube_dl.utils.DownloadError):
        await message.channel.send('URL not recognised.')


async def stop_audio(message, client):
    """Stop playing audio."""
    channel_voice_stream = get(client.voice_clients)
    try:
        channel_voice_stream.stop()
    except (discord.errors.ClientException, AttributeError):
        pass


async def leave_vc(message, client):
    """Leave current voice channel."""
    try:
        await message.guild.voice_client.disconnect()
    except AttributeError:
        pass
