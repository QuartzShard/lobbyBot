## Initialisation
import os
import re
import json
import atexit
import discord
import lib 
from discord.ext import commands

## Constants and Config
intents = discord.Intents.default()
intents.members = lib.cfg['discord']['intents']['members']
intents.guilds = lib.cfg['discord']['intents']['guilds']
intents.reactions = lib.cfg['discord']['intents']['reactions']

## Define lobbyBot bot class
class lobbyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
        ## Remove default help command to replace with custom one
        self.remove_command('help')
        
        ## Retrieve queue setups for guilds
        try:
            with open("guildVars.json","r") as file:
                self.guildVars = json.load(file)
        except FileNotFoundError:
            self.guildVars = {}
            
        ## Load Cogs
        for root, subdirs, files in os.walk("./cogs"):
            if not ("__pycache__" in root):
                for file in files:
                    if file.endswith(".py") and not (file == "help.py" or file == "about.py"):
                        name = file[:-3]
                        parent = ".".join(re.findall(r"\w+",root))
                        self.load_extension(f"{parent}.{name}")

    ## Post login activity
    async def on_ready(self):
        ## Load commands that require login to init
        self.load_extension("cogs.utils.help")
        self.load_extension("cogs.utils.about")
        ## Log ready
        lib.log('--------------------------------')
        lib.log('Bot Ready.')
        lib.log(f'Logged in as {self.user.name}')
        lib.log(f'User ID: {self.user.id}')
        lib.log('--------------------------------')

    ## Setup guildVars for new guild
    async def on_guild_join(self, guild):
        self.guildVars[str(guild.id)] = lib.guildVarsSkel
    
    ## Dump guildVars on guild remove
    async def on_guild_remove(self,guild):
        del self.guildVars[str(guild.id)]
    
    ## Inform user of error
    async def on_command_error(self, ctx, err):
        embed=lib.embed(
            title="Error running command:",
            description=err.args[0],
            colour=lib.errorColour
        )
        await ctx.send(embed=embed)

    ## Store current state of guildVars in a json on shutdown to persist over restarts
    def shutdown(self):
        for guild in self.guildVars.keys():
            self.guildVars[guild]["lobbies"] = []
        with open("guildVars.json","w+") as file:
            json.dump(self.guildVars,file)

## Create an instance of the bot
botClient = lobbyBot(lib.cfg['options']['prefix'], intents=intents)
atexit.register(botClient.shutdown)

# Login and run the bot using the provided token
botClient.run(lib.cfg['discord']['token'])