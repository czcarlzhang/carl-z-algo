import psycopg2

from constants import PARAMS

def delete_tables():
    delete_script = 'TRUNCATE ONLY symbols, daily_bars, predict_bars RESTART IDENTITY'

    conn = None
    try:
        conn = psycopg2.connect(**PARAMS)
        cur = conn.cursor()

        cur.execute(delete_script)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
	delete_tables()
