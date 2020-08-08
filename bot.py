import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import random
import youtube_dl

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
channel_snd_dict = {'General' : ['universal.mp3'],
                    'game-time' : ['hello_gamer.mp3', 'frickin_gaming.mp3', 'gaming_setup.mp3'], 
                    'kript-skiddies' : ['HACKERMAN.mp3'], 
                    'speed-run' : ['sonic.mp3']*99+['sanic.mp3'], 
                    'the-gulag' : ['inthegulag.mp3']}

# List of channel that the bot won't follow people into, bot will still join these if someone has not moved from another channel
stalking_exclude = ['General']

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# when a user moves channel the bot follows them to play a greeting sound
@bot.event
async def on_voice_state_update(member, before, after):
    print(f"{member} was in {before.channel}")
    print(f"{member} is now in {after.channel}")

    # make sure the bot doesnt trigger this
    if str(member).split('#')[0] == BOT_NAME or after.channel == None:
        return
    
    # get the list of sounds for that channel
    chnl_snds = channel_snd_dict[str(after.channel)]
    # pick a random sound from the list
    snd = random.choice(chnl_snds)

    # get bot ready for voice
    voice = get(bot.voice_clients, guild=member.guild)
    channel = after.channel

    # if bot is doing something else so it and disconnect to avoid funny business
    if voice and voice.is_playing():
        voice.stop()
        await voice.disconnect()

    # if the person is new to the server always play otherwise play if that are moving to a non excluded channel
    if before.channel == None or (after.channel != None and str(after.channel) not in stalking_exclude):
        # if bot is connected then move otherwise connect
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        # play the sound file located in the sounds directory
        voice.play(discord.FFmpegPCMAudio(os.path.join('sounds', snd)))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = VOLUME

# play a local file
@bot.command(pass_context=True, aliases=['pf'])
async def play_file(ctx, snd, volume=0.2):
    # if the requested file exists them play it
    f = os.path.join('sounds', snd)
    snd_there = os.path.isfile(f)
    if not snd_there:
        await ctx.send(f"Never heard of {snd}, soz")
        return

    # got bot setup for voice
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    # if bot is doing something else stop it
    if voice and voice.is_playing():
        voice.stop()
        await voice.disconnect()
    
    # if bot is already connected the move otherwise initialise a connection
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    print(f"The bot is connected to {channel}")
    # play the sound
    voice.play(discord.FFmpegPCMAudio(os.path.join('sounds', snd)))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = volume

    await ctx.send(f"Playing {snd} for you {str(ctx.message.author).split('#')[0]}!")

@bot.command(pass_context=True, aliases=['ls'])
async def list_sounds(ctx):
    sounds = os.path.join('sounds')
    await ctx.send('The following sounds are in the sounds folder:')
    files = ""
    for file in os.listdir(sounds):
        if file.endswith(".mp3") or file.endswith(".wav"):
            files += file
            files += '\n'
    await ctx.send(files)

@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str, volume=0.2):
    # if the tmp file is already there then delete it
    f = os.path.join('yt_tmp.mp3')
    snd_there = os.path.isfile(f)
    try:
        if snd_there:
            os.remove(f)
            print("Removed old mp3")
    except PermissionError:
        print("Can't delete song because it is being played")
        await ctx.send("Error deleting last song, maybe try killing me with '!stop'")
    
    await ctx.send("Preparing audio")

    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    
    # yt download options
    ydl_opts = {'format' : 'bestaudio/best',
                'postprocessors' : [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
                }

    # Download the file
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading file')
        try:
            ydl.download([url])
        except:
            await ctx.send("Provided link is not a valid YT link")
    
    # rename the downloaded file
    for file in os.listdir('./'):
        if file.endswith(".mp3"):
            os.rename(file, 'yt_tmp.mp3')

    if voice and voice.is_playing():
        voice.stop()
        await voice.disconnect()
        
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    print(f"The bot is connected to {channel}")

    # play the file
    voice.play(discord.FFmpegPCMAudio(f))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = volume

    await ctx.send(f"Playing your link {str(ctx.message.author).split('#')[0]}!")

# kill all voice activity for the bot
@bot.command(pass_context=True, aliases=['s'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has left {channel}")
        await ctx.send(f"Leaving your channel {str(ctx.message.author).split('#')[0]}")
    else:
        print(f"Bot was told to leave but isn't in a channel")
        await ctx.send(f"I'm not in a channel")

# Helps you choose where to drop in COD Warzone
drop_locs = ["Dam", "Military", "Airport", "Superstore", 
                "Storage", "Boneyard", "Train Station", "Hospital", 
                "Downtown", "Port", "Gulag", "Farm", 
                "TV Station", "Stadium", "Lumberyard", "Quarry"]

@bot.command(pass_context=True, aliases=['d'])
async def drop(ctx):
    # pick a location and send it back to chat
    loc = random.choice(drop_locs)
    await ctx.send(f"Drop at {loc}")

# run the bot
bot.run(TOKEN)
