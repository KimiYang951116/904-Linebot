from pyexpat.errors import messages


from view.guess import PrepareGuess, playguess, setdiff, startguess

from flask import Flask, request, abort
app = Flask(__name__)
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage
import pymysql
import time
from imgurpython import ImgurClient
from datetime import datetime,timezone,timedelta
import time
local = time.localtime()
import random as rd
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from view.ab import *
from view.general import *
from view.wordle import *
from view.imgur import *
client_id ='6cca211229bdb72'
client_secret = '71a4af51db0c990c99fb3950c8f6760967df12c1'
access_token = "711b91f3df509af23502dad9bc3386687c513c93"
refresh_token = "755d5b499edf523d0a9e1f57ea9a6629702280d8"
line_bot_api = LineBotApi('ISGfM1RF3Q+ebtmKd3854wbUBkT05lca8268dGtSPofEYgs7vkZ5grGIWJEBr94fBS/gJMG9NkocJShmM7WlfZdX54OeD0l6WH/unQs7QUKnz+wkW8ZGeFQYHOprfCVMMqzoJlEHB96lXcpZHDNjGAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('66c4150f2f7451768da6b608807ba3d5')
admin_id='U66a509cdb84357c931224f9bfc87fbab'
ABinstuctions = '''1A2B規則如下:
1.電腦將會隨機產生一個不重複的四位數字
2.請輸入一個四位數字進行猜測
3.電腦將會告訴你那個數字是幾A幾B
(1)A表示一個位數正確並在對的位置
(2)B表示一個位數正卻但位置不對
4.目標:想辦法在最短次數內猜對數字
5.如需退出遊戲請輸入/leave1A2B
例:
電腦數字:1935
玩家猜測數字:2950 => 1A1B(9為A, 5為B)
請輸入一個四位數字來開始遊戲'''
ABstartmess = '''1A2B
輸入四位數字開始遊戲
如需規則請輸入/In'''
Guessinstuctions = '''猜數字模式說明如下:
1.簡單:數字介於0-20之間
2.普通:數字介於0-100之間
3.困難:數字介於0-1000之間
4.爆難:數字介於0-100000之間'''
Wordlestartmess = '''WORDLE
透過給予提示猜測含有五個字母之英文字
你有最多六字機會
更多規則請輸入/In
'''
WordleInstructions = '''WORDLE 規則
WORDLE很像1A2B只是它要猜的是英文單字，而不是一個四位數字
經典版WORDLE會以顏色提示你猜字的接近度
這裡我們已A, B, C 三個符號進行提示
A這個位置的英文字母是對的，它也應該出現在這裡
B英文字母是對的，但是它應該要放在其他位置
C這個英文字母不存在於英文單字中
例如: 如果答案是APPLE 你猜HAPPY
robot會回復你 : CBABC
每天每個人的答案皆相同，每天每個人有六次機會猜出答案
'''

englishwords = pd.read_json("words_dictionary.json",typ="series")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'ok'



def ChangeUserStatus(conn, uid, thing):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set behavior='{thing}' where name='{uid}'"
        cursor.execute(sql)
    conn.commit()

            


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    etext = event.message.text
    connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b8854a04772e3b",
        password="0891a25d",
        db="heroku_02e5c32fa545b1e",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id)
    AddUserInfo(connection, user_id, user_name.display_name)
    if etext == '/start1A2B':
        Start1a2b(connection, user_id)
        message=TextSendMessage(
            text = ABstartmess,
            quick_reply = QuickReply(
            items=[
                    QuickReplyButton(
                        action=MessageAction(label='退出遊戲', text='/leave')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='查看規則', text='/In')
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/1A2Bbest':
        best  = GetBestScore(connection)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=best))
    elif etext == '/leave':
        SetDefault(connection, user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你已退出此功能'))
    elif etext == '/games':
        message=TextSendMessage(
            text = '請選擇遊戲',
            quick_reply = QuickReply(
            items=[
                    QuickReplyButton(
                        action=MessageAction(label='1A2B', text='/start1A2B')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='猜數字', text='/startguess')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='wordle', text='/startwordle')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='1A2B排行榜', text='/1A2Bbest')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='製作1A2B獎狀', text='/1A2Bgood')
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/startguess':
        PrepareGuess(connection, user_id)
        message=TextSendMessage(
            text = '請選擇難易度',
            quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label='簡單', text='/guesseasy')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='普通', text='/guessmiddle')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='困難', text='/guesshard')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='爆難', text='/guessextreme')
                    ),
                    QuickReplyButton(
                        action=MessageAction(label='選項說明', text='/In')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/guesseasy':
        setdiff(connection, user_id, 1)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你選擇了簡單模式，數字將會介於1-20之間\n請開始猜測'))
    elif etext == '/guessmiddle':
        setdiff(connection, user_id, 2)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你選擇了普通模式，數字將會介於1-100之間\n請開始猜測'))
    elif etext == '/guesshard':
        setdiff(connection, user_id, 3)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你選擇了困難模式，數字將會介於1-1000之間\n請開始猜測'))
    elif etext == '/guessextreme':
        setdiff(connection, user_id, 4)  
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你選擇了爆難模式，數字將會介於1-100000之間\n請開始猜測'))
    elif etext == '/In':
        beha = CheckUser(connection, user_id, 'behavior')
        if beha == '1A2B':
            message=TextSendMessage(
                text = ABinstuctions,
                quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label='退出遊戲', text='/leave')
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif beha == 'guessnump':
            message=TextSendMessage(
                text = Guessinstuctions,
                quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label='簡單', text='/guesseasy')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='普通', text='/guessmiddle')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='困難', text='/guesshard')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='爆難', text='/guessextreme')
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif beha == 'wordle':
            message=TextSendMessage(
                text = WordleInstructions,
                quick_reply = QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label='退出遊戲', text='/leave')
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/comment':
        ChangeUserStatus(connection, user_id, 'comment')
        message=TextSendMessage(
            text = '如有任何問題，或系統有任何錯誤，歡迎寫下意見',
            quick_reply = QuickReply(
            items=[
                    QuickReplyButton(
                        action=MessageAction(label='取消留言', text='/leave')
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)  
    elif etext == '無功能':
        login = CheckUser(connection, user_id, 'login')
        if login == 'admin':
            message=TextSendMessage(
                text = f'歡迎登入，你的登入身分為{login}',
                quick_reply = QuickReply(
                items=[
                        QuickReplyButton(
                            action=MessageAction(label='重設所有人1A2B紀錄', text='/Default1A2BRecord')
                            ),
                        QuickReplyButton(
                            action=MessageAction(label='傳送群發訊息給所有人', text='/PushMessageEveryone')
                            ),
                        QuickReplyButton(
                            action=MessageAction(label='傳送群發訊息給904成員', text='/PushMessage904')
                            ),
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, message)
        elif login == 'developer':
            message=TextSendMessage(
                text = f'歡迎登入，你的登入身分為{login}',
                quick_reply = QuickReply(
                items=[
                        QuickReplyButton(
                            action=MessageAction(label='傳送群發訊息給904成員', text='/leave')
                            ),
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/PushMessageEveryone':
        loin = CheckUser(connection, user_id, 'login')
        if loin == 'admin':
            ChangeUserStatus(connection, user_id, 'pusheveryone')
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='輸入要發送的文字'))
    elif etext == '/GraduateClock':        
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        dt2 = datetime(2022,6,8,0,0,0).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        hr = (dt2-dt1).seconds // 3600
        m = (dt2-dt1).seconds % 3600 // 60
        s = (dt2-dt1).seconds % 60
        day = (dt1-dt2).days
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f'已經畢業 {day} 天 {hr} 小時 {m} 分 {s} 秒'
            )
        )
    elif etext == '/startwordle':
        StartWordle(connection, user_id)
        message=TextSendMessage(
            text = Wordlestartmess,
            quick_reply = QuickReply(
            items=[
                    QuickReplyButton(
                        action=MessageAction(label='退出遊戲', text='/leave')
                        ),
                    QuickReplyButton(
                        action=MessageAction(label='查看規則', text='/In')
                        ),
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    elif etext == '/1A2Bgood':
        good = Image.open('Certificate.png')
        times =str(CheckUser(connection, user_id, '1A2Bbest'))
        if times != -1:
            name = user_name.display_name
            drawobj = ImageDraw.Draw(good)
            fontinfo = ImageFont.truetype('kaiu.ttf', 100)
            fontinfo2 = ImageFont.truetype('kaiu.ttf', 50)
            drawobj.text((910,880),times,fill = 'Black', font = fontinfo)
            drawobj.text((870,600),name,fill = 'Black', font = fontinfo)
            drawobj.text((800,1100),f'西元{local.tm_year}年{local.tm_mon}月{local.tm_mday}日',fill = 'Black', font = fontinfo2)
            good.save('FCertificate.png')
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            image = upload(client, 'FCertificate.png')
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=str(image['link']), preview_image_url=str(image['link'])))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('你目前沒有任何1A2B遊玩紀錄，故無法製作獎狀'))
    else:
        beha = CheckUser(connection, user_id, 'behavior')
        if beha == '1A2B':
            try:
                vtext = str(int(etext))
            except:
                message=TextSendMessage(
                    text = '請輸入四位數字',
                    quick_reply = QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label='退出遊戲', text='/leave')
                            ),
                            QuickReplyButton(
                                action=MessageAction(label='查看規則', text='/In')
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, message)
            if len(etext) != 4 and etext.startswith != 0:
                    message=TextSendMessage(
                        text = '請輸入四位數字',
                        quick_reply = QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=MessageAction(label='退出遊戲', text='/leave')
                                    ),
                                QuickReplyButton(
                                    action=MessageAction(label='查看規則', text='/In')
                                    ),
                                ]
                            )
                        )
                    line_bot_api.reply_message(event.reply_token, message)
            else:
                AB, guess_times = Play1A2B(connection, user_id, etext)
                if AB == '4A0B':
                    best = CheckUser(connection, user_id, '1A2Bbest')
                    if best == -1:
                        Set1A2BBest(connection, user_id, guess_times)
                        mess = [
                            TextSendMessage(text=f'你成功在第{guess_times}次猜對了'),
                            TextSendMessage(text=f'你目前無任何紀錄，已將你本次紀錄謝入最佳紀錄')
                            ]
                        line_bot_api.reply_message(event.reply_token, mess)
                    else:
                        if best > guess_times:
                            Set1A2BBest(connection, user_id, guess_times)
                            mess = [
                            TextSendMessage(text=f'你成功在第{guess_times}次猜對了'),
                            TextSendMessage(text=f'你破紀錄了，恭喜恭喜')
                            ]
                            line_bot_api.reply_message(event.reply_token, mess)
                        else:
                            mess = [
                            TextSendMessage(text=f'你成功在第{guess_times}次猜對了'),
                            TextSendMessage(text=f'你並未突破你的最佳紀錄{best}次\n繼續加油')
                            ]
                            line_bot_api.reply_message(event.reply_token, mess)
                    SetDefault(connection, user_id)
                else:
                    message=TextSendMessage(
                        text = AB,
                        quick_reply = QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label='退出遊戲', text='/leave')
                            ),
                            QuickReplyButton(
                                action=MessageAction(label='查看規則', text='/In')
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, message)   
        elif beha == 'guessnum':
            try:
                vtext = str(int(etext))
            except:
                message=TextSendMessage(
                    text = '請輸入數字',
                    quick_reply = QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label='退出遊戲', text='/leave')
                            ),
                            QuickReplyButton(
                                action=MessageAction(label='查看規則', text='/In')
                            ),
                        ]
                    )
                ) 
                line_bot_api.reply_message(event.reply_token, message)  
            resu, guess_times = playguess(connection, user_id, etext)
            if resu == 'same':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(f'恭喜你，你在第{guess_times}次猜測中答對了'))
                SetDefault(connection, user_id)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(resu))
        elif beha == 'wordle':
            if len(etext) != 5:
                line_bot_api.reply_message(event.reply_token, TextSendMessage('請輸入含有五個字母之英文單字'))
            else:
                isword = checkifwordvaild(etext)
                if isword == False:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage('請輸入存在的英文單字'))
                else:
                    ABC, times = Playwordle(connection, user_id, etext)
                    if times > 6:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage('你已超過了六次的猜測次數'))
                    else:
                        lstABC = list(ABC)
                        correct = False
                        for i in range(len(lstABC)):
                            if lstABC[i] != 'A':
                                break
                            else:
                                if i == 4:
                                    correct = True
                        if correct != True:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(ABC))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(f'你在第{times}次答對了，恭喜你'))
                            SetDefault(connection,user_id)

        elif beha == 'comment':
            line_bot_api.push_message(admin_id, TextSendMessage(text=f'''{etext}
傳送人:{user_name.display_name}
日期:{local.tm_mon}月{local.tm_mday}日{local.tm_hour+8}時'''))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'''感謝你的回饋
你的訊息已透過以下格式送出
{etext}
傳送人:{user_name.display_name}
日期:{local.tm_mon}月{local.tm_mday}日{local.tm_hour+8}時'''))
            SetDefault(connection, user_id)
        elif beha == 'pusheveryone':
            lst1 = GetAllUser(connection, 'name')
            for i in range(len(lst1)):
                line_bot_api.push_message(lst1[i], TextSendMessage(text=etext))
            SetDefault(connection, user_id)
if __name__ == '__main__':
    app.run()