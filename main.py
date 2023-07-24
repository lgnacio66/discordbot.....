import discord
import random
import asyncio
import sqlite3
import json

from discord.ext import commands
from discord import app_commands

# Set up the bot and database connection
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='o ', intents=intents)



# Connect to the SQLite database
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# TODO: Add database tables and functions

# Function to create the users table
def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            alias TEXT,
            character_pfp_url TEXT,
            berries INTEGER,
            golden_berries INTEGER,
            guild_id INTEGER,
            FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
        )
    """)
    conn.commit()

# Create the users table (run this once)
create_users_table()

# Function to create the guilds table
def create_guilds_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id INTEGER PRIMARY KEY,
            guild_name TEXT,
            guild_master_id INTEGER
        )
    """)
    conn.commit()

# Create the guilds table (run this once)
create_guilds_table()

# Function to create a user profile
def create_profile(user_id, alias, character_pfp_url):
    cursor.execute("INSERT INTO users (user_id, alias, character_pfp_url, berries, golden_berries, guild_id) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, alias, character_pfp_url, 1000, 0, None))
    conn.commit()

# Function to create a guild
def create_guild(guild_id, guild_name, guild_master_id):
    cursor.execute("INSERT INTO guilds (guild_id, guild_name, guild_master_id) VALUES (?, ?, ?)",
                   (guild_id, guild_name, guild_master_id))
    conn.commit()

# Function to add a member to a guild
def add_member_to_guild(member_id, guild_id):
    cursor.execute("UPDATE users SET guild_id=? WHERE user_id=?", (guild_id, member_id))
    conn.commit()

# Function to get user profile from the database
def get_user_profile(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

# Function to get guild information from the database
def get_guild_info(guild_id):
    cursor.execute("SELECT * FROM guilds WHERE guild_id=?", (guild_id,))
    return cursor.fetchone()




# TODO: Create Player class

class Player:
    def __init__(self, user_id, alias, character_pfp_url):
        self.user_id = user_id
        self.alias = alias
        self.character_pfp_url = character_pfp_url
        self.berries = 1000
        self.golden_berries = 0
        self.cards = []
        self.weapons = []
        self.guild = None
        self.pet = None
        self.pvp_wins = 0
        self.pvp_losses = 0
        self.achievements = []
        self.badges = []
        self.daily_login_streak = 0

    def add_card(self, card):
        self.cards.append(card)

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def add_golden_berries(self, amount):
        self.golden_berries += amount

    def add_pvp_win(self):
        self.pvp_wins += 1

    def add_pvp_loss(self):
        self.pvp_losses += 1

    def add_achievement(self, achievement):
        self.achievements.append(achievement)

    def add_badge(self, badge):
        self.badges.append(badge)

    def add_daily_login_streak(self):
        self.daily_login_streak += 1

    def reset_daily_login_streak(self):
        self.daily_login_streak = 0

    def get_total_power(self):
        total_power = 0
        for card in self.cards:
            total_power += card.base_power

        if self.pet:
            total_power += self.pet.bonus_power

        return total_power

    def trade_cards(self, other_player, card1, card2):
        if card1 in self.cards and card2 in other_player.cards:
            self.cards.remove(card1)
            other_player.cards.remove(card2)
            self.cards.append(card2)
            other_player.cards.append(card1)

    def get_achievements(self):
        return self.achievements

    def get_badges(self):
        return self.badges

    def get_pvp_stats(self):
        return f"Total Wins: {self.pvp_wins}, Total Losses: {self.pvp_losses}"

    # Add more methods for other features

# TODO: Define Card, Weapon, Pet, Achievement, Badge, and other classes as required

# Define the Bot and SlashCommand instances
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

class Card:
    def __init__(self, name, power, character, image_url):
        self.name = name
        self.base_power = power
        self.character = character
        self.image_url = image_url

class Weapon:
    def __init__(self, name, multiplier, image_url):
        self.name = name
        self.multiplier = multiplier
        self.image_url = image_url

class Pet:
    def __init__(self, name, bonus_power, image_url):
        self.name = name
        self.bonus_power = bonus_power
        self.image_url = image_url

class Achievement:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Badge:
    def __init__(self, name, image_url):
        self.name = name
        self.image_url = image_url

# PVP Battle Command
@bot.command(name="pvp_battle", description="Challenge another player to a PVP battle.")
async def pvp_battle(ctx, target: discord.Member):
    # Get player profiles from the database based on ctx.author and target
    # Implement the PVP battle logic and determine the winner
    # Update player profiles in the database based on the battle result

    await ctx.send(f"{ctx.author.mention} has challenged {target.mention} to a PVP battle!")

# Example Achievements and Badges (for illustration purposes)
achievements_list = [
    Achievement("First Mission Complete", "Complete your first mission."),
    Achievement("PVP Champion", "Win 10 PVP battles."),
    # Add more achievements as needed...
]

badges_list = [
    Badge("Mission Master", "badge_image_url_1"),
    Badge("PVP Legend", "badge_image_url_2"),
    # Add more badges as needed...
]
# TODO: Create Mission class
class Mission:
    def __init__(self, name, description, options, difficulty, correct_option):
        self.name = name
        self.description = description
        self.options = options
        self.difficulty = difficulty
        self.correct_option = correct_option

    def get_difficulty_name(self):
        difficulty_names = {'D': 'D RANK MISSION',
                            'C': 'C RANK MISSION',
                            'B': 'B RANK MISSION',
                            'A': 'A RANK MISSION',
                            'S': 'S RANK MISSION'}
        return difficulty_names.get(self.difficulty, 'UNKNOWN RANK MISSION')

    def calculate_rewards(self):
        rewards_dict = {'D': 100, 'C': 125, 'B': 150, 'A': 175, 'S': 200}
        return rewards_dict.get(self.difficulty, 0)

    def check_answer(self, user_answer):
        return self.options[user_answer] == self.correct_option

# Sample missions
missions = []

def create_missions():
    global missions

    # Define missions format with options as lists
    mission1 = Mission(
        "Mission_1",
        "Who is the father of Monkey D. Luffy?",
        ["Dragon", "Shanks", "Garp", "Crocodile"],
        "B",
        "Dragon"
    )

    mission2 = Mission(
        "Mission_2",
        "Who was the first member of the SH crew to try and recruit a new member besides Luffy?",
        ["Zoro", "Usopp", "Nami", "Sanji"],
        "D",
        "Zoro"
    )

    # Add more missions as needed...

    # Shuffle the options for each mission
    for mission in [mission1, mission2]:
        random.shuffle(mission.options)

    # Append the missions to the list
    missions.append(mission1)
    missions.append(mission2)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def mission(ctx):
    """Retrieve a random mission from the list."""
    global missions

    if len(missions) == 0:
        await ctx.send("No missions available.")
        return

    mission = random.choice(missions)
    missions.remove(mission)

    embed = discord.Embed(title=f"Mission: {mission.name}",
                          description=f"**{mission.description}**",
                          color=discord.Color.blue())

    options_text = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(mission.options)])
    embed.add_field(name="Options:", value=options_text, inline=False)

    difficulty_name = mission.get_difficulty_name()
    embed.add_field(name="Difficulty", value=f"**{difficulty_name}**", inline=True)

    embed.set_image(url="https://media.giphy.com/media/3o7TKoWjU2koVfFdGk/giphy.gif")

    msg = await ctx.send(embed=embed)

    # Add reactions for each option
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
    for emoji in emojis:
        await msg.add_reaction(emoji)

