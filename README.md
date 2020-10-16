# discordpy-basics-bot
a basic discordpy rewrite bot you could probably get away with using

This is not updated, only fixed if required.
Feel free to use or adapt in any way, I don't mind

## TO USE
Make sure you have discord and youtube-dl installed. If you don't want to use YouTube functions, you can cut out audio_functions.py and all references to it / music in bot.py.

Open bot.py in a text editor and make the following changes:
* ADMIN_ID = [your Discord ID]
* BOT_ID = [the ID of the Discord bot itself]
* BIRTHDAY_CHANNEL_ID = [ID of channel to post Happy Birthday messages into]
  * If you don't want to use the birthday function, comment out line 152 'await check_birthdays()'

**You will also need to add your bot secret to token.discord in the resources folder!**
