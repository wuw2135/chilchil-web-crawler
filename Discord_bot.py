import discord
from discord.ext import commands
import json
from datetime import datetime
import pandas as pd

with open("./BlCD/BLCD_data.json","r",encoding="utf-8") as file:
    data = json.load(file)

with open("./Seiyuu/SEIYUU_data.json","r",encoding="utf-8") as file:
    data_sec = json.load(file)

with open("./BlCD/update_data.json","r",encoding="utf-8") as file:
    data_update = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("Bot已經上線!")
    channel = bot.get_channel(channel_ID)
    
    if len(data_update) == 1:
        await channel.send("@everyone",embed = format_(data_update[0]))
    else:
        if len(data_update) > 20:
            await channel.send("@everyone",embed=list_format(data_update,"更新"))
        
        if len(data_update) > 0:
            embed=discord.Embed(title="更新",color=0x881db9)
            embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
            for i in range (len(data_update)):
                embed.add_field(name=data_update[i]["title"], value=data_update[i]["title_url"], inline=False)
            await channel.send("@everyone",embed=embed)

    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    
    for i in range (len(user_document)):
        userid = user_document[i]["user_id"]
        new_sale = []
        new_release = []
        for j in range (len(user_document[i]["seiyuus"])):
            for n in range (len(data)):
                if user_document[i]["seiyuus"][j] in str(data[n]) and data[n]["date"] == rightnowtime():
                    new_sale.append(str(data[n]))
            for o in range (len(data_update)):
                if user_document[i]["seiyuus"][j] in str(data_update[o]):
                    new_release.append(str(data_update[o]))
        for j in range (len(user_document[i]["albums"])):
            for n in range (len(data)):
                if user_document[i]["albums"][j] in str(data[n]) and data[n]["date"] == rightnowtime():
                    new_sale.append(str(data[n]))
            for o in range (len(data_update)):
                if user_document[i]["albums"][j] in str(data_update[o]):
                    new_release.append(str(data_update[o]))
        
        pd.unique(new_sale).tolist()
        pd.unique(new_release).tolist()

        for i in range (len(new_sale)):
            new_sale[i] = eval(new_sale[i])
        
        for i in range (len(new_release)):
            new_release[i] = eval(new_release[i])
    
        _user = await bot.fetch_user(userid)
        if len(new_sale) == 1:
            await _user.send("新發售",embed = format_(new_sale[0]))
        if len(new_sale) > 1:
            await _user.send("新發售",embed = list_format(new_sale,"通知"))
        
        if len(new_release) == 1:
            await _user.send("新作品",embed = format_(new_release[0]))
        if len(new_release) > 1:
            await _user.send("新作品",embed = list_format(new_release,"通知"))

    

#format
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

#search
@bot.command()
async def norsearch(ctx, *args):
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
        await ctx.channel.send("{}".format(ctx.message.author.mention),embed=format_(eval(finallist[0])))
    else:
        if len(finallist) > 20:
            await ctx.channel.send("{}".format(ctx.message.author.mention),embed=list_format(finallist,"搜尋結果"))
        
        if len(finallist) > 0:
            embed=discord.Embed(title="搜尋結果",color=0x881db9)
            embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
            for i in range (len(finallist)):
                embed.add_field(name=eval(finallist[i])["title"], value=eval(finallist[i])["title_url"], inline=False)
            await ctx.channel.send("{}".format(ctx.message.author.mention),embed=embed)


@bot.command()
async def seisearch(ctx, arg):
    for i in range(len(data_sec)):
        if arg in str(data_sec[i]):
            await ctx.channel.send("{}".format(ctx.message.author.mention),embed=format_sec(data_sec[i]))

@bot.command()
async def followsearch(ctx):
    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)

    detial = {
        "user_id" : ctx.message.author.id,
        "seiyuus" : [],
        "albums" : [],
    }

    if str(ctx.message.author.id) not in str(user_document):
        user_document.append(detial)
        await ctx.channel.send("{} 尚未註冊,已建檔".format(ctx.message.author.mention))
        return 0

    seiyuus = ""
    albums = ""
    for i in range (len(user_document)):
        if str(ctx.message.author.id) in str(user_document[i]):
            for j in range (len(user_document[i]["seiyuus"])):
                seiyuus = seiyuus + user_document[i]["seiyuus"][j] + "、"
            for p in range (len(user_document[i]["albums"])):
                albums = albums + user_document[i]["albums"][p] + "、"

    await ctx.channel.send("{} \n 聲優: {} \n 作品: {}".format(ctx.message.author.mention,seiyuus.removesuffix("、"),albums.removesuffix("、")))

