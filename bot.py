import discord
import os
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

# load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class GameTimeBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("bot_commands")
        await self.load_extension("bot_audio")
        await self.load_extension("bot_events")


bot = GameTimeBot(
    command_prefix="!", case_insensitive=True, intents=discord.Intents.all()
)

# make way for custom help command
bot.remove_command("help")


# custom help command
@bot.command(pass_context=True, aliases=["h"])
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name="help")
    embed.add_field(
        name="!play_file, alias=[!pf]",
        value="Play the file specified after the command, see available files with !ls",
        inline=False,
    )
    embed.add_field(
        name="!list_sounds, alias=[!ls]",
        value="Also !ls, lists available sounds",
        inline=False,
    )
    embed.add_field(
        name="!play, alias=[!p]", value="Plays the specified youtube link", inline=False
    )
    embed.add_field(
        name="!stop, alias=[!s]", value="Stops all bot voice activity", inline=False
    )
    embed.add_field(
        name="!drop, alias=[!d]",
        value="Picks a random drop location from COD Warzone",
        inline=False,
    )
    embed.add_field(name="!toss", value="Toss a coin", inline=False)
    embed.add_field(
        name="!game, alias=[!g]",
        value="Show what the activites of everyone, optionally query a specific person",
        inline=False,
    )
    embed.add_field(
        name="!fry, alias=[!deep_fry]",
        value="Use in a message with an image and the bot will return a deep fried verison",
        inline=False,
    )
    embed.add_field(
        name="!shuffle",
        value="Move all online members to random channels",
        inline=False,
    )
    embed.add_field(
        name="!inthegulag, alias=[!itg, !gulag]",
        value="Move a specified person to the gulag",
        inline=False,
    )
    embed.add_field(
        name="!letters",
        value="Find the longest word from the specified letters",
        inline=False,
    )
    embed.add_field(
        name="!numbers",
        value="Using the hyphen separated list of numbers reach the goal number. If true is added then do a trickshot!",
        inline=False,
    )
    embed.add_field(
        name="!faces", value="Extracts all faces from a photo", inline=False
    )
    await ctx.send(embed=embed)


# notify that bot is running
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


# run the bot
bot.run(TOKEN)
