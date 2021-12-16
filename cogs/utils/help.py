## Initialisation
import lib
import discord

from discord.ext import commands, tasks

## Define help cog
class help(commands.Cog):
    ## Initialose with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = f"Display help about {self.bot.user.name}'s commands"
        self.usage = f"""
        {self.bot.command_prefix}help
        {self.bot.command_prefix}help <command>
        """
        self.forbidden = False
        
    ## Callable command to provide user help with command usage
    @commands.command(aliases=["?"])
    async def help(self, ctx, *args):
        embed=False
        prefix = self.bot.command_prefix
        ## Provide specific help, or general command list
        if (args) :
            cog = self.bot.get_cog(args[0])
            command = self.bot.get_command(args[0])
            if not (cog):
                pass
            ## Gather usage info about command
            elif (not cog.forbidden):
                embed=lib.embed(
                    title=cog.qualified_name,
                    description=cog.description,
                    sections=[("Usage",cog.usage),("Category",cog.category)]
                )
                if (command.aliases):
                    embed.set_footer(text=f'Aliases: {", ".join(command.aliases)}')
        else:
            cogs = {}
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if (not cog.forbidden):
                    if not (cog.category in cogs.keys()):
                        cogs[cog.category] = []
                    cogs[cog.category].append(f"`{cog.qualified_name}`\n> {cog.description}")
            ## Display list of commands and descriptions
            embed=lib.embed(
                title="List of commands:",
                footer=f"Use {self.bot.command_prefix}help <command> to get more specific usage information."
            )
            for category in cogs.keys():
                embed.add_field(name=category,value="\n".join(cogs[category]))
                
        if not (embed):   
            embed=lib.embed(
                title="This command does not exist",
                description=f"Try {self.bot.command_prefix}help to see a list of available commands."
            )       
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(help(bot))