# TODO: Implement profile creation command
user_profiles = {}
@bot.command(name="create_profile", description="Create your personal profile with a pfp and alias.")
async def create_profile(ctx):
    # Check if the user already has a profile
    if ctx.author.id in user_profiles:
        await ctx.send("You already have a profile.")
        return

    # Send the create profile embed
    embed = discord.Embed(title="Create Your Profile",
                          description="Welcome to One Piece WORLD! Please create your personal profile.",
                          color=discord.Color.blue())

    embed.add_field(name="Alias:", value="Enter your alias (nickname) for the game.", inline=False)
    embed.add_field(name="Character PFP URL:",
                    value="Provide the URL of the One Piece character pfp you want to use.", inline=False)
    embed.set_image(url="https://media.giphy.com/media/3o7TKoWjU2koVfFdGk/giphy.gif")

    msg = await ctx.send(embed=embed)

    # Define a check function for the message
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # Wait for alias input from the user
        alias_msg = await bot.wait_for('message', timeout=60.0, check=check)
        alias = alias_msg.content

        # Wait for character pfp URL input from the user
        pfp_msg = await bot.wait_for('message', timeout=60.0, check=check)
        character_pfp_url = pfp_msg.content

        # Create the user profile
        create_profile(ctx.author.id, alias, character_pfp_url)

        # Send confirmation message
        await ctx.send(f"Profile created successfully for {ctx.author.mention}!\n"
                       f"Alias: {alias}\n"
                       f"Character PFP: {character_pfp_url}")
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, time limit exceeded. Profile creation canceled.")



