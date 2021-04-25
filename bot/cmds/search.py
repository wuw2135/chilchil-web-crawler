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


def format_(list_detail):
    embed=discord.Embed(title=list_detail["title"], url=list_detail["title_url"], description=list_detail["description"], color=0xa92acf)
    embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
    embed.set_image(url=list_detail["jpg_url"])
    if list_detail["date_text"] != "":
        embed.add_field(name="発売日", value=list_detail["date_text"], inline=False)
    if list_detail["seme X uke"] != " → ":
        list_detail["seme X uke"] = list_detail["seme X uke"].replace("/ ","\n").replace("*","")
        embed.add_field(name="攻 X 受", value=list_detail["seme X uke"], inline=False)
    else:
        embed.add_field(name="攻 X 受", value="無", inline=False)
    if list_detail["other"]!= "":
        embed.add_field(name="その他キャラ", value=list_detail["other"], inline=False)
    if list_detail["ero"] != "":
        embed.add_field(name="エロ度", value=list_detail["ero"], inline=False)
    if list_detail["plays"] != "":
        embed.add_field(name="プレイ", value=list_detail["plays"], inline=False)
    if list_detail["settings"] != "":
        embed.add_field(name="設定", value=list_detail["settings"], inline=False)
    return embed

def format_sec(list_detail):
    if list_detail["HP_link"] == "None" and list_detail["twitter_link"] == "None":
        embed=discord.Embed(title=list_detail["name"], url=list_detail["name_url"], description="None Social Media", color=0xa92acf)
        embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")    
    else:
        embed=discord.Embed(title=list_detail["name"], url=list_detail["name_url"], description="HP\n"+list_detail["HP_link"]+"\n\nTwitter\n"+list_detail["twitter_link"], color=0xa92acf)   
        embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
    if list_detail["title_url"] == "javascript:void(0)":
        embed.add_field(name="作品数", value=list_detail["title_count"], inline=False)
    else:
        embed.add_field(name="作品数", value=list_detail["title_count"]+"\n"+list_detail["title_url"], inline=False)
    if list_detail["seme_url"] == "javascript:void(0)":
        embed.add_field(name="攻め作品", value=list_detail["seme_count"], inline=False)
    else:
        embed.add_field(name="攻め作品", value=list_detail["seme_count"]+"\n"+list_detail["seme_url"], inline=False)
    if list_detail["uke_url"] == "javascript:void(0)":
        embed.add_field(name="受け作品", value=list_detail["uke_count"], inline=False)
    else:
        embed.add_field(name="受け作品", value=list_detail["uke_count"]+"\n"+list_detail["uke_url"], inline=False)
    return embed

def rightnowtime():
    time = datetime.now().strftime('%Y-%m-%d')
    return time


def list_format(list_detail,title_name):
    for i in range (int(len(list_detail)/20)):
        embed=discord.Embed(title=title_name,color=0x881db9)
        embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
        for j in range(20):
            embed.add_field(name=eval(list_detail[j])["title"], value=eval(list_detail[j])["title_url"], inline=False)
        del list_detail[:20]
        return embed

def simple_format(reply=str):
    embed=discord.Embed(title=reply,color=0xa92acf)
    return embed

def user_search_format(list_detail):
    seiyuus = ""
    albums = ""
    embed=discord.Embed(title="Search Result",color=0xa92acf)
    for j in range (len(list_detail["seiyuus"])):
        seiyuus = seiyuus + list_detail["seiyuus"][j] + "\n"
    embed.add_field(name="Seiyuu", value=seiyuus, inline=False)

    for p in range (len(list_detail["albums"])):
        for n in range (len(data)):
            if list_detail["albums"][p] == data[n]["title"]:
                albums = albums + data[n]["title"] + "\n" + data[n]["title_url"] + "\n"
                break
    embed.add_field(name="Albums", value=albums, inline=False)
    return embed


class Search(Cog_Extension):
    #---------------------------search features---------------------------------
    @commands.command()
    async def norsearch(self,ctx, *args):
        data_str = []
        for i in range (len(data)):
            data_str.append(str(data[i]))

        def select(arg):
            specific_range = []
            for i in range(len(data_str)):
                if arg in data_str[i]:
                    specific_range.append(data_str[i])
            return(set(specific_range))

    
        finalrange = set()
        index = 0
        for arg in args:
            index = index + 1
            if index == 1:
                finalrange = select(arg)
            else:
                finalrange = finalrange & select(arg)

        finallist = list(finalrange)

        if len(finallist) == 1:
            await ctx.channel.send(ctx.message.author.mention,embed=format_(eval(finallist[0])))
        else:
            if len(finallist) > 20:
                await ctx.channel.send(ctx.message.author.mention,embed=list_format(finallist,"Search Result"))
            
            if len(finallist) > 0:
                embed=discord.Embed(title="Search Result",color=0x881db9)
                embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
                for i in range (len(finallist)):
                    embed.add_field(name=eval(finallist[i])["title"], value=eval(finallist[i])["title_url"], inline=False)
                await ctx.channel.send(ctx.message.author.mention,embed=embed)


    @commands.command()
    async def seisearch(self,ctx, arg):
        for i in range(len(data_sec)):
            if arg in str(data_sec[i]):
                await ctx.channel.send(ctx.message.author.mention,embed=format_sec(data_sec[i]))

    @commands.command()
    async def followsearch(self,ctx):
        with open("user_record.json","r",encoding="utf-8") as file:
            user_document = json.load(file)

        detial = {
            "user_id" : ctx.message.author.id,
            "seiyuus" : [],
            "albums" : []
        }

        if str(ctx.message.author.id) not in str(user_document):
            user_document.append(detial)
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format("Didn't register,Filed"))
            return 0

        
        for i in range (len(user_document)):
            if str(ctx.message.author.id) in str(user_document[i]):
                await ctx.channel.send(ctx.message.author.mention,embed=user_search_format(user_document[i]))


def setup(bot):
    bot.add_cog(Search(bot))