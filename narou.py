import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import gzip
from lxml import html
import urllib
from urllib.request import urlopen
import urllib.parse
import gzip
import json
import os

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('ログインしました')

client.remove_command('help')
@client.command()
async def help():
    embed = discord.Embed(title='なろうbot', description='※現在開発中')
    embed.add_field(name='コマンド一覧', value='**!kisaragi 作品名**\n\n' + '作品のアクセス解析を表示します。単語のみの場合、その単語のランキング1位が表示されます。', inline= False)
    await client.say(embed=embed)

@client.command()
async def kisaragi(ctx):
    #ncodeに変換
    url = "http://api.syosetu.com/novelapi/api/?out=json&lim=3&word=" + str(ctx) + "&title=1&wname=1&order=hyoka&of=t-n-w-s"
    response = requests.get(url)
    print(response)
    mylist = []
    j_date = response.json()
    for novel in j_date[1:]:
        n = novel['ncode']
        mylist.append(n)
    #kisaragiでスクレイピング
    kisaragi = "https://kasasagi.hinaproject.com/access/top/ncode/" + mylist[0] + "/"
    k_date = requests.get(str(kisaragi))
    print(k_date)
    soup = BeautifulSoup(k_date.content, "html.parser")
    t_date = soup.select("#title")
    td = soup.select("td.right")
    for text in t_date:
        title = text.text
    td_list = []
    for a_txt in td:
        a = a_txt.text
        td_list.append(a.replace('アクセス', ''))
    #整形
    d = ['小計', td_list[0], 'パソコン', td_list[1], '携帯', td_list[2], 'スマホ', td_list[3]]
    y = ['小計', td_list[4], 'パソコン', td_list[5], '携帯', td_list[6], 'スマホ', td_list[7]]
    t = ['累計', td_list[8], td_list[9], 'パソコン', td_list[10], td_list[11], '携帯', td_list[12], td_list[13], 'スマホ', td_list[14], td_list[15]]

    msg = discord.Embed(title= title, description='**◆本日のデータ**\n' + \
              '小説全体' + '　　　' + 'PV\n\n' + \
              d[0] + '　　　　' + d[1] + '\n' + \
              d[2] + '　　' + d[3] + '\n' + \
              d[4] + '　　　　' + d[5] + '\n' + \
              d[6] + '　　　' + d[7] + '\n', colour=0x546e7a
              )
    field_1 = '**◆昨日のデータ**\n' + \
              '小説全体' + '　　　' + 'PV\n\n' + \
              y[0] + '　　　　' + y[1] + '\n' + \
              y[2] + '　　' + y[3] + '\n' + \
              y[4] + '　　　　' + y[5] + '\n' + \
              y[6] + '　　　' + y[7] + '\n'

    field_2 = '**◆総合・ユニーク**\n' + \
              '小説全体' + '　　　　PV' + '　　　　　　　　　ユニーク\n\n' + \
              t[0] + '　　　　' + t[1] + '　　　　　' + t[2] + '\n' + \
              t[3] + '　　' + t[4] + '　　　　　　' + t[5] +'\n' + \
              t[6] + '　　　　' + t[7] + '　　　　　　' + t[8] +'\n' + \
              t[9] + '　　　' + t[10] + '　　　　　　' + t[11] + '\n\n\n' + \
              'リンク\n' + kisaragi

    msg.add_field(name= '-----------------------------------------------', value= field_1, inline= False)
    msg.add_field(name= '-----------------------------------------------', value= field_2, inline= False)
    await client.say(embed=msg)



NAROU_TOKEN = os.environ.get('NAROU_TOKEN')
client.run(NAROU_TOKEN)














client.run("NDYxNTQ4NzY5MjE4MDAyOTY0.DtR64w.TjIAJjGADcmJZWnP4qBfX1ea_FE")