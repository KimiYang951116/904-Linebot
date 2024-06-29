import random as rd
from view.general import *


def Start1a2b(conn, uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    if result_one == None:
        r = GenerateRandomNum1A2B()
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO userinfo (name, number, guess_times, behavior, role, login, difficulty, code)
             VALUES('{uid}', 0, 0, '1A2B', 'None', 'user', 'None', 0)'''
            cursor.execute(sql)
        conn.commit()
    else:
        beha = CheckUser(conn, uid, 'behavior')
        if beha != '1A2B':
            r = GenerateRandomNum1A2B()
            with conn.cursor() as cursor:
                sql = f"UPDATE userinfo set number = {r}, guess_times = 0, behavior = '1A2B' WHERE name='{uid}'"
                cursor.execute(sql)
            conn.commit()

def GenerateRandomNum1A2B():
    r = rd.randint(1000,9999)
    while len(set(list(str(r)))) != 4:
        r = rd.randint(1000,9999)
    return r

def Play1A2B(conn, uid, utext):
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
        result_one = cursor.fetchone()
    guess_times = result_one['guess_times'] + 1
    number = result_one['number']
    a = 0
    b = 0
    number = list(str(number))
    utext = list(str(utext))
    for i in range(0,4):
        if number[i] == utext[i]:
            a += 1
            utext[i] = 'f'
            number[i] = 'a'
    for j in range(0,4):
        for k in range(0,4):
            if number[j] == utext[k]:
                b += 1
                utext[k] = 's'
                number[j] = 'z'
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set guess_times = {guess_times} WHERE name='{uid}'"
        cursor.execute(sql)
    conn.commit()
    return f'{a}A{b}B', guess_times

def Set1A2BBest(conn, uid, times):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set 1A2Bbest='{times}' where name='{uid}'"
        cursor.execute(sql)
    conn.commit()
def GetBestScore(conn):
    with conn.cursor() as cursor:
        sql = f'''SELECT user_name from userinfo'''
        cursor.execute(sql)
        result = cursor.fetchall()
    list1 = []
    for i in range(len(result)):
        print(result[i]['user_name'])
        list1.append(result[i]['user_name'])
    print(list1)
    list2 = []
    with conn.cursor() as cursor:
        for i in range(len(list1)):
            with conn.cursor() as cursor:
                print(list1[i])
                sql = f'''SELECT * from userinfo where user_name="{list1[i]}"''' 
                cursor.execute(sql)
                resultA = cursor.fetchone()
                resultA = resultA['1A2Bbest']
                print(resultA)
                list2.append(resultA)
    print(list2)
    dict1 = { list1[i]: list2[i] for i in range(len(list1)) if list2[i] != -1}
    print(dict1)
    lst = sorted(dict1.items(), key=lambda item:item[1])
    user_score = ''
    for i in range(len(lst)):
        print(f'第{i+1}名:{lst[i][0]}，{lst[i][1]}次')
        user_score += f'第{i+1}名:{lst[i][0]}，{lst[i][1]}次\n'
    print(user_score)
    return user_score