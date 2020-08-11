import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import random
import youtube_dl

# import files with cogs
import bot_commands
import bot_audio
import bot_events

# ---- START: Edit for your own discord ----

# load token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# The name of the bot, used to stop the bot from triggering channel movement events
BOT_NAME = "Game Time"

# Volume for sounds when the bot greets members of channels 
VOLUME = 0.2

# maps channel names to sounds
# customise according to your discord
# Bot lives in 2 discords so some double ups because I'm lazy
CHNL_SND_DICT = {'General' : ['universal.mp3'],
                 'game-time' : ['hello_gamer.mp3', 'frickin_gaming.mp3', 'gaming_setup.mp3'], 
                 'kript-skiddies' : ['HACKERMAN.mp3'], 
                 'speed-run' : ['sonic.mp3']*99+['sanic.mp3'], 
                 'the-gulag' : ['inthegulag.mp3'],
                 '🎮 game-time 🎮' : ['hello_gamer.mp3', 'frickin_gaming.mp3', 'gaming_setup.mp3'], 
                 '💻 kript-skiddies 💻' : ['HACKERMAN.mp3'], 
                 '⏩ speed-run ⏩' : ['sonic.mp3']*99+['sanic.mp3'], 
                 '⛓ the-gulag ⛓' : ['inthegulag.mp3']}

# List of channel that the bot won't follow people into, bot will still join these if someone has not moved from another channel
STALK_EXCLUDE = ['General']

# ---- END: Edit for your own discord ----

# make way for custom help command
bot.remove_command('help')
# custom help command
@bot.command(pass_context=True, aliases=['h'])
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='help')
    embed.add_field(name='!play_file', 
                    value='Play the file specified after the command, see available files with !ls',
                    inline=False)
    embed.add_field(name='!list_sounds', 
                    value='Also !ls, lists available sounds',
                    inline=False)
    embed.add_field(name='!play', 
                    value='Plays the specified youtube link',
                    inline=False)
    embed.add_field(name='!stop', 
                    value='Stops all bot voice activity',
                    inline=False)
    embed.add_field(name='!drop', 
                    value='Picks a random drop location from COD Warzone',
                    inline=False)
    embed.add_field(name='!toss', 
                    value='Toss a coin',
                    inline=False)
    embed.add_field(name='!game', 
                    value='Show what the activites of everyone, optionally query a specific person',
                    inline=False)
    await ctx.send(embed=embed)

# notify that bot is running
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# add misc commands cog
bot.add_cog(bot_commands.BotCommands(bot))

# add audio commands cog
bot.add_cog(bot_audio.BotAudio(bot))

# add events cog
bot.add_cog(bot_events.BotEvents(bot, CHNL_SND_DICT, STALK_EXCLUDE, BOT_NAME, VOLUME))

# run the bot
bot.run(TOKEN)
