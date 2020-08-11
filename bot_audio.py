import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl

class BotAudio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # play a local file
    @commands.command(pass_context=True, aliases=['pf'])
    async def play_file(self, ctx, snd, volume=0.2):
        # if the requested file exists them play it
        f = os.path.join('sounds', snd)
        snd_there = os.path.isfile(f)
        if not snd_there:
            await ctx.send(f"Never heard of {snd}, soz")
            return

        # got bot setup for voice
        voice = get(self.bot.voice_clients, guild=ctx.guild)
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

    @commands.command(pass_context=True, aliases=['ls'])
    async def list_sounds(self, ctx):
        sounds = os.path.join('sounds')
        await ctx.send('The following sounds are in the sounds folder:')
        files = ""
        for file in os.listdir(sounds):
            if file.endswith(".mp3") or file.endswith(".wav"):
                files += file
                files += '\n'
        await ctx.send(files)
       
    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str, volume=0.2):
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

        voice = get(self.bot.voice_clients, guild=ctx.guild)
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
    @commands.command(pass_context=True, aliases=['s'])
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        
        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Bot has left {channel}")
            await ctx.send(f"Leaving your channel {str(ctx.message.author).split('#')[0]}")
        else:
            print(f"Bot was told to leave but isn't in a channel")
            await ctx.send(f"I'm not in a channel")
