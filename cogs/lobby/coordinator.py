## Initialization
import lib
import discord
import asyncio

from math import ceil
from discord.ext import commands,tasks

## Class setup
class coordinator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        ## Help stuff
        self.category = lib.getCategory(self.__module__)
        self.description = 'Game coordinator'
        self.usage = f"""
        This module will take users from the queue and sort them into lobbies.
        """
        self.forbidden = False

        self.coordinator.start()

    def cog_unload(self):
        self.coordinator.cancel()        

    @commands.command()
    async def settings(self, ctx, *args):
        await ctx.message.reply("wip")

    ## Button listeners
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx, *args):
        await self.setQueueState(ctx)
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx, *args):
        await self.setQueueState(ctx)

    ## Add or remove user from queue on button press        
    async def setQueueState(self, ctx):
        if ctx.user_id == self.bot.user.id:
            return
        guild = self.bot.get_guild(ctx.guild_id)
        ## Check for existing guild config
        try:
            guildVars = self.bot.guildVars[str(guild.id)]
        except KeyError:
            return    
        if ctx.message_id != guildVars["queueEmbed"][1]:
            return
        if ctx.user_id in guildVars["queue"]:
            await self.dequeue(ctx.user_id, guild)
        else:
            await self.enqueue(ctx.user_id, guild)

    async def enqueue(self, userID, guild):
        guildVars = self.bot.guildVars[str(guild.id)]
        guildVars["queue"].append(userID)

    async def dequeue(self, userID, guild):
        guildVars = self.bot.guildVars[str(guild.id)]
        for i in range(len(guildVars["queue"])):
            if guildVars["queue"][i] == userID:
                guildVars["queue"].pop(i)

    @tasks.loop(seconds=5)
    async def coordinator(self):
        for guildID in self.bot.guildVars.keys():
            guildVars = self.bot.guildVars[guildID]
            guild = self.bot.get_guild(int(guildID))
            lobbies = guildVars["lobbies"]
            queue = guildVars["queue"]

            ## Clean up lobbies
            l = 0
            while l < len(lobbies):
                lobby = lobbies[l]
                ## Ensure Bot's lobby is synced with users in chat
                connected = list(map(lambda m: m.id, lobby.channel.members))
                lobby.players = connected
                ## Prune empty
                if len(lobby.players) < 1:
                    await lobby.channel.delete()
                    lobbies.pop(l)
                else:
                    l += 1



            ## Bail early if no one is waiting
            if len(queue) < 1:
                return

            ## Fill currently active lobbies to playercap
            for lobby in lobbies:
                while len(lobby.players) < guildVars["playerCap"] and len(queue) > 0:
                    player = queue.pop(0)
                    lobby.players.append(player)
                    member = await guild.fetch_member(player)
                    try:
                        await member.move_to(lobby.channel)
                    except discord.errors.HTTPException:
                        channel = await lib.apiWrappers.getChannel(guildVars["queueEmbed"][0], guild)
                        message = await channel.send(f"{member.mention}, You need to be in the voice chat to queue!")
                        await asyncio.sleep(5)
                        await message.delete()


            newLobbiesNeeded = ceil(len(queue)/guildVars["playerCap"])
            for i in range(newLobbiesNeeded):
                players = []
                category = await lib.apiWrappers.getCategory(guildVars["queueCategory"], guild)
                channel = await guild.create_voice_channel(
                    f"{guildVars['gameChannel']}",
                    overwrites={guild.default_role:discord.PermissionOverwrite(connect=False)},
                    category=category,
                    user_limit=guildVars["playerCap"]    
                )
                while len(players) < guildVars["playerCap"] and len(queue) > 0:
                    player = queue.pop(0)
                    players.append(player)
                    member = await guild.fetch_member(player)
                    try:
                        await member.move_to(channel)
                        guildVars["lobbies"].append(lib.lobby(channel,players))
                    except discord.errors.HTTPException:
                        textChannel = await lib.apiWrappers.getChannel(guildVars["queueEmbed"][0], guild)
                        message = await textChannel.send(f"{member.mention}, You need to be in the voice chat to queue!")
                        await channel.delete()
                        await asyncio.sleep(5)
                        await message.delete()
            
            

    @coordinator.before_loop
    async def before_coordinator(self):
        await self.bot.wait_until_ready()
        for guildID in self.bot.guildVars.keys():
            guildVars = self.bot.guildVars[guildID]
            guild = self.bot.get_guild(int(guildID))
            category = lib.apiWrappers.getCategory(guildVars["queueCategory"], guild)
            for channel in category.channels:
                if channel.id != guildVars["queueChannel"]:
                    await channel.delete()
    

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(coordinator(bot))