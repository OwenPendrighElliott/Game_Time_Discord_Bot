import discord
import os
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
import random
import youtube_dl
import time
import asyncio

# import files with cogs
import bot_commands
import bot_audio
import bot_events
import bot_settings

# load token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', case_insensitive=True)

bs = bot_settings.BotSettings()

VOLUME = bs.volume
CHNL_SND_DICT = bs.chnl_snd_dict
STALK_EXCLUDE = bs.stalk_exclude

# make way for custom help command
bot.remove_command('help')
# custom help command
@bot.command(pass_context=True, aliases=['h'])
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='help')
    embed.add_field(name='!play_file, alias=[!pf]', 
                    value='Play the file specified after the command, see available files with !ls',
                    inline=False)
    embed.add_field(name='!list_sounds, alias=[!ls]', 
                    value='Also !ls, lists available sounds',
                    inline=False)
    embed.add_field(name='!play, alias=[!p]', 
                    value='Plays the specified youtube link',
                    inline=False)
    embed.add_field(name='!stop, alias=[!s]', 
                    value='Stops all bot voice activity',
                    inline=False)
    embed.add_field(name='!drop, alias=[!d]', 
                    value='Picks a random drop location from COD Warzone',
                    inline=False)
    embed.add_field(name='!toss', 
                    value='Toss a coin',
                    inline=False)
    embed.add_field(name='!game, alias=[!g]', 
                    value='Show what the activites of everyone, optionally query a specific person',
                    inline=False)
    embed.add_field(name='!fry, alias=[!deep_fry]', 
                    value='Use in a message with an image and the bot will return a deep fried verison',
                    inline=False)
    embed.add_field(name='!shuffle', 
                    value='Move all online members to random channels',
                    inline=False)
    embed.add_field(name='!inthegulag, alias=[!itg, !gulag]', 
                    value='Move a specified person to the gulag',
                    inline=False)
    embed.add_field(name='!letters', 
                    value='Find the longest word from the specified letters',
                    inline=False)
    embed.add_field(name='!numbers', 
                    value='Using the hyphen separated list of numbers reach the goal number. If true is added then do a trickshot!',
                    inline=False)
    embed.add_field(name='!faces', 
                    value='Extracts all faces from a photo',
                    inline=False)
    await ctx.send(embed=embed)

# notify that bot is running
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@tasks.loop(seconds=5)
async def schedule_func():
    for guild in bot.guilds:
        try:
            channel = discord.utils.get(guild.text_channels, name="bot_cmds")
        except:
            continue
        print("---------------------------------------------")
        print(guild)
        print(channel)
        try:
            await channel.send("TESTING")
        except:
            continue

    # for guild in bot.guilds:
    #     channel = get(guild.channels, name='bot_cmds', type=discord.ChannelType.text)
    #     await bot.send_message(channel, "TEST")

# add misc commands cog
bot.add_cog(bot_commands.BotCommands(bot))

# add audio commands cog
bot.add_cog(bot_audio.BotAudio(bot))

# add events cog
bot.add_cog(bot_events.BotEvents(bot, CHNL_SND_DICT, STALK_EXCLUDE, VOLUME))

# start scheduled function
schedule_func.start()

# run the bot
bot.run(TOKEN)
