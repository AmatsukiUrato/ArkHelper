# ArkTImer.py

## Infomation
DiscordのArk用Bot．
python3.6で実装．
Arkに役立つリンクやケア用のタイマー管理を行える．

## How2Use
1. `git clone https://github.com/AmatsukiUrato/ArkHelper.git`でArkTimerをDownLoadする．
2. `KEY.txt`を`arktymer.py`と同じ階層に作成し，DiscordのTokenを入力する．
3. `arktimer.py`を起動する．

## Command
`!ark help`で確認して下さい．

## Future
- Timerの音声アラームを実装
- ~~現在測定しているタイマーの一覧表を実装~~
    - サーバ情報を取っていないので，今後複数サーバに対応できるようにサーバデータも取る．<br>余裕があればDBを使用したい．
- ~~登録したタイマーの削除~~
- 恐竜のテイム用カリュキュレータの実装
- ブリーディングの時間リスト実装

## If
- 指定したサーバのログイン状況の表示(BattleMatrixから取得orSteamAPI．詳しく調べてない)

## Used
- [Discord.py](https://github.com/Rapptz/discord.py)
