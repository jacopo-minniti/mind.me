import mysql.connector
from api_keys import HOST, DATABASE, USER, PASSWORD

db_config = {
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'database': DATABASE,
}

def connect_and_execute(args):

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()

            [query, values] = add_emotions_query(args['emotions_data'], args['user_id'])
            cursor.executemany(query, values)
            conn.commit()



    except ConnectionError as e:
        print(f'Connection Failed: {e}')
    except Exception as e:
        print(f'Exception during query execution: {e}')

    finally:
        if conn is not None and conn.is_connected():
            conn.close()



def add_emotions_query(emotions_data, user_id):
    # promt,    
    #  `Heart Rate BPM` FLOAT,
    #Pressure FLOAT,
    #Breath FLOAT,
    #Transcript TEXT,
    values = []
    for data in emotions_data:
        values.append(([user_id, 0.0, 0.0, 0.0] + list(data.values()) + ['no']))
    values = tuple(values)

    # Add placeholders for the values in the query
    # query = "INSERT INTO emotions_table (user_id, `Heart Rate BPM`, Pressure, Breath, " + ", ".join(emotions_data[0].keys()) + f"`Suggestions/Advices`" + ") VALUES "
    # query += ", ".join(["(" + ", ".join(["%s"] * len(data)) + ")" for data in values])
    column_names = ["user_id", "Heart Rate BPM", "Pressure", "Breath"] + list(emotions_data[0].keys()) + ["Suggestions/Advices"]
    query = f"INSERT INTO emotions_table ({', '.join(['`' + col + '`' for col in column_names])}) VALUES "
    #query += ", ".join(["(" + ", ".join(["%s"] * row) + ")" for row in values[0]])
    query += '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    print(query)

    return [query, values]

