import random as rd
from view.general import *

def PrepareGuess(conn, uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    if result_one == None:
        r = GenerateRandomNumGuess(conn, uid)
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO userinfo (name, number, guess_times, behavior, role, login, difficulty, code)
             VALUES('{uid}', 0, 0, 'guessnump', 'None', 'user', 'None', 0)'''
            cursor.execute(sql)
        conn.commit()
    else:
        r = GenerateRandomNumGuess(conn, uid)
        with conn.cursor() as cursor:
            sql = f"UPDATE userinfo set number = 0, guess_times = 0, behavior = 'guessnump' WHERE name='{uid}'"
            cursor.execute(sql)
        conn.commit()
def startguess(conn, uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    if result_one == None:
        r = GenerateRandomNumGuess(conn, uid)
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO userinfo (name, number, guess_times, behavior, role, login, difficulty, code)
             VALUES('{uid}', {r}, 0, 'guessnum', 'None', 'user', 'None', 0)'''
            cursor.execute(sql)
        conn.commit()
    else:
        r = GenerateRandomNumGuess(conn, uid)
        with conn.cursor() as cursor:
            sql = f"UPDATE userinfo set number = {r}, guess_times = 0, behavior = 'guessnum' WHERE name='{uid}'"
            cursor.execute(sql)
        conn.commit()
def GenerateRandomNumGuess(conn, uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    diff = result_one['difficulty']
    if diff == 1:
        r = rd.randint(1,20)
        return r
    if diff == 2:
        r = rd.randint(1,100)
        return r
    if diff == 3:
        r = rd.randint(1,1000)
        return r
    if diff == 4:
        r = rd.randint(1,100000)
        return r

def setdiff(conn, uid, diff):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set difficulty='{diff}' where name='{uid}'"
        cursor.execute(sql)
    conn.commit()
    startguess(conn, uid)

def playguess(conn, uid, utext):
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
        result_one = cursor.fetchone()
    guess_times = result_one['guess_times'] + 1
    number = result_one['number']
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set guess_times='{guess_times}' where name='{uid}'"
        cursor.execute(sql)
    conn.commit()
    if int(utext) > number:
        return '你猜測的數字太大了，請試著猜小一點的數字', guess_times
    elif int(utext) < number:
        return '你猜測的數字太小了，請試著猜大一點的數字', guess_times
    else:
        return 'same', guess_times