@bot.command()
async def seifollow(ctx, *args):
    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    detial = {
        "user_id" : ctx.message.author.id,
        "seiyuus" : [],
        "albums" : [],
    }

    if str(ctx.message.author.id) not in str(user_document):
        user_document.append(detial)

    args = list(args)

    didntexist = []
    success_list = []
    for index, arg in enumerate(args):
        appear = 0
        flag = 0
        if arg not in str(data_sec):
            didntexist.append(arg)
            flag = 1
        for i in range (len(data_sec)):
            if arg in str(data_sec[i]):
                args[index] = data_sec[i]["name"].split("\n")[0]
                appear = appear + 1 
        if appear >= 2:
            didntexist.append(arg)
            flag = 1
        if flag == 0:
            success_list.append(arg)
    
    pd.unique(success_list).tolist()

    for i in range (len(user_document)):
        for thing in success_list:
            if str(ctx.message.author.id) in str(user_document[i]):
                if thing in str(user_document[i]):
                    pass
                else:
                    user_document[i]["seiyuus"].append(thing)

    didntexistmeg = ""
    if len(didntexist) > 0:
        for i in range (len(didntexist)):
            didntexistmeg = didntexistmeg + didntexist[i] + "、"
        await ctx.channel.send("{} {}不存在".format(ctx.message.author.mention,didntexistmeg.removesuffix("、")))
    
    with open("user_record.json","w",encoding="utf-8") as file:
        file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
    
    await ctx.channel.send("{} 已登記完成".format(ctx.message.author.mention))

@bot.command()
async def albfollow(ctx, *args):
    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    detial = {
        "user_id" : ctx.message.author.id,
        "seiyuus" : [],
        "albums" : [],
    }

    if str(ctx.message.author.id) not in str(user_document):
        user_document.append(detial)

    args = list(args)

    didntexist = []
    success_list = []
    for index, arg in enumerate(args):
        appear = 0
        flag = 0
        if arg not in str(data):
            didntexist.append(arg)
            flag = 1
        for i in range (len(data)):
            if arg in str(data[i]):
                args[index] = data[i]["title"]
                appear = appear + 1 
        if appear >= 2:
            didntexist.append(arg)
            flag = 1
        if flag == 0:
            success_list.append(arg)
    
    pd.unique(success_list).tolist()

    for i in range (len(user_document)):
        for thing in success_list:
            if str(ctx.message.author.id) in str(user_document[i]):
                if thing in str(user_document[i]):
                    pass
                else:
                    user_document[i]["albums"].append(thing)

    didntexistmeg = ""
    if len(didntexist) > 0:
        for i in range (len(didntexist)):
            didntexistmeg = didntexistmeg + didntexist[i] + "、"
        await ctx.channel.send("{} {}不存在".format(ctx.message.author.mention,didntexistmeg.removesuffix("、")))
    
    with open("user_record.json","w",encoding="utf-8") as file:
        file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
    
    await ctx.channel.send("{} 已登記完成".format(ctx.message.author.mention))
            

        
@bot.command()
async def seifollowdel(ctx, arg):
    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    detial = {
        "user_id" : ctx.message.author.id,
        "seiyuus" : [],
        "albums" : [],
    }

    if str(ctx.message.author.id) not in str(user_document):
        user_document.append(detial)
        await ctx.channel.send("{} 尚未註冊,已建檔".format(ctx.message.author.mention))
        return 0

    if arg not in str(data_sec):
        await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"不存在")
        return 0

    appear = 0
    for i in range (len(data_sec)):
        if arg in str(data_sec[i]):
            arg = data_sec[i]["name"].split("\n")[0]
            appear = appear + 1 
    if appear >= 2:
        await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"不存在")
        return 0


    for i in range (len(user_document)):
        if str(ctx.message.author.id) in str(user_document[i]):
            if arg in str(user_document[i]["seiyuus"]):
                user_document[i]["seiyuus"].remove(arg)
            else:
                await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"不存在")
                return 0

    
    with open("user_record.json","w",encoding="utf-8") as file:
        file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
    
    await ctx.channel.send("{} 已刪除完成".format(ctx.message.author.mention))

@bot.command()
async def albfollowdel(ctx, arg):
    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    detial = {
        "user_id" : ctx.message.author.id,
        "seiyuus" : [],
        "albums" : [],
    }

    if str(ctx.message.author.id) not in str(user_document):
        user_document.append(detial)
        await ctx.channel.send("{} 尚未註冊,已建檔".format(ctx.message.author.mention))
        return 0

    if arg not in str(data):
        await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"不存在")
        return 0

    appear = 0
    for i in range (len(data)):
        if arg in str(data[i]):
            arg = data[i]["title"]
            appear = appear + 1 
    if appear >= 2:
        await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"不存在")
        return 0

    for i in range (len(user_document)):
        if str(ctx.message.author.id) in str(user_document[i]):
            if arg in str(user_document[i]["albums"]):
                user_document[i]["albums"].remove(arg)
            else:
                await ctx.channel.send("{}".format(ctx.message.author.mention),arg+"尚未追蹤")
                return 0

    
    with open("user_record.json","w",encoding="utf-8") as file:
        file.write(json.dumps(user_document,ensure_ascii=False,indent=1))
    
    await ctx.channel.send("{} 已刪除完成".format(ctx.message.author.mention))



bot.run("TOKEN")
