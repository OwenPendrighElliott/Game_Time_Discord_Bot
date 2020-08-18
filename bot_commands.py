import discord
from discord.ext import commands
import random 
import asyncio
from PIL import Image, ImageOps, ImageEnhance

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
    async def fry(self, ctx, scale=2):
        print("Downloading image")
        # download the attachment
        disc_img = ctx.message.attachments[0]
        await disc_img.save("attachment.png")

        print("Lowering image into the fryer")
        # open the image and fry it
        img = Image.open('attachment.png')
        img = img.convert('RGB')
        red_chnl = img.split()[0] #(R,G,B)
        red_chnl = ImageEnhance.Contrast(red_chnl).enhance(2)
        red_chnl = ImageEnhance.Brightness(red_chnl).enhance(2)
        red_chnl = ImageOps.colorize(red_chnl, (230, 0, 10), (255, 255, 15))
        img = Image.blend(img, red_chnl, 0.95)
        img = ImageEnhance.Sharpness(img).enhance(150)
        orig_size = img.size

        print("Losing pixels")
        res_factor = scale
        img = img.resize((int(orig_size[0]/res_factor), int(orig_size[1]/res_factor)), resample=Image.BOX)
        img = img.resize(orig_size, resample=Image.NEAREST)
        img.save('attachment.png')

        print("Sending image")
        # send it back
        with open('attachment.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)