from ast import Lambda
from threading import local
from unicodedata import name
from unittest import result
from mysqlx import Result
import pymysql
import pymysql.cursors

import os

# Connect to the database
connection = pymysql.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="b8854a04772e3b",
    password="0891a25d",
    db="heroku_02e5c32fa545b1e",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )

# with connection.cursor() as cursor:
#     sql =   f"UPDATE userinfo set 1A2Bbest = -1 '"
#     cursor.execute(sql)
# connection.commit()


# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage
# import pymysql
# import time
# import random as rd

# connection = pymysql.connect(
#         host="us-cdbr-east-05.cleardb.net",
#         user="b8854a04772e3b",
#         password="0891a25d",
#         db="heroku_02e5c32fa545b1e",
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
# line_bot_api = LineBotApi('ISGfM1RF3Q+ebtmKd3854wbUBkT05lca8268dGtSPofEYgs7vkZ5grGIWJEBr94fBS/gJMG9NkocJShmM7WlfZdX54OeD0l6WH/unQs7QUKnz+wkW8ZGeFQYHOprfCVMMqzoJlEHB96lXcpZHDNjGAdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('66c4150f2f7451768da6b608807ba3d5')
# with connection.cursor() as cursor:
#     sql = f'''SELECT name from userinfo'''
#     cursor.execute(sql)
#     result = cursor.fetchall()
# print(result)
# with connection.cursor() as cursor:
#     for i in range(len(result)):
#         user_name = line_bot_api.get_profile(result[i]['name']).display_name
#         sql = f'''UPDATE userinfo set user_name='{user_name}' WHERE name = '{result[i]['name']}' '''
#         cursor.execute(sql)
#         connection.commit()




from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, ImageSendMessage, StickerSendMessage, LocationSendMessage
import pymysql
import time
import random as rd
import time as t

connection = pymysql.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b8854a04772e3b",
        password="0891a25d",
        db="heroku_02e5c32fa545b1e",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
line_bot_api = LineBotApi('ISGfM1RF3Q+ebtmKd3854wbUBkT05lca8268dGtSPofEYgs7vkZ5grGIWJEBr94fBS/gJMG9NkocJShmM7WlfZdX54OeD0l6WH/unQs7QUKnz+wkW8ZGeFQYHOprfCVMMqzoJlEHB96lXcpZHDNjGAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('66c4150f2f7451768da6b608807ba3d5')

local = t.localtime()
# local = t.localtime()
# print(local)
if local.tm_mon == 3:
    print(1)
else:
    print(2)
# print(len(str(local.tm_mon)))
# month = (str(local.tm_mon))
# if len(str(local.tm_mon)) == 1:
#     month = '0' + month
# day = str(local.tm_mday)
# if len(day) == 1:
#     day = '0' + day
# date = (str(local.tm_year)[2:4] + month + day)

# with connection.cursor() as cursor:
#     sql = f"""INSERT INTO hwtable (date, HW, exam)
#                  VALUES({int(date)}, 'hahaha', 'no test')"""
#     cursor.execute(sql)
# connection.commit()



# with connection.cursor() as cursor:
#     sql = f"""select * from hwtable where date = 220210"""
#     cursor.execute(sql)
#     resulta = cursor.fetchall()
# print(resulta)
# print(f"""{resulta[0]['date']}作業如下:
# {resulta[0]['hw']}
# {resulta[0]['exam']}""")

# with connection.cursor() as cursor:
#     sql = f"""INSERT INTO userinfo (date, HW, exam)
#             VALUES()"""




with connection.cursor() as cursor:
    sql = f'''SELECT * from userinfo'''
    cursor.execute(sql)
    result = cursor.fetchall()
print(result)
# print(result[0]['name'])
# lst = []
# for i in range(len(result)):
#     if result[i]['role'] == '904':
#         lst.append(result[i]['user_name'])
# print(lst)
# for i in range(len(lst)):
#     print(f'hello {lst[i]}, how are you ahahahah"{i**100}"')
# print(len(lst))



# list1 = []
# with connection.cursor() as cursor:
#     sql = f'''SELECT role from userinfo'''
#     cursor.execute(sql)
#     result1 = cursor.fetchall()
# print(result1)
# for i in range(len(result)):
#     if result1[i]['role'] == '904':
#         print(result[i]['name'])
#         list1.append(result[i]['name'])
# print(list1)
# for i in range(len(list1)):
#     # line_bot_api.push_message(list1[i], TextSendMessage(text='904test'))
#     print(result1[i]['role'])
#     print(list1[i])





# list2 = []
# with connection.cursor() as cursor:
#     for i in range(len(list1)):
#         with connection.cursor() as cursor:
#             print(list1[i])
#             sql = f'''SELECT * from userinfo where user_name="{list1[i]}"''' 
#             cursor.execute(sql)
#             resultA = cursor.fetchone()
#             resultA = resultA['1A2Bbest']
#             print(resultA)
#             list2.append(resultA)
# print(list2)
# dict1 = { list1[i]: list2[i] for i in range(len(list1)) if list2[i] != -1}
# print(dict1)
# lst = sorted(dict1.items(), key=lambda item:item[1])
# user_score = ''
# for i in range(len(lst)):
#     print(f'第{i+1}名:{lst[i][0]}，{lst[i][1]}次')
#     user_score += f'\n第{i+1}名:{lst[i][0]}，{lst[i][1]}次'
# print(user_score)
# with connection.cursor() as cursor:
#     sql = f"UPDATE userinfo set login = 'developer' where user_name = 'james'"
#     cursor.execute(sql)
# connection.commit()
