import discord
from discord.ext import commands
import random 
import asyncio
from PIL import Image, ImageOps, ImageEnhance
import os
import sys
from collections import deque
from itertools import combinations

# letters and number modules that are used in a separate project of mine
# https://github.com/OwenPendrighElliott/countdown_solver
import letters
import nums

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drop_locs = ["Dam", "Military", "Airport", "Superstore", 
                "Storage", "Boneyard", "Train Station", "Hospital", 
                "Downtown", "Port", "Gulag", "Farm", 
                "TV Station", "Stadium", "Lumberyard", "Quarry"]

    @commands.command(pass_context=True, aliases=['d'])
    async def drop(self, ctx) -> None:
        '''
        Chooses a drop location for WarZone
        '''
        # pick a location and send it back to chat
        loc = random.choice(self.drop_locs)
        await ctx.send(f"Drop at {loc}")

    # toss a coin
    @commands.command(pass_context=True)
    async def toss(self, ctx) -> None:
        '''
        Tosses a coin
        '''
        coin = random.choice(['Heads', 'Tails'])
        await ctx.send(f"{coin}")

    # Bored and want to find a game to play or activity to join? this is the command
    # See what everyone is doing
    # Optionally query a specific person
    @commands.command(pass_context=True, aliases=['g'])
    async def game(self, ctx, prsn=None) -> None:
        '''
        Lists the current activity for everyone in the server
        '''
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        for member in ctx.message.author.guild.members:
            if member.activity:
                game = str(member.activity.name)
            else:
                game = "No game time :("
            if not prsn and not member.bot:
                embed.add_field(name=str(member).split('#')[0], 
                                value=game,
                                inline=False)
            elif str(member).split('#')[0] == prsn and not member.bot:
                embed.add_field(name=str(member).split('#')[0], 
                                value=game,
                                inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['deep_fry'])
    async def fry(self, ctx, res_factor1=4: int, res_factor2=5: int) -> None:
        '''
        deepfry an image included in the message
        '''
        print("Downloading image")
        # download the attachment
        disc_img = ctx.message.attachments[0]
        await disc_img.save("attachment.png")

        print("Lowering image into the fryer")
        # open the image and fry it
        img = Image.open('attachment.png')
        img = img.convert('RGB')
        orig_size = img.size

        print("Losing pixels")
        img = img.resize((int(orig_size[0]/res_factor1), int(orig_size[1]/res_factor1)), resample=Image.BILINEAR)
        img = ImageEnhance.Sharpness(img).enhance(15)
        img = img.resize(orig_size, resample=Image.BILINEAR)
        img = img.convert('RGB')
        converter = ImageEnhance.Color(img)
        img = converter.enhance(30)
        img = ImageEnhance.Sharpness(img).enhance(30)
        img.save('attachment.png')

        print("Sending image")
        # send it back
        with open('attachment.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command(pass_context=True)
    async def shuffle(self, ctx) -> None:
        '''
        Move all users to random channels
        '''
        possib_chnls = [channel for channel in ctx.message.author.guild.channels if type(channel) == discord.VoiceChannel]
        for member in ctx.message.author.guild.members:
            if member.bot == True:
                continue
            try:
                chnl = random.choice(possib_chnls)
                await member.move_to(chnl)
                print(f"Moving {member.name} to {chnl}")
            except Exception:
                print(f"{member.name} can't move, probably not online")
    
    @commands.command(pass_context=True, aliases=['itg', 'gulag'])
    async def inthegulag(self, ctx, name: str) -> None:
        '''
        Send the specified user to the gulag
        '''
        gulag = None
        for channel in ctx.message.author.guild.channels:
            if channel.name == "⛓ the-gulag ⛓" or channel.name == "the-gulag":
                gulag = channel

        for member in ctx.message.author.guild.members:
            if member.name.lower() != name.lower():
                continue
            try:
                await member.move_to(gulag)
                print(f"Moving {member.name} to {gulag}")
            except Exception:
                print(f"{member.name} can't move to the gulag")

    @commands.command(pass_context=True)
    async def numbers(self, ctx, numbers: str, target: int) -> None:
        '''
        Find the optimal solution for a game of numbers (countdown)
        '''
        ns = [int(n) for n in numbers.split('-')]
        game = nums.numbers_game(target, ns, True)
        sol = game.solve()
        
        sol_str = ""
        for a, op, b, r in sol:
            sol_str += f"{op.capitalize()} {a} and {b} to get {r}\n"
        await ctx.send(sol_str)

    @commands.command(pass_context=True)
    async def letters(self, ctx, ls: str) -> None:
        '''
        Find the optimal solution for a game of letters (countdown)
        '''
        if len(ls) > 9:
            await ctx.send(f'Too many letters!')
            return None

        game = letters.letters_game(ls)
        sol = game.solve()
        await ctx.send(f'The best word is "{sol}" and has a length of {len(sol)}')

    @commands.command(pass_context=True)
    async def update(self, ctx, branch="master": str) -> None:
        '''
        Update the bot from the specified branch

        Useful for testing and rebooting if something funny happens
        '''
        await ctx.send(f"Updating myself from branch {branch}")
        if branch == "master":
            os.system("bash bot_update.sh")
        elif branch == "dev":
            os.system("bash bot_update_dev.sh")
        await ctx.send("Updated!")
