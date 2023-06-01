from configparser import ConfigParser
import psycopg2

def config(filename = 'config/database.cfg', section = 'DATABASE'):
    parser = ConfigParser()
    parser.read(filename)

    database = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            database[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file.'.format(section, filename))
    return database

def connect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        print('Connected to the PostgreSQL database...')
    except:
        print('Not connected to the PostgreSQL database...')
    return conn

def create_table(database_name):
    conn = connect()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS " + database_name + " (time VARCHAR(50), status VARCHAR(50), image BYTEA NOT NULL)")
        cur.close()
        conn.commit()

def insert_to_database(database_name, variable_name, variable_value, data_log):
    conn = connect()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("INSERT INTO " + database_name + "(" + variable_name + ") VALUES(" + variable_value + ");", (data_log))          
        cur.close()
        conn.commit()
        conn.close()