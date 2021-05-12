import discord
from discord.ext import commands


def GetBearerToken():
    bearer_token = "NOT LOADED"
    with open("Bearer_token.txt", "r") as file:
        bearer_token = file.readline()
    return bearer_token


class Mate:
    name = ""
    group_id = -1
    
    def __init__(self, name, group_id = -1):
        self.name = name
        self.group_id = group_id


client = commands.Bot(command_prefix = '!')
TOKEN = GetBearerToken()


async def GetClassMates(file_path):
    mates = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file.read().splitlines():
            infos = line.split(';')
            mate = Mate(infos[0], int(infos[1]))
            mates.append(mate)
    return mates


def GetAbsentNames(names, mates, group = 0):
    return [x.name for x in mates if (x.name not in names and (x.group_id == group or group == 0))]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    
@client.command()
async def absent(ctx, group_arg = 0):
    try:
        voice_channel = ctx.author.voice.channel
    except:
        await ctx.channel.send("You aren't in a Voice channel\nPlease connect to a Voice Channel!")
        return
    group = int(group_arg)
    mates = await GetClassMates("classmates.txt")
    in_voice_names = []
    for member in voice_channel.members:
        in_voice_names.append(member.display_name)
    absent_names = GetAbsentNames(in_voice_names, mates, group)
    str_absent_names = ""
    if len(absent_names) == 0:
        str_absent_names = "Nobody is Absent!"
    else:
        for name in absent_names:
            str_absent_names += "@" + name + "\n" 
    await ctx.channel.send(str_absent_names)
   
   
client.run(TOKEN)
