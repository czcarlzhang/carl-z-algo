import psycopg2

from constants import PARAMS

def create_tables():
    commands = (
        '''
        CREATE TABLE IF NOT EXISTS symbols (
            id serial PRIMARY KEY,
            symbol varchar(5) NOT NULL
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS daily_bars (
            id serial PRIMARY KEY,
            symbol varchar(5) NOT NULL,
            name varchar(40) NOT NULL,
            timestamp timestamp,
            open numeric(15, 5),
            high numeric(15, 5),
            low numeric(15, 5),
            close numeric(15, 5),
            volume bigint,
            trade_num bigint,
            volume_weight numeric(20, 10)
        )
        ''',
		'''
        CREATE TABLE IF NOT EXISTS predict_bars(
			id serial PRIMARY KEY,
            symbol varchar(5) NOT NULL,
            name varchar(40) NOT NULL,
            timestamp timestamp,
            open numeric(15, 5)
        )
        '''
    )

    conn = None
    try:
        conn = psycopg2.connect(**PARAMS)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
	create_tables()
