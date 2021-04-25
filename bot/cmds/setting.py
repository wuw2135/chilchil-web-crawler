import discord
from discord.ext import commands
import json
from datetime import datetime
import pandas as pd
from core.classes import Cog_Extension

with open("D:/notifiction_bot/BlCD/BLCD_data.json","r",encoding="utf-8") as file:
    data = json.load(file)

with open("D:/notifiction_bot/Seiyuu/SEIYUU_data.json","r",encoding="utf-8") as file:
    data_sec = json.load(file)

with open("D:/notifiction_bot/BlCD/update_data.json","r",encoding="utf-8") as file:
    data_update = json.load(file)

class Setting(Cog_Extension):
    #---------------------------update channel setting---------------------------------
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channelset(self,ctx, *, given_name=None):
        wanted_id = int()
        for channel in ctx.guild.channels:
            if channel.name == given_name:
                wanted_id = channel.id
        
        if wanted_id == 0:
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format("Channel Didn't Exist"))
            return 0
                
        with open("server_list.json","r",encoding="utf-8") as file:
            serverdata = json.load(file)
        
        server_detail ={
            "server_id" : ctx.message.guild.id,
            "channel_id" : wanted_id
        }

        if str(ctx.message.guild.id) not in str(serverdata):
            serverdata.append(server_detail)
            with open("server_list.json","w",encoding="utf-8") as file:
                file.write(json.dumps(serverdata,ensure_ascii=False,indent=1))
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format("Setting Finished"))
        else:
            for i in range (len(serverdata)):
                if str(ctx.message.guild.id) == str(serverdata[i]["server_id"]):
                    serverdata[i]["channel_id"] = wanted_id
                    with open("server_list.json","w",encoding="utf-8") as file:
                        file.write(json.dumps(serverdata,ensure_ascii=False,indent=1))
                    await ctx.channel.send(ctx.message.author.mention,embed=simple_format("Change Finished"))
                    break

def simple_format(reply=str):
    embed=discord.Embed(title=reply,color=0xa92acf)
    return embed

def setup(bot):
    bot.add_cog(Setting(bot))