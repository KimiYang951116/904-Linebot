def AddUserInfo(conn, uid, user_name):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
        result_one = cursor.fetchone()
    if result_one == None:
        with conn.cursor() as cursor:
            sql = f'''INSERT INTO userinfo (name, number, guess_times, behavior, role, login, difficulty, code, user_name, 1A2Bbest)
            VALUES('{uid}', 0, 0, 'None', 'None', 'user', 'None', 0, '{user_name}', -1)'''
            cursor.execute(sql)
    conn.commit()

def CheckUserExistance(conn,uid):
    with conn.cursor() as cursor:
        sql =  f"SELECT * FROM userinfo WHERE name='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    return result_one



def SetDefault(conn, uid):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set guess_times = 0, behavior = 'None', number = 0, difficulty = 0 where name='{uid}'"
        cursor.execute(sql)
    conn.commit()


def SetRole(conn, uid, role):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set role='{role}' where name='{uid}'"
        cursor.execute(sql)
    conn.commit()

def CheckUser(conn, uid, thing):
    with conn.cursor() as cursor:
        sql = f"select * from userinfo where name='{uid}'"
        cursor.execute(sql)
        result = cursor.fetchone()
    print(result)
    thing = result[thing]
    return thing

def GetAllUser(conn, thing):
    with conn.cursor() as cursor:
        sql = f'''SELECT name from userinfo'''
        cursor.execute(sql)
        result = cursor.fetchall()
    list1 = []  
    for i in range(len(result)):
        print(result[i][thing])
        list1.append(result[i][thing])
    print(list1)
    return list1
    
