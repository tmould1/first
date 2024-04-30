import os
import random

from discord.ext import commands
import discord.utils

import game

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = "test"
GAME_CHANNEL = "game"

activity = discord.Game(name="Playing games, !help for commands")
game_bot = game.DiscordBot(activity=activity, intents=discord.Intents.all(), command_prefix='!')
#set the presence of the bot
game_bot.status

# Handles event registration
@game_bot.event
async def on_ready():
    proper_guild = discord.utils.get(game_bot.guilds, name=GUILD)
        
    print(
        f'{game_bot.user} has connected to Discord!\n'
        f'{proper_guild.name}(id: {proper_guild.id})\n'
    )
    
    members = '\n - '.join([member.name for member in proper_guild.members])
    print(f'Guild Members:\n - {members}')
    
@game_bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! 💯💯💯'
    )
    
@game_bot.command(name='playgame', help='Starts a game in the game channel')
async def playgame(context):
    print(f'Received playgame command from {context.author.name} in channel {context.channel.name}')
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    await context.send("Let's play a game! 🎮")
    if game_bot.game.is_playing(context.author.name) is False:
        game_bot.joingame(context)
    await context.send("Here's the map:")
    await context.send(game_bot.show_player_surroundings(context))

@game_bot.command(name='rolldice', help='Rolls some dice')
async def roll_dice(context, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await context.send(', '.join(dice))
    await context.send(f'Total: {sum([int(die) for die in dice])}')
    
@game_bot.command(name='createchannel', help='Creates a new channel')
@commands.has_role('admin')
async def create_channel(context, channel_name):
    guild = context.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await context.send(f'Channel {channel_name} created')
    else:
        await context.send(f'Channel {channel_name} already exists')

@game_bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.errors.CheckFailure):
        await context.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await context.send('Please pass in all required arguments.')
    else:
        print(f'An error occurred: {error}')
        
@game_bot.command(name='move', help='Move your player on the map')
async def move(context, direction):
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    move_msg = game_bot.move_player(context, direction)
    await context.send(move_msg)
    await context.send(game_bot.show_player_surroundings(context))
    
@game_bot.command(name='showmap', help='Show the map')
async def show_map(context):
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    await context.send(game_bot.show_player_surroundings(context))
    
@game_bot.command(name='attack', help='Attack an enemy')
async def attack(context, target_name):
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    attack_msg = game_bot.attack_enemy(context, target_name)
    await context.send(attack_msg)
    
@game_bot.command(name='stats', help='Show player stats')
async def stats(context):
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    await context.send(game_bot.show_player_stats(context))
    
# @game_bot.command(name='inventory', help='Show player inventory')
# async def inventory(context):
#     if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
#         # send the user a DM directing them to the game channel
#         await context.author.create_dm()
#         await context.author.dm_channel.send(
#             f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
#         )
#         return
#     await context.send(game_bot.show_player_inventory(context))

@game_bot.command(name='take', help='Take an item')
async def take(context, item_name):
    if context.channel != discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel for game-related messages.'
        )
        return
    take_msg = game_bot.take_item(context, item_name)
    await context.send(take_msg)

game_bot.run(TOKEN)