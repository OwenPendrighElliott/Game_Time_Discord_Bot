import discord
from discord.ext import commands
import random 
import asyncio
from PIL import Image, ImageOps, ImageEnhance
import os
import sys
from collections import deque
from itertools import combinations

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drop_locs = ["Dam", "Military", "Airport", "Superstore", 
                "Storage", "Boneyard", "Train Station", "Hospital", 
                "Downtown", "Port", "Gulag", "Farm", 
                "TV Station", "Stadium", "Lumberyard", "Quarry"]

    @commands.command(pass_context=True, aliases=['d'])
    async def drop(self, ctx):
        # pick a location and send it back to chat
        loc = random.choice(self.drop_locs)
        await ctx.send(f"Drop at {loc}")

    # toss a coin
    @commands.command(pass_context=True)
    async def toss(self, ctx):
        # pick a location and send it back to chat
        coin = random.choice(['Heads', 'Tails'])
        await ctx.send(f"{coin}")

    # Bored and want to find a game to play or activity to join? this is the command
    # See what everyone is doing
    # Optionally query a specific person
    @commands.command(pass_context=True, aliases=['g'])
    async def game(self, ctx, prsn=None):
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
    async def fry(self, ctx, res_factor1=4, res_factor2=5):
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
    async def shuffle(self, ctx):
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
    async def inthegulag(self, ctx, name: str):
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
    async def numbers(self, ctx, numbers: str, target: int):
        nums = [int(n) for n in numbers.split('-')]
        strat = False
        game = numbers_game(target, nums, strat)
        sol = game.solve()
        
        output = ""
        for a, op, b, r in sol:
            output += f"{op.capitalize()} {a} and {b} to get {r}\n"

        await ctx.send(output)


    @commands.command(pass_context=True)
    async def update(self, ctx, branch="master"):
        await ctx.send(f"Updating myself from branch {branch}")
        if branch == "master":
            os.system("bash bot_update.sh")
        elif branch == "dev":
            os.system("bash bot_update_dev.sh")
        await ctx.send("Updated!")



class numbers_game():
    def __init__(self, goal, nums, shortest=False):
        self.goal = goal
        self.nums = nums
        self.ops = [self.add, self.subtract, self.multiply, self.divide]
        self.shortest = shortest

    def add(self, a,b):
        return a+b
    
    def subtract(self, a,b):
        return a-b
    
    def multiply(self, a,b):
        return a*b
    
    # div can not return negative or float numbers
    def divide(self, a,b):
        if a == 0 or b == 0 or a%b != 0:
            raise ValueError("Invalid division for Countdown")
        return int(a/b)
    
    def solve(self):
        # initialise a deque for tracking progress
        Q = deque()
        Q.append((self.nums, []))
        nodes = 0
        while Q:
            ns, path = Q.pop()

            # check goal
            if self.goal in ns:
                print(f"Solution found after expanding {nodes} nodes")
                return path
            
            # if only one number is left then this path has failed
            if len(ns) <= 1:
                continue

            for a, b in combinations(ns, 2):
                # enforce largest first to allow for combinations instead of permutations
                if b > a:
                    a, b = b, a
                for op in self.ops:
                    nodes += 1
                    # calulate new value 
                    try:
                        new_n = op(a, b)
                    except ValueError:
                        continue
                    
                    # if value is negative then we dont need it
                    if new_n < 0:
                        continue

                    # create new list of numbers and new path
                    new_ns = list(ns)
                    new_ns.remove(a)
                    new_ns.remove(b)
                    new_ns.append(new_n)
                    new_path = list(path)
                    new_path.append((a, op.__name__, b, new_n))
                    Q.append((new_ns, new_path))