## Initialisation
import lib
import discord

from discord.ext import commands, tasks

## Define reactionRole cog
class reactionRole(commands.Cog):
    ## Initialise with help info
    def __init__(self, bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = f"Allow users to react to a message to self-assign roles"
        self.usage = f"""
        {self.bot.command_prefix}reactionRole <role name|role ID|@role> <emoji> [<role name|role ID|@role> <emoji>]...
        """
        self.forbidden = False

    ## Callable command to set up reaction role.
    @commands.command(aliases=["reactionRoles"])
    @commands.has_guild_permissions(administrator=True)
    async def reactionRole(self, ctx, *args):
        guild = ctx.guild

        ## Check for existing guild config
        try:
            guildconf = self.bot.guildConf[str(guild.id)]
        except KeyError:
            self.bot.guildConf[str(guild.id)] = {
                "selfrole":{},
                "joinrole":[]
            }
            guildconf = self.bot.guildConf[str(guild.id)]

        ## Check for existing reactionRole message, and remove it if present
        if "msgID" in guildconf["selfrole"].keys():
            channel = guild.get_channel(guildconf["selfrole"]["msgID"][0])
            if (channel):     
                try:  
                    message = await channel.fetch_message(guildconf["selfrole"]["msgID"][1])
                    await message.delete()
                except:
                    pass

        ## Generate role : emoji map from provided arguments
        roleString = ""
        for i in range(0,len(args),2):
            role = await lib.role.getRole(args[i], guild)
            guildconf["selfrole"][args[i+1]] = role.id
            roleString += f"{args[i+1]} : {role.mention}\n"

        ## Send message and add reactions  
        embed = lib.embed(
            title="React to assign yourself a role",
            description=roleString
        )
        reply = await ctx.send(embed=embed)
        guildconf["selfrole"]["msgID"] = (reply.channel.id,reply.id)
        for emoji in guildconf["selfrole"].keys():
            if emoji != "msgID":
                await reply.add_reaction(emoji)

        ## Delete call
        await ctx.message.delete()
        
    ## Listner to add roles to users
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,ctx, *args):
        if ctx.user_id == self.bot.user.id:
            return
        guild = self.bot.get_guild(ctx.guild_id)
        ## Check for existing guild config
        try:
            guildconf = self.bot.guildConf[str(guild.id)]
        except KeyError:
            return    
        if ctx.message_id != guildconf["selfrole"]["msgID"][1]:
            return
        role = await lib.role.getRole(guildconf["selfrole"][ctx.emoji.name],guild)
        await ctx.member.add_roles(role)


    ## Listener to remove roles from user  
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx, *args):
        if ctx.user_id == self.bot.user.id:
            return
        guild = self.bot.get_guild(ctx.guild_id)
        ## Check for existing guild config
        try:
            guildconf = self.bot.guildConf[str(guild.id)]
        except KeyError:
            return    
        if ctx.message_id != guildconf["selfrole"]["msgID"][1]:
            return
        role = await lib.role.getRole(guildconf["selfrole"][ctx.emoji.name],guild)
        await guild.get_member(ctx.user_id).remove_roles(role)

    ## Hiden force json save for debug  
    @commands.command()
    @commands.is_owner()
    async def saveGuildconf(self, ctx):
        self.bot.shutdown()
        await ctx.send(embed = lib.embed(
            title="guildconf saved"
        ))
    

def setup(bot):
    bot.add_cog(reactionRole(bot))
