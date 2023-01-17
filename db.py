from dotenv import load_dotenv
from os import environ as env
from mysql.connector import connect

# loads .env file
load_dotenv()


# create DB connection. Credentials are stored in .env
# opens a connection within query and skips the connection closing
def get_connection():
    connection = connect(
        user=env.get("MYSQL_USER"),
        password=env.get("MYSQL_PASSWORD"),
        host=env.get("MYSQL_HOST"),
        port=env.get("MYSQL_PORT"),
        database=env.get("MYSQL_DATABASE")
    )

    return connection


# query to simplify all funcs. Many = many data or single
def query(connection, q, data=None, many=False, fetch=None):
    cursor = connection.cursor()

    # check if entry data is single or multiple
    if many:
        cursor.executemany(q, data)
    else:
        cursor.execute(q, data)

    # fetch
    if fetch:
        return cursor.fetchall()
    # commit
    else:
        connection.commit()

    cursor.close()


def show_wallet():
    with get_connection() as conn:
        q = "SELECT crypto_name, quantity FROM crypto;"
        res = query(conn, q, fetch=True)
        return res


def extract_name_column():
    with get_connection() as conn:
        q = "SELECT crypto_name FROM crypto;"
        lst = query(conn, q, fetch=True)
        # convert list with tuples to list with str for easy checks
        res = [''.join(i) for i in lst]
        return res


def extract_activities_name_column():
    with get_connection() as conn:
        q = "SELECT crypto_name FROM activities;"
        lst = query(conn, q, fetch=True)
        # convert list with tuples to list with str for easy checks
        res = [''.join(i) for i in lst]
        return res


def extract_owned_assets():
    with get_connection() as conn:
        q = "SELECT crypto_name, quantity FROM crypto;"
        res = query(conn, q, fetch=True)
        return res


def show_single_cryptocurrency_transactions(option):
    with get_connection() as conn:
        q = "SELECT recipient, activity, transferred_quantity, crypto_name, transferred_at FROM activities" \
            " WHERE crypto_name = (%s) ORDER BY transferred_at DESC;"
        data = (option,)
        res = query(conn, q, data, fetch=True)
        return res


def show_all_transactions():
    with get_connection() as conn:
        q = "SELECT recipient, activity, transferred_quantity, crypto_name, transferred_at FROM all_transactions;"
        res = query(conn, q, fetch=True)
        return res


def extract_single_quantity(crypto_name):
    with get_connection() as conn:
        q = "SELECT quantity FROM crypto WHERE crypto_name = (%s);"
        data = (crypto_name,)
        res = query(conn, q, data, fetch=True)
        return res[0][0]


def extract_key(crypto_name):
    with get_connection() as conn:
        q = "SELECT privet_key FROM crypto WHERE crypto_name = (%s);"
        data = (crypto_name,)
        res = query(conn, q, data, fetch=True)
        return res[0][0]


def deposit_new_crypto(crypto_name, quantity, key):
    with get_connection() as conn:
        q = "INSERT INTO crypto (crypto_name, quantity, privet_key) VALUES (%s, %s, %s);"
        data = (crypto_name, quantity, key)
        query(conn, q, data)


def add_to_existing_crypto(quantity, crypto_name):
    with get_connection() as conn:
        q = "UPDATE crypto SET quantity = quantity + (%s) WHERE crypto_name = (%s);"
        data = (quantity, crypto_name)
        query(conn, q, data)


def subtract_from_existing_crypto(quantity, crypto_name):
    with get_connection() as conn:
        q = "UPDATE crypto SET quantity = quantity - (%s) WHERE crypto_name = (%s);"
        data = (quantity, crypto_name)
        query(conn, q, data)


def send_whole_crypto(crypto_name):
    with get_connection() as conn:
        q = "DELETE from crypto WHERE crypto_name = (%s);"
        date = (crypto_name,)
        query(conn, q, date)


# records all crypto movement made by the user
def activity_record(transaction, crypto_name, transferred_quantity, recipient):
    with get_connection() as conn:
        q = "INSERT INTO activities (activity, crypto_name, transferred_quantity, recipient)" \
            " VALUES (%s, %s ,%s ,%s);"
        data = (transaction, crypto_name, transferred_quantity, recipient)
        query(conn, q, data)
