## Initialisation
import discord

## Get a role objet given a name, mention or id and a guild
async def getRole(nameOrID, guild):
    if type(nameOrID) is str:
        if nameOrID.isdigit():
            return guild.get_role(int(nameOrID))
        else:
            for role in guild.roles:
                if role.name == nameOrID or role.mention == nameOrID:
                    return role
            return None
    elif type(nameOrID) is int:
        return guild.get_role(nameOrID)
    else:
        return None

## Get a member objet given a name, mention or id and a guild
async def getMember(nameOrID, guild):
    if type(nameOrID) is str:
        if nameOrID.isdigit():
            return guild.get_member(int(nameOrID))
        else:
            for member in guild.members:
                if member.name == nameOrID or str(member.id) in nameOrID:
                    return member
            return None
    elif type(nameOrID) is int:
        return guild.get_member(nameOrID)
    else:
        return None

async def getChannel(nameOrID,guild):
    if type(nameOrID) is str:
        if nameOrID.isdigit():
            return guild.get_channel(int(nameOrID))
        else:
            for channel in guild.channels:
                if channel.name == nameOrID or str(channel.name) in nameOrID:
                    return channel
    elif type(nameOrID) is int:
        return guild.get_channel(nameOrID)
    else:
        return None

async def getCategory(nameOrID,guild):
    return await getChannel(nameOrID,guild)
