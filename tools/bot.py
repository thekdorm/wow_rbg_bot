import discord

from .Group import Group, GroupManager
from .secrets import owner

from discord.ext import commands

bg_bot = commands.Bot(command_prefix='!')
bg_bot.manager = GroupManager()


@bg_bot.event
async def on_ready():
    # do all this stuff when bot connects successfully
    bg_bot.owner_id = owner
    print(f'Logged in as {bg_bot.user.name}!')


@bg_bot.command(name='create_group')
async def create_group(ctx, name: str, role: str, group_type: str=None, comp: str=None, rating: int=None, time: str=None):
    """Create a new group

    Args:
        name ([str]): Name of group
        role ([str]): Role of group leader
        group_type ([str], optional): <arena2 | arena3 | rbg>
        comp ([str], optional): Desired tank/healer/dps composition for group i.e. "1 3 6"
        rating ([int], optional): Desired group rating; if omitted, YOLO
        time ([str], optional): Desired group start time; if omitted, ASAP
    """

    owner = ctx.message.author.name
    
    if comp:
        comp = [int(i) for i in comp.split()]  # convert string input to array

    new_group = Group(owner, name, role, group_type, rating, time, comp)
    bg_bot.manager.add_group(owner, new_group)
    
    await ctx.send(f'Created new {group_type} group for leader {owner}!')


@bg_bot.command(name='delete_group')
async def delete_group(ctx, group_name: str, owner: str=None):
    """Remove a group from the GroupManager

    Args:
        group_name ([str]): Name of group to delete
        owner ([str], optional): Owner of group to delete; if omitted, defaults to message author
    """

    if owner and owner != ctx.message.author.name:
        if ctx.message.author.id != bot.owner_id:
            await ctx.send("Sorry, you don't have permission to delete that group. Nerd.")
    else:
        owner = ctx.message.author.name

    if bg_bot.manager.remove_group(owner, group_name):
        response = f'{group_name} successfully removed from {owner} groups!'
    else:
        response = f'Error in removing {group_name} from {owner} groups!'
    
    await ctx.send(response)


@bg_bot.command(name='display_group')
async def display_group(ctx, owner: str, group_name: str=None, option: str=None):
    """Display the existing groups for specified owner

    Args:
        owner ([str]): Owner of groups to display
        group_name ([str], optional): Name of group to display; if omitted, display all groups of specified owner
        *deprecated option ([str]), optional): Specify an attribute of Group class to display
    """

    groups = bg_bot.manager.get_groups(owner, group_name)

    if len(groups) == 0:
        await ctx.send("No groups exist that match the input criteria.")
    else:
        embed = discord.Embed(title="Open Groups")
        for group in groups:
            if group.comp:
                open_spots = [group.comp[role]['number'] - len(group.comp[role]['players']) for role in group.comp]
                availability = f'Open Spots\nTanks: {open_spots[0]}, Healers: {open_spots[1]}, DPS: {open_spots[2]}'
            else:
                availability = f'No specified comp, {group._max - group._total} spots left'
            
            embed.add_field(name=f'{group.name} by {group.owner}: {group.rating} {group.group_type}', value=availability)

    await ctx.send(embed=embed)


@bg_bot.command(name='add_player')
async def add_player(ctx, group_name: str, player_name: str, player_role: str, owner: str=None):
    """Add a player to an existing group

    Args:
        group_name (str): Name of group
        player_name (str): Name of player to add to group
        player_role (str): <tank | healer | dps>
        owner (str): Leader of group
    """

    if owner and owner != ctx.message.author.name:
        if ctx.message.author.id != bot.owner_id:
            await ctx.send("Sorry, you don't have permission to modify that group. Nerd.")
    else:
        owner = ctx.message.author.name
    
    if owner in bg_bot.manager.groups:
        for group in bg_bot.manager.groups[owner]['groups']:
            if group.name == group_name:
                if group.add_member(player_name, player_role):
                    response = f'Added {player_name} to {group_name} successfully!'
                    break
                else:
                    response = "Error adding player! Specified role is most likely already full for this group."
                    break

    else:
        response = "No groups exist that match the input criteria."
    
    await ctx.send(response)


@bg_bot.command(name='remove_player')
async def remove_player(ctx, group_name: str, player_name: str, owner: str=None):
    """Remove a player from an existing group

    Args:
        group_name (str): Name of group
        player_name (str): Name of player to add to group
        owner (str): Leader of group
    """

    if owner and owner != ctx.message.author.name:
        if ctx.message.author.id != bot.owner_id:
            await ctx.send("Sorry, you don't have permission to modify that group. Nerd.")
    else:
        owner = ctx.message.author.name
    
    if owner in bg_bot.manager.groups:
        for group in bg_bot.manager.groups[owner]['groups']:
            if group.name == group_name:
                if group.remove_member(player_name):
                    response = f'Removed {player_name} from {group_name} successfully!'
                    break
                else:
                    response = "Error removing player!"
                    break

    else:
        response = "No groups exist that match the input criteria."
    
    await ctx.send(response)
