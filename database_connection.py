import mysql.connector
from api_keys import HOST, DATABASE, USER, PASSWORD

# Configuration to access a mysql database in local. The database will be used as a data source for MindsDB.
db_config = {
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'database': DATABASE,
}
# This function has two objectives:
#   1. Connect to the database
#   2. Execute a query
# The function was built in a way that it can be used to execute different types of query.
# In our case example, we are using it to execute an INSERT query.


def connect_and_execute(args):

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            # we get the specific query statement and the values to fill it.
            # executemany() and commit() permit to execute bath queries, whjich considering the vast amount of short audio segments (i.e. rows)
            # that we have, it is great.
            [query, values] = add_emotions_query(
                args['emotions_data'], args['user_id'])
            cursor.executemany(query, values)
            conn.commit()

    # baisc conncetion error handling
    except ConnectionError as e:
        print(f'Connection Failed: {e}')
    except Exception as e:
        print(f'Exception during query execution: {e}')

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

# the following function returns the query statement and the corresponding values.


def add_emotions_query(emotions_data, user_id):
    values = []
    # the emotion data, which is a list of dictionaries, is converted into a list of tuples.
    # others parameters not measured by hume are addedd (e.g. heart rate, pressure, breath) and initialized to 'semi-null' values
    for data in emotions_data:
        values.append(([user_id, 0.0, 0.0, 0.0] +
                      list(data.values()) + ['no']))
    values = tuple(values)
    # To maintain the simmerity also the query will consider these other non-emotions factors.
    column_names = ["user_id", "Heart Rate BPM", "Pressure", "Breath"] + \
        list(emotions_data[0].keys()) + ["Suggestions/Advices"]
    query = f"INSERT INTO emotions_table ({', '.join(['`' + col + '`' for col in column_names])}) VALUES "
    # While it may not be the most elegant of choices, this code adds a placeholder for each value in the query statement.
    # The number of placeholders is equal to the number of columns in the table.
    # It is costant so can  be hardcoded.
    query += '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    return [query, values]
