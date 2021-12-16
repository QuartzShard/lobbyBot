## Initialisation
import discord
from discord.ext import commands, tasks

## Cog utility commands
class cogUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forbidden = True
    
    ## Reload a cog
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, name: str):
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog reloaded')

    ## Unload a cog
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, name: str):
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog unloaded')

    ## Load a new cog
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, name: str):
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f'"**{name}**" Cog loaded')

## Allow use of cog class by main bot instance
def setup(bot):
    bot.add_cog(cogUtils(bot))
