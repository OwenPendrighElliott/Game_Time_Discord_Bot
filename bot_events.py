import discord
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import os
import bot_settings

bs = bot_settings.BotSettings()

VOLUME = bs.volume
CHNL_SND_DICT = bs.chnl_snd_dict
STALK_EXCLUDE = bs.stalk_exclude


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_snd_dict = CHNL_SND_DICT
        self.stalking_exclude = STALK_EXCLUDE
        self.volume = VOLUME

    # when a user moves channel the bot follows them to play a greeting sound
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(f"{member} was in {before.channel}")
        print(f"{member} is now in {after.channel}")

        # make sure the bot doesnt trigger this
        if member.bot or after.channel == None:
            return

        # get the list of sounds for that channel
        if str(after.channel) in self.channel_snd_dict:
            chnl_snds = self.channel_snd_dict[str(after.channel)]
            # pick a random sound from the list
            snd = random.choice(chnl_snds)
        else:
            return

        # if the person is new to the server always play otherwise play if that are moving to a non excluded channel
        if (
            before.channel == None
            or (
                after.channel != None
                and str(after.channel) not in self.stalking_exclude
            )
        ) and str(before.channel) != str(after.channel):
            # get bot ready for voice
            voice = get(self.bot.voice_clients, guild=member.guild)
            channel = after.channel

            # if bot is doing something else stop it to avoid funny business
            if voice and voice.is_playing():
                voice.stop()

            # if bot is connected then move otherwise connect
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            # play the sound file located in the sounds directory
            voice.play(discord.FFmpegPCMAudio(os.path.join("sounds", snd)))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = self.volume


async def setup(bot):
    # add misc commands cog
    await bot.add_cog(BotEvents(bot))
