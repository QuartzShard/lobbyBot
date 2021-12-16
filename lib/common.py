## Initialisation
import datetime
import re
import yaml
from discord import Embed, Color, Colour

## Exported values
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
hr="─────────────────────────────────────────────────"
defaultColour = Colour.from_rgb(**cfg['options']['embed']['colour']['default'])
errorColour = Colour.from_rgb(**cfg['options']['embed']['colour']['error'])

## Log to console and/or file with timestamp, based on config contents
def log(event):
    now = datetime.datetime.now().strftime("%d,%m,%y %H:%M:%S")
    if cfg['options']['logging']['logToConsole']:
        print(f'[{now}]:{event}')
    if cfg['options']['logging']['logToFile']:
        with open(cfg['options']['logging']['logFilePath'],"a") as logFile:
            logFile.write(f'[{now}]:{event}')

## Helper function for using message embeds
def embed(**kwargs):
    """
    Created an embed from the provided details
    title - Title of embed
    description - Text in embed, pre body
    sections - list of (title,content) tuples
    body - list of entries to be seperated by a <hr>, follows sections
    colour - discord.Colour object to ovveride default
    url - webpage to link to
    thumbnail - boolean to display roleman thumbnail
    footer - Text to put at the bottom of the embed
    """
    
    embed=Embed()

    ## Check for present kwargs and edit embed accordingly
    if ("title" in kwargs.keys()):
        embed.title = kwargs["title"]
    if ("description" in kwargs.keys()):
        embed.description = kwargs["description"]
    if ("sections" in kwargs.keys()):
        for elem in kwargs["sections"]:
            embed.add_field(name=elem[0],value=elem[1])
    if ("body" in kwargs.keys()):
        for elem in kwargs["body"]:
            embed.add_field(name=hr,value=elem, inline=False)
        #now = datetime.datetime.now().strftime("%H:%M")
        #embed.add_field(name=hr,value=f"Request fulfilled at {now}",inline=False)
    if ("colour" in kwargs.keys()):
        embed.colour = kwargs["colour"]
    elif ("color" in kwargs.keys()):
        embed.color = kwargs["color"] 
    else:
        embed.colour = defaultColour
    if ("url" in kwargs.keys()):
        embed.url = kwargs["url"]
    if ("thumbnail" in kwargs.keys()):
        if kwargs["thumbnail"]:
            embed.set_image(url=cfg['options']['embed']['thumbnail'])
    if ("footer" in kwargs.keys()):
        embed.set_footer(text=kwargs["footer"])
    return embed

def getCategory(module):
    try:
        category = re.search(r"cogs\.(\w+)\.",module).groups()[0]
    except AttributeError:
        category = "Misc"
    return category