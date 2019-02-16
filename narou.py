import requests
import time
from bs4 import BeautifulSoup
import bs4
import discord
from discord.ext import commands
import json
from urllib.request import urlopen
import gzip
import urllib.parse
from datetime import datetime
from lxml import html
import chardet
import re
import tempfile


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('ログインしました')

@client.command()
async def command():
    msg = discord.Embed(title= 'ヘルプ', description= '**作品検索**\n!narou 作品名\n\n**R18作品検索**\n!r18 作品名\n\n**外国語検索**\n!babel 単語',colour=0x546e7a)
    await client.say(embed=msg)

@client.command()
async def narou(ctx):
    s_quote = urllib.parse.quote(ctx)
    url = "http://api.syosetu.com/novelapi/api/?out=json&lim=3&word=" + s_quote + "&title=1&wname=1&order=hyoka&of=t-n-w-s&gzip=5"
    response = urlopen(url)
    with gzip.open(response,"rt",encoding="utf-8") as f:
        j_raw = f.read()
        jObj = json.loads(j_raw)
        for a_novel in jObj[1:]:
            title = a_novel['title']
            writer = a_novel['writer']
            story = a_novel['story']
            ncode = a_novel['ncode']
            link = "http://ncode.syosetu.com/{}/".format(ncode.lower())
            msg = discord.Embed(title= title, description= '\n\n' + link + '\n\n' '作：' + writer + '\n\n' + story + '\n',colour=0x546e7a)
            await client.say(embed=msg)



@client.command()
async def r18(ctx):
    s_quote = urllib.parse.quote(ctx)
    url = "http://api.syosetu.com/novel18api/api/?out=json&lim=3&word=" + s_quote + "&title=1&order=hyoka&of=t-n-w-s&gzip=5"
    response = urlopen(url)
    with gzip.open(response,"rt",encoding="utf-8") as f:
        j_raw = f.read()
        jObj = json.loads(j_raw)
        for a_novel in jObj[1:]:
            title = a_novel['title']
            writer = a_novel['writer']
            story = a_novel['story']
            ncode = a_novel['ncode']
            link = "http://ncode.syosetu.com/{}/".format(ncode.lower())
            msg = discord.Embed(title= title, description= '\n\n' + link + '\n\n' '作：' + writer + '\n\n' + story + '\n',colour=0x546e7a)
            await client.say(embed=msg)

@client.command()
async def babel(ctx):
    s_quote = urllib.parse.quote(ctx, encoding= 'euc-jp')
    url = "http://www.tekiro.main.jp/?search=" + s_quote
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', class_= 'entry_title')
    content = soup.find('div', class_= 'jgm_entry_desc_mark')
    try:
        msg = discord.Embed(title= 'BABEL～世界の言葉～', description= title.getText() + '\n' + ' ' + content.getText().replace('Tweet', '') + '\n他の検索結果も見る\n' + url, colour=0x546e7a)
        await client.say(embed=msg)
    except AttributeError:
        msg = discord.Embed(title= 'BABEL～世界の言葉～', description='検索結果が存在しません！',colour=0x546e7a)
        await client.say(embed=msg)

@client.event
async def on_message(message):
    if client.user != message.author:
        msg = message.content.split(' ')
        if msg[0] == '!read':
            print(msg)
            print(len(msg))
            if len(msg) == 2:
                await client.send_message(message.channel, message.author.mention + ' こいつコマンド間違ってるんだがｗｗｗｗｗｗｗアホ過ぎｗｗｗｗｗｗｗ')
            elif len(msg) >= 3:
                s_quote = urllib.parse.quote(msg[1])
                url = "http://api.syosetu.com/novelapi/api/?out=json&lim=1&word=" + s_quote + "&title=1&wname=1&order=hyoka&of=t-n-w-s&gzip=5"
                print(url)
                response = urlopen(url)
                with gzip.open(response,"rt",encoding="utf-8") as f:
                    j_raw = f.read()
                    jObj = json.loads(j_raw)
                    for a_novel in jObj[1:]:
                        title = a_novel['title']
                        ncode = a_novel['ncode']
                        link = "http://ncode.syosetu.com/{}/".format(ncode.lower())
                target_url = link + msg[-1] + '/'
                print(target_url)
                request = requests.get(target_url)
                search_data = BeautifulSoup(request.content, 'lxml')
                print(search_data)
                for rt in search_data.find_all('rt', src = False):
                    rt.decompose()
                for rp in search_data.find_all('rp', src = False):
                    rp.decompose()
                text_data = search_data.find("div",id="novel_honbun")
                print(text_data)
                time.sleep(1)
                string = text_data.getText()
                file_name = title + '.txt'
                with tempfile.TemporaryDirectory() as tmp:
                    with open(tmp + '/' + file_name, 'w+') as file:
                        file.write(string)
                    await client.send_file(message.channel, tmp + '/' + file_name, content = title + msg[-1] + '話')

client.run("NDYxNTQ4NzY5MjE4MDAyOTY0.DtR64w.TjIAJjGADcmJZWnP4qBfX1ea_FE")