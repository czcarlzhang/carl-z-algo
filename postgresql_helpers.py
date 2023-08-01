import psycopg2
import psycopg2.extras

import pandas as pd

from constants import HOST, DATABASE, USER, PWD, PORT

param_dic = {
    "host"      : str(HOST),
    "database"  : str(DATABASE),
    "user"      : str(USER),
    "password"  : str(PWD),
    "port"      : str(PORT),
    }

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**param_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    print("Connection successful")
    return conn

def insert_symbol(conn, symbol):
    cur = conn.cursor()

    insert_script = 'INSERT INTO symbols (symbol) VALUES(%s)'
    cur.execute(insert_script, (symbol,))

    conn.commit()

def insert_daily_bars(conn, data):
    cur = conn.cursor()

    insert_script = 'INSERT INTO daily_bars (symbol, name, timestamp, open, high, low, close, volume, trade_num, volume_weight) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    for row in data:
        cur.execute(insert_script, row)

    conn.commit()

def get_last_timestamp(conn, symbol):
    cur = conn.cursor()

    fetch_script = 'SELECT timestamp FROM daily_bars WHERE symbol = %s ORDER BY timestamp DESC LIMIT 1'
    cur.execute(fetch_script, (symbol,))

    return cur.fetchone()[0]

# def get_last(conn, symbol):
#     cur = conn.cursor()

#     fetch_script = 'SELECT timestamp, '
#     cur.execute(fetch_script, (symbol,))

    return cur.fetchall()
    
def insert_predict_bars(conn, data):
    cur = conn.cursor()

    insert_script = 'INSERT INTO predict_bars (symbol, name, timestamp, open) VALUES(%s, %s, %s, %s)'
    cur.execute(insert_script, data)

    conn.commit()

def symbol_exists(conn, symbol):
    cur = conn.cursor()

    exists_script = '''
        SELECT EXISTS (
            SELECT 1
            FROM symbols
            WHERE symbol = %s
        )
    '''
    cur.execute(exists_script, (symbol, ))

    return cur.fetchone()[0]

def postgresql_to_dataframe(conn, symbol):
        """
        Tranform a SELECT query into a pandas dataframe
        """
        cursor = conn.cursor()
        try:
            select_query = 'SELECT * FROM daily_bars WHERE symbol = %s'
            cursor.execute(select_query, (symbol,))
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            cursor.close()
            return 1

        tuples = cursor.fetchall()
        cursor.close()
        column_names = [
            'id',
            'symbol',
            'name',
            'timestamp',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'trade_num',
            'volumne_weighted'
        ]
        df = pd.DataFrame(tuples, columns=column_names)
        return df


# conn = None

# try:
#     with psycopg2.connect(
#         host=HOST,
#         database=DATABASE,
#         user=USER,
#         password=PWD,
#         port=PORT
#     ) as cursor:

#         with  conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor

#             #
#             cursor.execute('DROP TABLE IF EXISTS stock_history')

#             create_script = ''' 
#             CREATE TABLE if NOT EXISTS stock_history (
#                 id int PRIMARY KEY,
#                 symbol varchar(5) NOT NULL,
#                 name varchar(40) NOT NULL,
#                 open_price numeric(10, 4),
#                 predicted_price numeric(10, 4)
#             )
#             '''
#             cursor.execute(create_script)

#             insert_script = 'INSERT INTO stock_history (id, symbol, name, open_price, predicted_price) VALUES(%s, %s, %s, %s, %s)'
#             insert_value = (0, 'TEST', 'tester', 123.4567, 120.1234) # put in array to insert multiple rows and for loop the execute
#             cursor.execute(insert_script, insert_value)

#             update_script = 'UPDATE stock_history SET symbol = \'TEST2\' WHERE id = 0'
#             cursor.execute(update_script)


#             delete_script = 'DELETE FROM stock_history WHERE id = %s'
#             delete_record = (0,)
#             cursor.execute(delete_script, delete_record)

#             # show 
#             cursor.execute('SELECT * FROM stock_history')
#             for record in cursor.fetchall():
#                 print(record['symbol']) # can use column name as it is dict now with extras

# except Exception as err:
#     print(err)
# finally:
#     if conn is not None:
#         conn.close()
        
