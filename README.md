# discordpy-basics-bot
#### a basic discordpy rewrite bot you could probably get away with using

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


## Additional Configuration
The bot can be configured to execute functions on a loop. In order to use this function, uncomment line 153 'await rolling_presence.start()'
The function name can be changed, it's an old name I need to update
The functions you want to loop can be placed in the rolling_presence() function at line 141.
Make sure to await them!

In order to add new commands, add the command to the responses dictionary (line 167).
The key is the command to be input, and the value is the function to call OR the text to directly reply with.

For ease of use, you can use the following functions in your code:
* clear() - will clear the console when used.
* get_file(location) - will return the contents of a file at a given location. The location should include the file name
  eg get_file('C:\files\lyrics.txt')
* write_file(location, contents) - will replace the contents of a file at location with contents.


## Commands
All commands below can be found at resources/commands.

Command | Function
------- | --------
Good Bot, Bad Bot | (no prefix required) test and see
GETPFP [user-id, anyone] | get the profile picture of the given user ID. Anyone will pick randomly
SETNICK [nickname] | set the bot's nickname
SETSTATUS [status] | set the bot's status
JOIN | join your voice channel
SINGYT [url] | play audio from a YouTube URL
STOP | stop playing audio
DISCONNECT | leave the voice channel

Additionally, there are commands that only the user specified with ADMIN_ID can use:

Command | Function
------- | --------
GETALL | will send the profile picture of everyone in the server to the channel the command was used in
RESTART | restart the bot - can be used to test new code
STOP | stop the bot
