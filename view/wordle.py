from view.general import *
import pandas as pd
import random as rd
import time as t
def StartWordle(conn, uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    if result_one == None:
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO userinfo (name, number, guess_times, behavior, role, login, difficulty, code)
             VALUES('{uid}', 0, 0, 'wordle', 'None', 'user', 'None', 0)'''
            cursor.execute(sql)
        conn.commit()
    else:
        beha = CheckUser(conn, uid, 'behavior')
        if beha != 'wordle':
            with conn.cursor() as cursor:
                sql = f"UPDATE userinfo set guess_times = 0, behavior = 'wordle' WHERE name='{uid}'"
                cursor.execute(sql)
            conn.commit()
def GetDailyWord(day):
    englishwords = pd.read_json("words_dictionary.json",typ="series")
    englishwords = englishwords.keys()
    englishwords = list(englishwords)
    for i in range(len(englishwords)-1, -1, -1):
        if len(englishwords[i]) != 5:
            englishwords.pop(i)
    print(len(englishwords))
    rd.seed(day // 86400)
    ranword = rd.randint(0,15917)
    return englishwords[ranword]


def Playwordle(conn, uid, utext):
    utext = utext.lower()
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
        result_one = cursor.fetchone()
    guess_times = result_one['guess_times'] + 1
    a = 0
    b = 0
    c = 0
    word = GetDailyWord(t.time())
    word = list(str(word))
    utext = list(str(utext))
    for i in range(0,5):
        if word[i] == utext[i]:
            word[i] = 'gg'
            utext[i] = 'green'
    for j in range(0,5):
        for k in range(0,5):
            if word[j] == utext[k]:
                b += 1
                utext[k] = 'yellow'
                word[j] = 'yy'
    result = ''
    for i in range(len(utext)):
        if utext[i] == 'green':
            result += 'A'
        elif utext[i] == 'yellow':
            result += 'B'
        else:
            result += 'C'
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set guess_times = {guess_times} WHERE name='{uid}'"
        cursor.execute(sql)
    conn.commit()
    return result, guess_times

def checkifwordvaild(word):
    word = word.lower()
    isaword = False
    englishwords = pd.read_json("words_dictionary.json",typ="series")
    englishwords = englishwords.keys()
    englishwords = list(englishwords)
    for i in range(len(englishwords)-1, -1, -1):
        if len(englishwords[i]) != 5:
            englishwords.pop(i)
    for i in range(len(englishwords)):
        if englishwords[i] == word:
            isaword = True
            break
    return isaword