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
    comp = [int(i) for i in comp.split()]  # convert string input to array

    new_group = Group(owner, name, role, group_type, rating, time, comp)
    bg_bot.manager.add_group(owner, new_group)
    
    await ctx.send(f'Created new {group_type} group for leader {owner}!')


@bg_bot.command(name='delete_group')
async def delete_group(ctx, group_name: str, owner: str=None):
    """Remove a group from the GroupManager

    First check to see if the message author has permission to remove the specified group

    Args:
        group_name ([str]): Name of group to delete
        owner ([str], optional): Owner of group to delete; if omitted, defaults to message author
    """

    if owner and owner != ctx.message.author.name:
        if ctx.message.author.id != bot.owner_id:
            response = "Sorry, you don't have permission to delete that group. Nerd."
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
        option ([str]), optional): Specify an attribute of Group class to display
    """

    groups = bg_bot.manager.get_groups(owner, group_name)

    if len(groups) == 0:
        response = "No groups exist that match those criteria."
    elif group_name and option:
        response = [getattr(group, option) for group in groups]
    else:
        response = [group.name for group in groups]

    await ctx.send(response)
