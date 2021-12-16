## Initialisation
import lib
import discord

from discord.ext import commands, tasks

## Define about cog
class about(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = f"Display information about {self.bot.user.name}"
        self.usage = f"""
        {self.bot.command_prefix}about
        """
        self.forbidden = False
        
    ## Callable command to provide info about bot
    @commands.command()
    async def about(self, ctx, *command):
        embed=lib.embed(
            title="About lobbyBot",
            description="A p2p multiplayer lobby helper. Find us on github!",
            url="https://github.com/QuartShard/roleman",
            thumbnail=True
        )
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(about(bot))
