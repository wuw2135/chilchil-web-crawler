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

#---------------------------format setting---------------------------------
def simple_format(reply=str):
    embed=discord.Embed(title="Running Result", description=reply ,color=0xa92acf)
    return embed

class Follow(Cog_Extension):
    #---------------------------follow add---------------------------------
    @commands.command()
    async def seifollow(self,ctx, *args):
        with open("user_record.json","r",encoding="utf-8") as file:
            user_document = json.load(file)
        
        detial = {
            "user_id" : ctx.message.author.id,
            "seiyuus" : [],
            "albums" : []
        }

        if str(ctx.message.author.id) not in str(user_document):
            user_document.append(detial)

        args = list(args)

        didntexist_list = []
        success_list = []
        for index, arg in enumerate(args):
            appear = 0
            flag = 0
            if arg not in str(data_sec):
                didntexist_list.append(arg)
                flag = 1
            for i in range (len(data_sec)):
                if arg in str(data_sec[i]):
                    args[index] = data_sec[i]["name"].split("\n")[0]
                    appear = appear + 1 
            if appear >= 2:
                didntexist_list.append(arg)
                flag = 1
            if flag == 0:
                success_list.append(args[index])
        
        pd.unique(success_list).tolist()

        add_list = []
        exist_list = []
        for i in range (len(user_document)):
            for thing in success_list:
                if str(ctx.message.author.id) in str(user_document[i]):
                    if thing in str(user_document[i]["seiyuus"]):
                        exist_list.append(thing)
                    else:
                        user_document[i]["seiyuus"].append(thing)
                        add_list.append(thing)

        finalmeg = ""
        existmeg = ""
        if len(exist_list) > 0:
            for i in range (len(exist_list)):
                existmeg = existmeg + exist_list[i] + "、"
            finalmeg = finalmeg + existmeg.removesuffix("、") + " Already Exist" + "\n"

        didntexistmeg = ""
        if len(didntexist_list) > 0:
            flag = 2
            for i in range (len(didntexist_list)):
                didntexistmeg = didntexistmeg + didntexist_list[i] + "、"
            finalmeg = finalmeg + didntexistmeg.removesuffix("、") + " Didn't Exist" +  "\n"
        
        addmeg = ""
        if len(add_list) > 0:
            if flag == 1:
                flag = 2
            for i in range (len(add_list)):
                addmeg = addmeg + add_list[i] + "、"
            finalmeg = finalmeg + addmeg.removesuffix("、") + " Register Finished"

        
        await ctx.channel.send(ctx.message.author.mention,embed=simple_format(finalmeg))

        with open("user_record.json","w",encoding="utf-8") as file:
            file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
        
        

    @commands.command()
    async def albfollow(self,ctx, *args):
        with open("user_record.json","r",encoding="utf-8") as file:
            user_document = json.load(file)
        
        detial = {
            "user_id" : ctx.message.author.id,
            "seiyuus" : [],
            "albums" : []
        }

        if str(ctx.message.author.id) not in str(user_document):
            user_document.append(detial)

        args = list(args)

        didntexist_list = []
        success_list = []
        for index, arg in enumerate(args):
            appear = 0
            flag = 0
            if arg not in str(data):
                didntexist_list.append(arg)
                flag = 1
            for i in range (len(data)):
                if arg in str(data[i]):
                    args[index] = data[i]["title"]
                    appear = appear + 1 
            if appear >= 2:
                didntexist_list.append(arg)
                flag = 1
            if flag == 0:
                success_list.append(args[index])
        
        pd.unique(success_list).tolist()

        add_list = []
        exist_list = []
        for i in range (len(user_document)):
            for thing in success_list:
                if str(ctx.message.author.id) in str(user_document[i]):
                    if thing in ', '.join(map(str, user_document[i]["albums"])):
                        exist_list.append(thing)
                    else:
                        user_document[i]["albums"].append(thing)
                        add_list.append(thing)

        finalmeg = ""
        existmeg = ""
        if len(exist_list) > 0:
            for i in range (len(exist_list)):
                existmeg = existmeg + exist_list[i] + "、"
            finalmeg = finalmeg + existmeg.removesuffix("、") + " Already Exist" + "\n"

        didntexistmeg = ""
        if len(didntexist_list) > 0:
            flag = 2
            for i in range (len(didntexist_list)):
                didntexistmeg = didntexistmeg + didntexist_list[i] + "、"
            finalmeg = finalmeg + didntexistmeg.removesuffix("、") + " Didn't Exist" +  "\n"
        
        addmeg = ""
        if len(add_list) > 0:
            if flag == 1:
                flag = 2
            for i in range (len(add_list)):
                addmeg = addmeg + add_list[i] + "、"
            finalmeg = finalmeg + addmeg.removesuffix("、") + " Register Finished"

        
        await ctx.channel.send(ctx.message.author.mention,embed=simple_format(finalmeg))

        with open("user_record.json","w",encoding="utf-8") as file:
            file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
        
        
                

    #---------------------------follow del---------------------------------        
    @commands.command()
    async def seifollowdel(self,ctx, arg):
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

        if arg not in str(data_sec):
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Didn't Exist"))
            return 0

        appear = 0
        for i in range (len(data_sec)):
            if arg in str(data_sec[i]):
                arg = data_sec[i]["name"].split("\n")[0]
                appear = appear + 1 
        if appear >= 2:
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Didn't Exist"))
            return 0


        for i in range (len(user_document)):
            if str(ctx.message.author.id) in str(user_document[i]):
                if arg in str(user_document[i]["seiyuus"]):
                    user_document[i]["seiyuus"].remove(arg)
                else:
                    await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Didn't Exist"))
                    return 0

        
        with open("user_record.json","w",encoding="utf-8") as file:
            file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
        
        await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Delete Finished"))

    @commands.command()
    async def albfollowdel(self,ctx, arg):
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

        if arg not in str(data):
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Didn't Exist"))
            return 0

        appear = 0
        for i in range (len(data)):
            if arg in str(data[i]):
                arg = data[i]["title"]
                appear = appear + 1 
        if appear >= 2:
            await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Didn't Exist"))
            return 0

        for i in range (len(user_document)):
            if str(ctx.message.author.id) in str(user_document[i]):
                if arg in ', '.join(map(str, user_document[i]["albums"])):
                    user_document[i]["albums"].remove(arg)
                else:
                    await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" have yet to follow"))
                    return 0

        
        with open("user_record.json","w",encoding="utf-8") as file:
            file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
        
        await ctx.channel.send(ctx.message.author.mention,embed=simple_format(arg+" Delete Finished"))


def setup(bot):
    bot.add_cog(Follow(bot))