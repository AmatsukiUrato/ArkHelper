# ArkTImer.py

## Infomation
### English
DiscordBot for Ark:SurvivalEvolved
Used python3.6/sqlite3
This bot can management dino's caretime and etc..

### Japanese
DiscordのArk用Bot．
python3.6/sqlite3で実装．
Arkに役立つリンクやケア用のタイマー管理を行える．

## How2Use
### English
1. type `git clone https://github.com/AmatsukiUrato/ArkHelper.git` on console.
2. make `KEY.txt` at same `arktymer.py` directory, and insert your bot token in `KEY.txt`.
3. start arkHelperBot by `python|python3 arktimer.py`.

### Japanese
1. `git clone https://github.com/AmatsukiUrato/ArkHelper.git`でArkTimerをDownLoadする．
2. `KEY.txt`を`arktymer.py`と同じ階層に作成し，DiscordのTokenを入力する．
3. `python|python3 arktimer.py`でarkHelperBotを起動する．

## Command
### English
use `!ark help` on Discord.

### Japanese
`!ark help`で確認して下さい．

## Future
- Timerの音声アラームを実装
- ~~現在測定しているタイマーの一覧表を実装~~
    - ~~サーバ情報を取っていないので，今後複数サーバに対応できるようにサーバデータも取る．<br>余裕があればDBを使用したい．~~
    - サーバ別にデータベースを作成する
- ~~登録したタイマーの削除~~
- 恐竜のテイム用カリュキュレータの実装
- ブリーディングの時間リスト実装

## If
- 指定したサーバのログイン状況の表示(BattleMatrixから取得orSteamAPI．詳しく調べてない)

## Used
- [Discord.py](https://github.com/Rapptz/discord.py)
