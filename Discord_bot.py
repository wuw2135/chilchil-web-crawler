import discord
from discord.ext import commands
import json

with open("./BlCD/BLCD_data.json","r",encoding="utf-8") as f:
    data = json.load(f)

with open("./Seiyuu/SEIYUU_data.json","r",encoding="utf-8") as file:
    data_sec = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("Bot已經上線!")

#format
def format(list_detail):
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
    if list_detail["title_url"] == "javascript:void(0)":
        embed.add_field(name="受け作品", value=list_detail["uke_count"], inline=False)
    else:
        embed.add_field(name="受け作品", value=list_detail["uke_count"]+"\n"+list_detail["uke_url"], inline=False)
    return embed

#search
@bot.command()
async def norsearch(ctx, *args):

    channel = bot.get_channel(channel)

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
        await ctx.channel.send(embed=format(eval(finallist[0])))
    else:
        for i in range (int(len(finallist)/20)):
            embed=discord.Embed(title="搜尋結果",color=0x881db9)
            embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
            for j in range(20):
                embed.add_field(name=eval(finallist[j])["title"], value=eval(finallist[j])["title_url"], inline=False)
            del finallist[:20]
            await ctx.channel.send(embed=embed)
        
        embed=discord.Embed(title="搜尋結果",color=0x881db9)
        embed.set_author(name="chil-chil", url="https://www.chil-chil.net/", icon_url="https://www.chil-chil.net/img/logo2016.png")
        for i in range (len(finallist)):
            embed.add_field(name=eval(finallist[i])["title"], value=eval(finallist[i])["title_url"], inline=False)
        await ctx.channel.send(embed=embed)


@bot.command()
async def seisearch(ctx, arg):
    channel = bot.get_channel(channel)
    
    for i in range(len(data_sec)):
        if arg in str(data_sec[i]):
            await ctx.channel.send(embed=format_sec(data_sec[i]))
            break



bot.run("TOKEN")
