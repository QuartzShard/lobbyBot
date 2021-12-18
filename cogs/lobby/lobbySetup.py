## Initialization
import lib
import discord

from discord.ext import commands, tasks

## Class setup
class lobbySetup(commands.Cog):
    ## Initialise with help info
    def __init__(self, bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = f"Configure the bot to use a set of channels"
        self.usage = f"""
        {self.bot.command_prefix}lobbySetup <queueChannel> <gameChannel> <playerCap> [<category>]

        queueChannel is the name of the voice channel users should join to be moved into a game channel
        gameChannel is the name of the voice channel the bot should make, and will be appended with a number (e.g, "Lobby" will result in channels named "Lobby 1, Lobby 2)
        playerCap is the number of players each lobby should hold
        category is an optional argument that specifies the channel category to create lobbies under

        """
        self.forbidden = False

        self.updateInfo.start()

    def cog_unload(self):
        self.updateInfo.cancel()

    ## Callable command to set up reaction role.
    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def lobbySetup(self, ctx, *args):
        guild = ctx.guild

        ## Check for existing guild config
        try:
            guildVars = self.bot.guildVars[str(guild.id)]
        except KeyError:
            self.bot.guildVars[str(guild.id)] = lib.guildVarsSkel
            guildVars = self.bot.guildVars[str(guild.id)]

        ## Check for existing reactionRole message, and remove it if present
        if guildVars["queueEmbed"]:
            channel = guild.get_channel(guildVars["queueEmbed"][0])
            if (channel):     
                try:  
                    message = await channel.fetch_message(guildVars["queueEmbed"][1])
                    await message.delete()
                except:
                    pass

        ## Setup channels
        guildVars["queueChannel"] = (await lib.apiWrappers.getChannel(args[0], guild)).id
        guildVars["gameChannel"] = args[1]
        guildVars["playerCap"] = int(args[2])
    
        guildVars["queueCategory"] = (await lib.apiWrappers.getCategory(args[3],guild)).id
        
        ## Send message and add reactions  
        embed = lib.embed(
            title="React to join the queue!",
            sections=[
                ("Players in queue:",f"{len(guildVars['queue'])}"),
                ("Currently open lobbies:",f"{len(guildVars['lobbies'])}")
            ]
        )
        reply = await ctx.send(embed=embed)
        guildVars["queueEmbed"] = (reply.channel.id,reply.id)
        await reply.add_reaction("🎟️")

        ## Delete call
        await ctx.message.delete()
        
    ## Update lobby info
    @tasks.loop(seconds=5)
    async def updateInfo(self):
        for guildID in self.bot.guildVars.keys():
            guildVars = self.bot.guildVars[guildID]
            guild = self.bot.get_guild(int(guildID))
            if guildVars["queueEmbed"]:
                channel = guild.get_channel(guildVars["queueEmbed"][0])
                message = await channel.fetch_message(guildVars["queueEmbed"][1])
                embed = lib.embed(
                    title="React to join the queue!",
                    sections=[
                        ("Players in queue:",f"{len(guildVars['queue'])}"),
                        ("Currently open lobbies:",f"{len(guildVars['lobbies'])}")
                    ]
                )
                await message.edit(embed=embed)
    @updateInfo.before_loop
    async def before_updateInfo(self):
        await self.bot.wait_until_ready()

    ## Hiden force json save for debug  
    @commands.command()
    @commands.is_owner()
    async def saveguildVars(self, ctx):
        self.bot.shutdown()
        await ctx.send(embed = lib.embed(
            title="guildVars saved"
        ))

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(lobbySetup(bot))