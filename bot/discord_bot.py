import discord
from discord.ext import commands
import json
from datetime import datetime
import pandas as pd
from discord.utils import get
import os



with open("D:/notifiction_bot/BlCD/BLCD_data.json","r",encoding="utf-8") as file:
    data = json.load(file)

with open("D:/notifiction_bot/Seiyuu/SEIYUU_data.json","r",encoding="utf-8") as file:
    data_sec = json.load(file)

with open("D:/notifiction_bot/BlCD/update_data.json","r",encoding="utf-8") as file:
    data_update = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


#---------------------------join server---------------------------------
@bot.event
async def on_guild_join(guild):
    await guild.text_channels[0].send('已加入 {}!\n請先設定更新訊息發送頻道!\n若未設定將不發送任何更新訊息!'.format(guild.name))

#---------------------------send update message---------------------------------
@bot.event
async def on_ready():
    print("Bot已經上線!")

    with open("server_list.json","r",encoding="utf-8") as file:
        serverdata = json.load(file)

    for i in range (len(serverdata)):
        try:
            channelid = serverdata[i]["channel_id"]
            channel = bot.get_channel(channelid)

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
        except:
            pass


    with open("user_record.json","r",encoding="utf-8") as file:
        user_document = json.load(file)
    
    
    for i in range (len(user_document)):
        try:
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
        except:
            pass

#---------------------------format setting---------------------------------
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

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx,extension):
    bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx,extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"Un-Loaded {extension} done.")

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx,extension):
    bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"Re-Loaded {extension} done.")

for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")


if __name__ == "__main__":
    bot.run("ODE4MTYyODgyMjY0ODI1ODk2.YEUDjw.DB1O4niQtE0YPx3IS4b08xvHNg0")