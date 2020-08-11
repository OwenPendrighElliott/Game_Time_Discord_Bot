import discord
from discord.ext import commands
from discord.utils import get
import random 
import asyncio
import os

class BotEvents(commands.Cog):
    def __init__(self, bot, channel_snd_dict, stalking_exclude, bot_name, volume):
        self.bot = bot
        self.channel_snd_dict = channel_snd_dict
        self.stalking_exclude = stalking_exclude
        self.bot_name = bot_name
        self.volume = volume

    # when a user moves channel the bot follows them to play a greeting sound
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(f"{member} was in {before.channel}")
        print(f"{member} is now in {after.channel}")

        # make sure the bot doesnt trigger this
        if str(member).split('#')[0] == self.bot_name or after.channel == None:
            return
        
        # get the list of sounds for that channel
        chnl_snds = self.channel_snd_dict[str(after.channel)]
        # pick a random sound from the list
        snd = random.choice(chnl_snds)

        # get bot ready for voice
        voice = get(self.bot.voice_clients, guild=member.guild)
        channel = after.channel

        # if bot is doing something else so it and disconnect to avoid funny business
        if voice and voice.is_playing():
            voice.stop()
            await voice.disconnect()

        # if the person is new to the server always play otherwise play if that are moving to a non excluded channel
        if before.channel == None or (after.channel != None and str(after.channel) not in self.stalking_exclude):
            # if bot is connected then move otherwise connect
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            # play the sound file located in the sounds directory
            voice.play(discord.FFmpegPCMAudio(os.path.join('sounds', snd)))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = self.volume

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print(f"{before} was doing {before.activity} but is now doing {after.activity}")
        if not before.activity:
            print(self.bot.guilds)