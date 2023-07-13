from io import BytesIO

import discord
from discord import Intents
from discord.ext import commands

import math

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix='!', intents=intents)


# Event that gets triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


from discord.ext import commands


class Hi(commands.Command):
    """Says hello to the user."""

    def __init__(self, bot):
        super().__init__(name="hi", description="Says hello to the user.")
        self.bot = bot

    async def handle(self, ctx):
        user = ctx.author
        greeting = f"Hi {user.name}!"
        await ctx.send(greeting)


def setup(bot):
    bot.add_command(Hi(bot))


if __name__ == "__main__":
    bot = discord.Client(intents=intents)
    bot=commands()
    setup(bot)
    bot.run()


# Command to make the bot say "Hi"
@bot.command()
async def hi(ctx):
    latency = bot.latency
    await ctx.send(f'Hello')


@bot.command()
async def redroc(ctx):
    await ctx.send('red roc', file=discord.File('roof-piece-one-piece.gif'))


@bot.command()
async def supersaiyan(ctx):
    await ctx.send('SUPER SAIYAN', file=discord.File('SUPER SAiyan.gif.gif'))


@bot.command()
async def mugetsu(ctx):
    file = discord.File('kurosaki-ichigo-aizen.gif')
    await ctx.send("mugetsu", file=file)


@bot.command()
async def fix_latency(ctx):
    # Measure the current latency of the bot
    latency = bot.latency
    await ctx.send(f'Current latency: {latency * 1000:.2f} ms')

    # Implement code optimizations here
    # Example: Optimize database queries, caching, or code logic

    # Measure the updated latency after optimizations
    latency = bot.latency
    await ctx.send(f'Optimized latency: {latency * 1000:.2f} ms')


user_balances = {
    'berries': {},
    'tickets': {}
}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.command()
async def balance(ctx, currency='berries'):
    user = ctx.author
    if user.id in user_balances[currency]:
        balance = user_balances[currency][user.id]
        embed = discord.Embed(title=f'{currency.capitalize()} Balance', color=discord.Color.green())
        embed.add_field(name="User", value=user.name, inline=False)
        embed.add_field(name="Balance", value=f"{balance} {currency}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('You have no balance in that currency.')


@bot.command()
async def earn(ctx, currency='berries'):
    user = ctx.author
    if user.id in user_balances[currency]:
        await ctx.send(f'You have already earned your daily {currency}.')
    else:
        user_balances[currency][user.id] = 100  # Set initial balance to 100
        await ctx.send(f'You earned 100 {currency} for completing a mission!')


# Voting API endpoint and token
VOTING_API_URL = 'https://your-voting-api.com/vote'
VOTING_API_TOKEN = 'your-voting-api-token'


@bot.command()
async def vote(ctx, requests=None):
    user = ctx.author

    # Check if user has already voted
    if user.id in user_balances and 'vote' in user_balances[user.id]:
        await ctx.send('You have already voted.')
        return

    # Make a request to the voting API
    headers = {'Authorization': f'Token {VOTING_API_TOKEN}'}
    response = requests.post(VOTING_API_URL, headers=headers)

    if response.status_code == 200:
        user_balances[user.id] = {
            'coins': user_balances.get(user.id, {}).get('coins', 0) + 100,
            'vote': True
        }
        await ctx.send('Thank you for voting! You received 100 coins.')
    else:
        await ctx.send('Failed to vote. Please try again later.')


@bot.command()
async def thunderclap(ctx):
    await ctx.send('thunderclap', file=discord.File('3DA89429-8752-4EF4-BD16-FB53231ABD3F.gif'))


'''import random
import logging
import requests
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# Dictionaries to store user levels and bounties
user_levels = {}
user_bounties = {}

# Constants for the bounty system
BASE_BOUNTY_INCREMENT = 500
DIMINISHING_FACTOR = 0.8


def increment_bounty(user):
    current_bounty = user_bounties.get(user.id, 0)
    bounty_increment = math.floor(
        BASE_BOUNTY_INCREMENT * DIMINISHING_FACTOR ** (current_bounty / BASE_BOUNTY_INCREMENT))
    user_bounties[user.id] = current_bounty + bounty_increment


def increment_level(user):
    user_levels[user.id] = user_levels.get(user.id, 0) + 1


def generate_bounty_poster(user):
    bounty = user_bounties[user.id]
    username = str(user)
    profile_pic_url = user.avatar_url_as(size=256)

    # Load the One Piece bounty poster template
    poster_template = Image.open('one_piece_bounty_template.png')

    # Resize and paste the user's profile picture onto the poster
    profile_pic_response = requests.get(profile_pic_url)
    profile_pic = Image.open(BytesIO(profile_pic_response.content)).convert('RGBA')
    profile_pic = profile_pic.resize((160, 160))
    poster_template.paste(profile_pic, (120, 120), profile_pic)

    # Draw the user's name and bounty value on the poster
    draw = ImageDraw.Draw(poster_template)
    font = ImageFont.truetype('arialbd.ttf', 48)
    draw.text((220, 300), username, font=font, fill=(255, 255, 255))
    draw.text((220, 400), f'Bounty: {bounty} berries', font=font, fill=(255, 255, 255))

    # Save the final poster as a temporary file
    poster_path = 'bounty_poster.png'
    poster_template.save(poster_path)

    # Send the poster image as a Discord message
    return discord.File(poster_path)


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    user = message.author

    # Increment user's bounty
    increment_bounty(user)

    # Increment user's level
    increment_level(user)

    # Continue processing other commands and events
    await bot.process_commands(message)


@bot.command()
async def bounty(ctx):
    user = ctx.author
    poster = generate_bounty_poster(user)
    await ctx.send(file=poster)


@bot.command()
async def level(ctx):
    user = ctx.author'''


bot.run('MTAxNjU2ODg0OTk2MjkwNTcxMw.GdvpPP.zSm_QTjjvkNwlxRHFLWmQ2ZZqSSlRZ6Op3G-ok')
