import sqlite3
import pickle


def getdata(id:int):
    database = sqlite3.connect("userdb.db")
    data = database.execute("select data from USER where id=?", (id,)).fetchone()
    try:
        datapack = pickle.loads(data[0])
        database.close()
        return datapack
    except:
        return None

def getname(id:int):
    database = sqlite3.connect("userdb.db")
    data = database.execute("select username from USER where id=?", (id,)).fetchone()
    try:
        username = data[0]
        database.close()
        return username
    except:    
        return f"Error <user/{id}> is not found"

def getpoint(id:int):
    data = getdata(id)
    if data is None:
        return 0
    else:
        return data['point']

def getsolve(id:int):
    data = getdata(id)
    if data is None:
        return []
    else:
        return data['solve']

def getranklist():
    database = sqlite3.connect("userdb.db")
    data_list = database.execute("SELECT id, username, data FROM USER").fetchall()
    filtered_data_list = [x for x in data_list if x[2] is not None]
    print(filtered_data_list)
    filtered_decoded_list = [(x[0], x[1], pickle.loads(x[2])) for x in filtered_data_list]
    print(filtered_decoded_list)
    sorted_data = sorted(filtered_decoded_list, reverse=True, key=lambda x: x[2]['point'])
    current_rank = 1
    previous_point = None
    rank_list =[]

    for index, user in enumerate(sorted_data):
        id, username, data = user
        point = data.get('point', 0)
        
        if point != previous_point:
            current_rank = index + 1
        
        rank_list.append(
            {
                'rank' : current_rank,
                'id': id, 
                'username': username, 
                'point':point
            }
        )
        previous_point = point
    database.close()
    return rank_list
    

def getrank(user_id: int):
    ranklist=getranklist()
    for user in ranklist:
        if user['id'] == user_id:
            return user['rank']
    return None