# TODO: Implement balance command

def get_player(user_id):
    # Check if the player profile already exists in the database
    # If it exists, fetch the profile and return the Player object
    # If it doesn't exist, create a new profile and return the Player object
    def save_player(player):
        # Save the player profile back to the database

        # Assuming you have a 'players' table in your database with columns 'user_id', 'alias', 'character_pfp_url', etc.
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        # Convert player object attributes to tuples
        player_data = (
            player.user_id,
            player.alias,
            player.character_pfp_url,
            player.berries,
            player.golden_berries,
            player.cards,
            player.weapons,
            player.guild.id if player.guild else None,
            player.pet.id if player.pet else None,
            player.pvp_wins,
            player.pvp_losses,
            player.achievements,
            player.badges,
            player.daily_login_streak
        )

        cursor.execute("""
            INSERT OR REPLACE INTO players (user_id, alias, character_pfp_url, berries, golden_berries, cards, weapons, guild_id, pet_id, pvp_wins, pvp_losses, achievements, badges, daily_login_streak)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, player_data)

        conn.commit()
        conn.close()

    @bot.command(aliases=['bal', 'balance'])
    async def show_balance(ctx):
        player = get_player(ctx.author.id)
    # Assuming you have a 'players' table in your database with columns 'user_id', 'alias', 'character_pfp_url', etc.
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE user_id=?", (user_id,))
    player_data = cursor.fetchone()
    conn.close()

    if player_data:
        user_id, alias, character_pfp_url, berries, golden_berries, cards, weapons, guild_id, pet_id, pvp_wins, pvp_losses, achievements, badges, daily_login_streak = player_data
        player = Player(user_id, alias, character_pfp_url)
        player.berries = berries
        player.golden_berries = golden_berries
        player.cards = cards
        player.weapons = weapons
        player.guild = guild_id
        player.pet = pet_id
        player.pvp_wins = pvp_wins
        player.pvp_losses = pvp_losses
        player.achievements = achievements
        player.badges = badges
        player.daily_login_streak = daily_login_streak
    else:
        # Create a new player profile if it doesn't exist in the database
        player = Player(user_id, "", "")
        save_player(player)  # You need to implement the 'save_player()' function to save the new player profile to the database

    return player

@bot.command(aliases=['bal', 'balance'])
async def show_balance(ctx):
    player = get_player(ctx.author.id)

    # Access player's balance and other attributes as needed
    balance = player.berries
    golden_berries = player.golden_berries

    embed = discord.Embed(title="Balance",
                          description=f"{ctx.author.mention}, here is your balance:",
                          color=discord.Color.gold())
    embed.add_field(name="Berries:", value=str(balance), inline=False)
    embed.add_field(name="Golden Berries:", value=str(golden_berries), inline=False)

    await ctx.send(embed=embed)
# TODO: Implement cooldowns command
@bot.command()
async def cooldowns(ctx):
    """Check active cooldowns for commands."""
    embed = discord.Embed(title="Command Cooldowns", color=discord.Color.gold())

    cooldown_info = []
    for command in bot.commands:
        if isinstance(command._buckets, commands.CooldownMapping):
            cooldown = command._buckets._cooldown
            if cooldown:
                # Get the cooldown bucket for the command
                bucket = command._buckets.get_bucket(ctx.message)
                remaining = bucket._cooldown - (ctx.message.created_at - bucket._window.get(ctx.message.author.id, 0))
                remaining = max(remaining.total_seconds(), 0)

                # Add the cooldown info to the list
                cooldown_info.append(f"{command.name}: {remaining:.1f}s")

    if cooldown_info:
        cooldown_text = "\n".join(cooldown_info)
        embed.add_field(name="Active Cooldowns:", value=cooldown_text, inline=False)
    else:
        embed.add_field(name="Active Cooldowns:", value="No active cooldowns.", inline=False)

    await ctx.send(embed=embed)

# TODO: Implement guild-related functions
@bot.command()
async def create_guild(ctx):
    """Start the process of creating a guild."""
    # Check if the user already belongs to a guild
    user_profile = get_user_profile(ctx.author.id)
    if user_profile['guild_id']:
        await ctx.send("You are already a member of a guild. You cannot create a new one.")
        return

    # Ask the user for the guild name
    await ctx.send("Please enter the desired name for your guild:")
    try:
        guild_name_msg = await bot.wait_for('message', timeout=60.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        guild_name = guild_name_msg.content

        # Create the guild and add it to the database
        create_guild(ctx.guild.id, guild_name, ctx.author.id)

        # Add the guild master as a member of the guild
        add_member_to_guild(ctx.author.id, ctx.guild.id)

        await ctx.send(f"Congratulations, {ctx.author.mention}! You have successfully created the guild '{guild_name}'.")
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, time limit exceeded. Guild creation canceled.")

# TODO: Create Guild class
class Guild:
    def __init__(self, guild_id, guild_name, guild_master_id):
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.guild_master_id = guild_master_id
        self.members = []

    def add_member(self, member_id):
        self.members.append(member_id)

    def remove_member(self, member_id):
        if member_id in self.members:
            self.members.remove(member_id)

    def get_member_count(self):
        return len(self.members)

    def is_member(self, member_id):
        return member_id in self.members

    def get_guild_info(self):
        return f"Guild ID: {self.guild_id}\nGuild Name: {self.guild_name}\nGuild Master ID: {self.guild_master_id}"

    # Add more methods for other features related to guilds

# TODO: Implement guild creation command
# Function to add a guild to the database
def add_guild(guild_id, guild_name, guild_master_id):
    conn = sqlite3.connect("guilds.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guilds (guild_id, guild_name, guild_master_id) VALUES (?, ?, ?)",
                   (guild_id, guild_name, guild_master_id))
    conn.commit()
    conn.close()



# TODO: Implement guild join command
# TODO: Implement guild join request

join_requests = {}  # Dictionary to store join requests (guild_id: {user_id: user_profile})


@bot.command()
async def guild_join_request(ctx, guild_name: str):
    # Check if the user already has a profile
    if ctx.author.id not in user_profiles:
        await ctx.send("You need to create a profile first using the /create_profile command.")
        return

    user_profile = user_profiles[ctx.author.id]

    # Check if the user is already a member of a guild
    if user_profile.guild is not None:
        await ctx.send("You are already a member of a guild.")
        return

    # Get the list of available guilds (you need to define this list based on your game's logic)
    available_guilds = get_available_guilds()

    if not available_guilds:
        await ctx.send("There are no available guilds to join.")
        return

    # Find the selected guild by name
    selected_guild = None
    for guild in available_guilds:
        if guild.name == guild_name:
            selected_guild = guild
            break

    # If the selected guild is not found, send an error message
    if not selected_guild:
        await ctx.send("Invalid guild name. Please select a valid guild.")
        return

    # Store the join request in the dictionary
    if selected_guild.id not in join_requests:
        join_requests[selected_guild.id] = {}

    join_requests[selected_guild.id][ctx.author.id] = user_profile

    # Send a DM to the guild master and vice master about the join request
    guild_master_id = selected_guild.guild_master_id
    guild_vice_master_id = selected_guild.guild_vice_master_id

    guild_master = bot.get_user(guild_master_id)
    guild_vice_master = bot.get_user(guild_vice_master_id)

    if guild_master:
        dm_message = f"User {ctx.author.mention} has requested to join your guild {selected_guild.name}. Use /accept_join_request {ctx.author.id} to accept their request."
        await guild_master.send(dm_message)

    if guild_vice_master:
        dm_message = f"User {ctx.author.mention} has requested to join your guild {selected_guild.name}. Use /accept_join_request {ctx.author.id} to accept their request."
        await guild_vice_master.send(dm_message)

    # Send a confirmation message to the user
    await ctx.send(
        f"You have requested to join {selected_guild.name}. The guild master and vice master will be notified about your request.")



# TODO: Implement guild join request

def save_player(player_profile):
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE my_table SET alias=?, character_pfp_url=?, berries=?, golden_berries=?, "
                   "cards=?, weapons=?, guild=? WHERE id=?",
                   (player_profile.alias, player_profile.character_pfp_url, player_profile.berries,
                    player_profile.golden_berries, json.dumps(player_profile.cards), json.dumps(player_profile.weapons),
                    player_profile.guild, player_profile.user_id))
    conn.commit()
    conn.close()


join_requests = {}  # Dictionary to store join requests (guild_id: {user_id: user_profile})

def get_available_guilds():
    # Sample guilds, replace this with the actual list of available guilds
    return [
        Guild("Straw Hat Pirates", guild_master_id=12345, guild_vice_master_id=67890, member_count=5),
        Guild("Whitebeard Pirates", guild_master_id=98765, guild_vice_master_id=54321, member_count=8),
        Guild("Heart Pirates", guild_master_id=13579, guild_vice_master_id=24680, member_count=3)
    ]

@bot.command()
async def guild_join_request(ctx, guild_name: str):
    # Get the available guilds
    available_guilds = get_available_guilds()

    # Check if the requested guild exists in the available guilds
    requested_guild = next((guild for guild in available_guilds if guild.name == guild_name), None)

    if requested_guild is None:
        await ctx.send("Invalid guild name. Please choose a valid guild to join.")
        return

    # Check if the user is already in a guild
    user_id = str(ctx.author.id)
    if user_id in user_profiles and user_profiles[user_id].guild is not None:
        await ctx.send("You are already part of a guild. You cannot join another guild.")
        return

    # Store the join request in the dictionary
    if requested_guild.guild_id not in join_requests:
        join_requests[requested_guild.guild_id] = {}

    join_requests[requested_guild.guild_id][user_id] = user_profiles[user_id]

    # Inform the guild master or vice master about the join request
    guild_master_id = requested_guild.guild_master_id
    guild_vice_master_id = requested_guild.guild_vice_master_id

    message = f"Player {ctx.author.mention} has requested to join {guild_name} guild. Use the command " \
              f"'o accept_join_request {ctx.author.id}' to accept the request."

    await bot.get_user(guild_master_id).send(message)
    await bot.get_user(guild_vice_master_id).send(message)

    await ctx.send("Your join request has been sent to the guild master and vice master. "
                   "They will review your request and decide whether to accept you into the guild.")

@bot.command()
async def accept_join_request(ctx, player_id: int):
    # Check if the command is invoked by the guild master or vice master
    guild_id = ctx.guild.id
    user_id = str(ctx.author.id)

    # Check if the user is the guild master or vice master
    if guild_id not in join_requests or user_id not in [str(requested_id) for requested_id in join_requests[guild_id]]:
        await ctx.send("You are not authorized to use this command.")
        return

    # Check if the player ID is valid and if there is a join request from that player
    player_id = str(player_id)
    if guild_id not in join_requests or player_id not in join_requests[guild_id]:
        await ctx.send("Invalid player ID or no join request from that player.")
        return

    # Add the player to the guild
    player_profile = join_requests[guild_id].pop(player_id)
    guild = get_guild_info(guild_id)

    if guild:
        guild_name = guild.guild_name
        player_profile.guild = guild_name
        save_player(player_profile)

        # Inform the player about the acceptance
        player_user = bot.get_user(int(player_id))
        if player_user:
            await player_user.send(f"Congratulations! You have been accepted into {guild_name} guild.")
            await ctx.send(f"Player {player_user.mention} has been added to {guild_name} guild.")
        else:
            await ctx.send("Failed to send a message to the player.")

    else:
        await ctx.send("Failed to add the player to the guild. Please try again later or contact support.")



# You may also need to update the Guild class with additional methods and properties.


# TODO: Create Leaderboard class
class Leaderboard:
    def __init__(self, title):
        self.title = title
        self.players = {}  # Dictionary to store player profiles (user_id: player_profile)

    def add_player(self, player_profile):
        self.players[player_profile.user_id] = player_profile

    def remove_player(self, user_id):
        if user_id in self.players:
            del self.players[user_id]

    def get_sorted_players(self, criteria='total_power', reverse=True):
        # Sort players based on the given criteria
        sorted_players = sorted(self.players.values(), key=lambda player: getattr(player, criteria), reverse=reverse)
        return sorted_players

    def get_leaderboard_embed(self, criteria='total_power', reverse=True, max_entries=10):
        # Get the sorted players based on the criteria
        sorted_players = self.get_sorted_players(criteria=criteria, reverse=reverse)

        # Create the leaderboard embed
        embed = discord.Embed(title=self.title, color=discord.Color.gold())

        # Add entries to the embed
        for index, player in enumerate(sorted_players[:max_entries], start=1):
            entry = f"{index}. {player.alias} - {getattr(player, criteria)}"
            embed.add_field(name=f"Rank {index}", value=entry, inline=False)

        return embed

# TODO: Implement leaderboard commands
# Create an instance of the Leaderboard class
global_leaderboard = Leaderboard(title="Global Leaderboard")

# Command to display the global leaderboard based on total power
@bot.command()
async def leaderboard_total_power(ctx, top: int = 10):
    # Get the sorted players based on total power
    sorted_players = global_leaderboard.get_sorted_players(criteria='total_power', reverse=True)

    # Create the leaderboard embed
    embed = discord.Embed(title="Global Leaderboard - Total Power", color=discord.Color.gold())

    # Add entries to the embed
    for index, player in enumerate(sorted_players[:top], start=1):
        entry = f"{index}. {player.alias} - {player.total_power}"
        embed.add_field(name=f"Rank {index}", value=entry, inline=False)

    await ctx.send(embed=embed)

# Command to display the global leaderboard based on number of berries
@bot.command()
async def leaderboard_Richest(ctx, top: int = 10):
    # Get the sorted players based on number of berries
    sorted_players = global_leaderboard.get_sorted_players(criteria='berries', reverse=True)

    # Create the leaderboard embed
    embed = discord.Embed(title="Global Leaderboard - Berries", color=discord.Color.gold())

    # Add entries to the embed
    for index, player in enumerate(sorted_players[:top], start=1):
        entry = f"{index}. {player.alias} - {player.berries} Berries"
        embed.add_field(name=f"Rank {index}", value=entry, inline=False)

    await ctx.send(embed=embed)

# Add more commands for other leaderboard criteria as needed...

# TODO: Implement pulling cards using berries and golden berries

# Define the Card class to store card information
class Card:
    def __init__(self, name, base_power, rarity, image_url):
        self.name = name
        self.base_power = base_power
        self.rarity = rarity
        self.image_url = image_url

# Define the cards for each rarity in separate dictionaries

D_CARDS = {
    1: Card(name="Card1", base_power=50, rarity="D", image_url="URL_OF_CARD1_IMAGE"),
    2: Card(name="Card2", base_power=55, rarity="D", image_url="URL_OF_CARD2_IMAGE"),
    # Add more D rarity cards...
}

C_CARDS = {
    1: Card(name="Card4", base_power=70, rarity="C", image_url="URL_OF_CARD4_IMAGE"),
    2: Card(name="Card5", base_power=75, rarity="C", image_url="URL_OF_CARD5_IMAGE"),
    # Add more C rarity cards...
}

B_CARDS = {
    1: Card(name="Card7", base_power=90, rarity="B", image_url="URL_OF_CARD7_IMAGE"),
    2: Card(name="Card8", base_power=95, rarity="B", image_url="URL_OF_CARD8_IMAGE"),
    # Add more B rarity cards...
}

A_CARDS = {
    1: Card(name="Card10", base_power=110, rarity="A", image_url="URL_OF_CARD10_IMAGE"),
    2: Card(name="Card11", base_power=115, rarity="A", image_url="URL_OF_CARD11_IMAGE"),
    # Add more A rarity cards...
}

# Combine all the card dictionaries into a single list (card_database)
card_database = []
card_database.extend(D_CARDS.values())
card_database.extend(C_CARDS.values())
card_database.extend(B_CARDS.values())
card_database.extend(A_CARDS.values())

# Sample user_profiles dictionary
user_profiles = {
    # Sample user profiles
    "123456": Player("123456", "Player1", "URL_OF_PFP"),
    "987654": Player("987654", "Player2", "URL_OF_PFP"),
    # Add more user profiles...
}

@bot.command()
async def pull(ctx, type: str):
    user_id = str(ctx.author.id)

    # Check if the user has a profile
    if user_id not in user_profiles:
        await ctx.send("You need to create a profile first. Use the 'create_profile' command.")
        return

    player = user_profiles[user_id]
    if type.lower() == "berry":
        if player.berries < 100:
            await ctx.send("You don't have enough berries to pull a card.")
            return

        # Pull a card using berries
        pulled_card = random.choice(list(D_CARDS.values()))
        player.berries -= 100

    elif type.lower() == "golden":
        if player.golden_berries < 1:
            await ctx.send("You don't have enough golden berries to pull a card.")
            return

        # Pull a card using golden berries
        rarity = random.choices(["D", "C", "B", "A"], weights=[50, 35, 10, 5], k=1)[0]
        if rarity == "D":
            pulled_card = random.choice(list(D_CARDS.values()))
        elif rarity == "C":
            pulled_card = random.choice(list(C_CARDS.values()))
        elif rarity == "B":
            pulled_card = random.choice(list(B_CARDS.values()))
        else:  # rarity == "A"
            pulled_card = random.choice(list(A_CARDS.values()))

        player.golden_berries -= 1

    else:
        await ctx.send("Invalid pull type. Use either 'berry' or 'golden'.")
        return

    # Add the pulled card to the player's collection
    player.add_card(pulled_card)

    # Send the pull result as an embed with the card image
    embed = discord.Embed(title="Card Pull Result",
                          description=f"You pulled a card!",
                          color=discord.Color.blue())

    embed.add_field(name="Card Name:", value=pulled_card.name, inline=False)
    embed.add_field(name="Rarity:", value=pulled_card.rarity, inline=True)
    embed.add_field(name="Base Power:", value=pulled_card.base_power, inline=True)
    embed.set_image(url=pulled_card.image_url)

    await ctx.send(embed=embed)

    # Save the updated player profile
    save_player(player)

@bot.command(name="all")
async def view_all_cards(ctx):
    user_id = str(ctx.author.id)

    # Check if the user has a profile
    if user_id not in user_profiles:
        await ctx.send("You need to create a profile first. Use the 'create_profile' command.")
        return

    player = user_profiles[user_id]

    # Check if the user has any cards
    if not player.cards:
        await ctx.send("You don't have any cards in your collection.")
        return

    # Send the user's card collection as an embed
    embed = discord.Embed(title="Your Card Collection",
                          description="Here are all the cards you have collected:",
                          color=discord.Color.green())

    for i, card in enumerate(player.cards, 1):
        embed.add_field(name=f"Card {i}", value=f"Name: {card.name}\nRarity: {card.rarity}\nBase Power: {card.base_power}",
                        inline=False)

    await ctx.send(embed=embed)



def pull_card():
    # Define the probabilities for each rarity (adjust the values as needed)
    rarity_probabilities = {
        "D": 0.4,   # 40% probability
        "C": 0.3,   # 30% probability
        "B": 0.2,   # 20% probability
        "A": 0.1,   # 10% probability
        "S": 0.00001,  # 5% probability
        "SS": 0.0000000000001  # 5% probability
    }

    # Generate a random number between 0 and 1
    random_number = random.random()

    # Determine the rarity based on the probabilities
    cumulative_probability = 0
    selected_rarity = None
    for rarity, probability in rarity_probabilities.items():
        cumulative_probability += probability
        if random_number <= cumulative_probability:
            selected_rarity = rarity
            break

    # Filter cards based on selected rarity
    available_cards = [card for card in card_database if card.rarity == selected_rarity]

    # Randomly select a card from the filtered list
    selected_card = random.choice(available_cards)

    return selected_card

# Rest of the code remains the same...

# ...

#
# TODO: Implement card system, tiers, and fusion

# TODO: Implement pet system and related commands

# TODO: Implement event system and special quests

# TODO: Implement trading system for duplicate cards

# TODO: Implement PVP battles and wagering rewards

# TODO: Implement tower challenge and guild evolution system

# Run the bot
bot.run('MTEzMTE2NTc2MzUxMjg0ODUwNQ.G7zR6a.IBt2nEC_Uwy2S11x_d1I63Jrx8VH12EkXZsvNo')


