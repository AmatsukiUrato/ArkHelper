# -*- coding: utf-8 -*-

from ctypes.util import find_library
from dateutil.parser import parse
import datetime
import discord
import sqlite3
import asyncio
import time
import re

# version
__version__ = '2.0.0'



# Discord.pyの読み込み
client = discord.Client()

# 鍵の読み込み
KEY = None
with open('KEY.txt', 'r') as f:
    KEY = f.read()

# データベースの読み込み
dbname = 'ark.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()

# Botが接続出来たとき
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if not discord.opus.is_loaded():
        discord.opus.load_opus(find_library("opus"))

    # テーブルの存在確認
    # テーブル名の定義
    tablename = "arktimer"
    c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % tablename)
    if not c.fetchone():
        # id, 名前，現在のタイム，アラート終了予定タイム，入力した人
        c.execute("CREATE TABLE %s(id INTEGER PRIMARY KEY, title TEXT, at_registration_time TEXT, finish_time TEXT, register_name TEXT)" % tablename)
        conn.commit()


    # テーブル内のタイマー切れ確認
    for row in c.execute("SELECT * FROM arktimer"):
        if (datetime.datetime.strptime(row[3],'%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now()).total_seconds() <= 0:
            # 配列の削除
            c.execute("DELETE FROM arktimer WHERE id=?",(row[0],))
            conn.commit()



# メッセージを受け取った時(チャット文が飛んできた時)
@client.event
async def on_message(message):



    ####################
    # ArkTimerの使い方説明
    ####################
    if message.content.startswith('!ark help'):
        text = '```js\n[1]!ark help - この説明文を表示する．\n\n[2]!ark link - Arkをやる上で知ってたら便利なリンク集．\n\n[3]!ark timer - ケア用のタイマー．\n"!ark timer"の後に"0~99:0~59"or"1~9999...d/h/m/"を入力することで時間を測れる．タイマーの後にタイトルも入力できる．\n\n[4]!ark timerlist - 現在のケア用タイマー一覧．\n"!ark timer"で登録したタイマーの一覧が見れる．\n\n[5]!ark timerdel - タイマー一覧にあるタイマーを削除する．\n"!ark timerdel id/all"で登録したタイマーを削除する．allにした場合全て消えるので注意．\n\n[7]!ark -v|!ark version - botのバージョンを表示する．```'
        # \n\n[5](未)!ark summon - ArkHelperをボイスチャンネルに呼ぶ．\nタイマーでYoutubeの動画音声を流したい場合は呼ぶ必要あり．\n\n[6](未)!ark disconnect - ArkHelperをボイスチャンネルから退ける．\n"!ark summon"で呼んだ後，戻すときに使う．\n\n[7](未)!ark setalert - timer用のYoutube動画をセットする．\n"!ark setalert youtubeのリンク"で登録を行う．
        await client.send_message(message.channel, text)



    #########################
    # Arkに関係する便利なリンク集
    #########################
    elif message.content.startswith('!ark link'):
        text = '__[1]Ark Officital wiki__ - <https://ark.gamepedia.com/ARK_Survival_Evolved_Wiki>\n\n__[2]Ark Japan wiki__ - <http://wikiwiki.jp/arkse/>\n\n__[3]DODOREX__ - <http://www.dododex.com/>\n\n__[4]ARK Community Forums__ - <https://survivetheark.com/>\n\n__[5]Ark wiki/Resource_Map__ - <https://ark.gamepedia.com/Resource_Map>\n\n__[6]Ark PatchNote__ - <https://steamcommunity.com/app/346110/discussions/0/594820656447032287/?l=japanese>'
        await client.send_message(message.channel, text)



    #########################
    # Arkのカウントダウンタイマー
    #########################
    elif message.content.startswith('!ark timer '):
        messagelist = message.content.split(" ")

        if len(messagelist) > 4:
            # 5項目以上ある時
            pass
        else:
            count_time = messagelist[2]

            # 以下の正規表現かどうかをチェック
            matchOB_hour_minutes = re.match(r"([0-9]|[0-9][0-9]):([0-9]|[0-5][0-9])", count_time)
            matchOB_hour = re.match(r"([1-9]|[1-9][0-9]*|)h", count_time)
            matchOB_minutes = re.match(r"([1-9]|[1-9][0-9]*)m", count_time)
            matchOB_days = re.match(r"([1-9]|[1-9][0-9]*)d", count_time)

            # タイマーのコマンドだと確認できた場合
            if matchOB_hour_minutes or matchOB_hour or matchOB_minutes or matchOB_days:

                finish_time = 0

                # XX:XX表記
                if matchOB_hour_minutes:
                    finish_time_list = count_time.split(":")
                    finish_time = ( int(finish_time_list[0]) * 60 + int(finish_time_list[1]) ) * 60

                # XXd表記
                if matchOB_days:
                    finish_time = int(count_time[:-1]) * 60 * 60 * 24

                # XXh表記
                if matchOB_hour:
                    finish_time = int(count_time[:-1]) * 60 * 60

                # XXm表記
                if matchOB_minutes:
                    finish_time = int(count_time[:-1]) * 60


                # Titleが空白だった場合の処理
                if len(messagelist) < 4:
                    messagelist.append("無名")

                # 現在の時刻を取得
                nowtime_datetime = datetime.datetime.now()
                # 終わる時刻を定義
                finishtime_datetime = (nowtime_datetime + datetime.timedelta(seconds=int(finish_time)))

                # 送るメッセージの作成
                text = '`' + finishtime_datetime.strftime("%m/%d %H:%M:%S") + '` に `'+ messagelist[3] +'` のアラートを行います'

                await client.send_message(message.channel,text)


                # timerlistに登録する
                # 名前，現在のタイム，アラート終了予定タイム，入力した人
                # Insert実行
                ark_timerdata = ([messagelist[3], nowtime_datetime, finishtime_datetime, message.author.name])
                c.execute("INSERT INTO arktimer (title, at_registration_time, finish_time, register_name) VALUES (?,?,?,?)", ark_timerdata)
                conn.commit()

                # InsertしたタイマーIDの取得
                timer_id = -1
                for row in c.execute("SELECT last_insert_rowid();"):
                    timer_id = row[0]

                # 指定した時間止める
                await asyncio.sleep(finish_time)

                # タイマーリストに存在するかどうかの判定
                c.execute("SELECT * FROM arktimer WHERE id = ?", (timer_id,))
                if c.fetchone():

                    # 通知の表示
                    await client.send_message(message.channel, '@here `'+messagelist[3]+'` の時間です by '+message.author.mention+'')


                # 配列の削除
                c.execute("DELETE FROM arktimer WHERE id = ?", (timer_id,))
                conn.commit()



    ################################
    # 現在登録されているタイマー一覧を表示
    ################################
    elif message.content.startswith('!ark timerlist'):
        text = '```css\n'

        # 表示するタイマーがある時
        for row in c.execute("SELECT * from arktimer"):

            remaining_time = str(datetime.datetime.strptime(row[3],'%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now()).split(".")[0]

            text += '['+str(row[0])+']'+row[1]+ ' by '+ row[4] + '\n　 [残り : ' + remaining_time + ']\n\n'
        else :
            text += '```'

        # 表示するタイマーがない時
        if text == '```css\n```':
            text = '```何も登録されていません```'

        await client.send_message(message.channel, text)



    ##############################
    # 登録されているタイマーの削除を行う
    ##############################
    elif message.content.startswith('!ark timerdel '):
        messagelist = message.content.split(" ")

        # 全削除
        if messagelist[2] == "all":
            c.execute("DELETE FROM arktimer")
            conn.commit()
            text = "現在登録されているタイマーを全て削除しました"
            await client.send_message(message.channel, text)

        # 個別削除
        else:
            for row in c.execute("SELECT * from arktimer"):
                if (int(messagelist[2]) == row[0]):
                    # 配列の削除
                    c.execute("DELETE FROM arktimer WHERE id=?",(row[0],))
                    conn.commit()
                    await client.send_message(message.channel, '`[' + messagelist[2] + ']' + row[1] + '` を削除しました')
                    break
            else:
                await client.send_message(message.channel, '`[' + messagelist[2] + ']' + row[1] + '` は見つかりませんでした')



    #########################
    # お知らせの追加
    #########################
    elif message.content.startswith('!ark notice'):
        # messagelist = message.content.split(" ")
        # if len(messagelist) > 2:
        #     with open('notice.txt', 'w') as n:
        #         n.write(message.content.replace('!ark notice ',''))



    ################################
    # ArkHelperBotのバージョンを表示する
    ################################
    elif message.content.startswith('!ark -v') or message.content.startswith('!ark version'):
        await client.send_message(message.channel, 'Botのバージョンは'+ __version__ +'です．')



@client.event
async def on_member_join(member):
    print('join channnel!')
    # with open('notice.txt', 'r') as n:
    #     client.send_message(member.private_channels, n.read())



@client.event
async def on_server_join(server):
    print('on_server_join')
    # with open('notice.txt', 'r') as n:
        # client.send_message(member.private_channels, n.read())

@client.event
async def on_voice_state_update(before, after):
    print(before.server.name)
    print('on_voice_state_update')

# Run
client.run(KEY)
