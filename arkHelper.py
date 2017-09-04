from ctypes.util import find_library
import discord
import asyncio
import time
import re

client = discord.Client()

# 鍵の読み込み
with open('KEY.txt', 'r') as f:
    KEY = f.read()

bot_voice = None
bot_server = None
alertlink = None

hour_minutes_pattern = r"([0-9]|[0-9][0-9]):([0-9]|[0-5][0-9])"
hour_pattern = r"([1-9]|[1-9][0-9])h"
minutes_pattern = r"([1-9]|[1-9][0-9]|[1-9][0-9][0-9])m"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if not discord.opus.is_loaded():
        discord.opus.load_opus(find_library("opus"))

@client.event
async def on_message(message):
    # ArkTimerの使い方説明
    if message.content.startswith('!ark help'):
        text = '```js\n[1]!ark help - この説明文を表示する．\n\n[2]!ark link - Arkをやる上で知ってたら便利なリンク集．\n\n[3]!ark timer - ケア用のタイマー．\n"!ark timer"の後に"0~99:0~59"or"1~99h"or"1~999m"を入力することで時間を測れる．\n\n[4](未)!ark timerlist - 現在のケア用タイマー一覧．\n"!ark timer"で登録したタイマーの一覧が見れる．\n\n[5]!ark summon - ArkHelperをボイスチャンネルに呼ぶ．\nタイマーでYoutubeの動画音声を流したい場合は呼ぶ必要あり．\n\n[6]!ark disconnect - ArkHelperをボイスチャンネルから退ける．\n"!ark summon"で呼んだ後，戻すときに使う．\n\n[7]!ark setalert - timer用のYoutube動画をセットする．\n"!ark setalert youtubeのリンク"で登録を行う．```'
        await client.send_message(message.channel, text)

    # Arkに関係する便利なリンク集
    elif message.content.startswith('!ark link'):
        text = '__[1]Ark Officital wiki__ - <https://ark.gamepedia.com/ARK_Survival_Evolved_Wiki>\n\n__[2]Ark Japan wiki__ - <http://wikiwiki.jp/arkse/>\n\n__[3]DODOREX__ - <http://www.dododex.com/>\n\n__[4]ARK Community Forums__ - <https://survivetheark.com/>\n\n__[5]Ark wiki/Resource_Map__ - <https://ark.gamepedia.com/Resource_Map>'

        await client.send_message(message.channel, text)

    # Arkのカウントダウンタイマー
    elif message.content.startswith('!ark timer '):
        messagelist = message.content.split(" ")
        count_time = messagelist[2]
        matchOB_hour_minutes = re.match(hour_minutes_pattern, count_time)
        matchOB_hour = re.match(hour_pattern, count_time)
        matchOB_minutes = re.match(minutes_pattern, count_time)

        if matchOB_hour_minutes or matchOB_hour or matchOB_minutes:
            finish_time = 0
            if matchOB_hour:
                finish_time = int(count_time[:-1]) * 3600

            if matchOB_minutes:
                finish_time = int(count_time[:-1]) * 60

            if matchOB_hour_minutes:
                finish_time_list = count_time.split(":")
                finish_time = ( int(finish_time_list[0]) * 60 + int(finish_time_list[1]) ) * 60

            # 空白だった場合の処理
            print(len(messagelist))
            print(messagelist)
            if len(messagelist) < 4:
                messagelist.append("無名")

            print(finish_time)
            await client.send_message(message.channel, str(int(finish_time / 60))+'分後に '+ messagelist[3] +' のアラートを行います')

            # with open('timeData.txt', 'a') as f:
            #     f.write(str(finish_time))

            await asyncio.sleep(finish_time)
            await client.send_message(message.channel, '@here '+messagelist[3]+'の時間です')
            if client.is_voice_connected(bot_server):
                player = await bot_voice.create_ytdl_player(alertlink)
                player.volume = 0.1
                player.start()
                time.sleep(60)
                player.stop()

    elif message.content.startswith('!ark summon'):
        global bot_voice
        global bot_server
        bot_voice = await client.join_voice_channel(message.author.voice.voice_channel)
        bot_server = bot_voice.server

    elif message.content.startswith('!ark setalert '):
            global alertlink
            alertlink = message.content[14:]
            await client.send_message(message.channel, 'アラートを<'+alertlink+'>に設定しました\nアラートは`!ark summon`をしていない場合機能しません．')

    elif message.content.startswith('!ark disconnect'):
        await bot_voice.disconnect()

client.run(KEY)
