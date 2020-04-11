#from Utils import SCORES_FILE_NAME
import pymysql
import os


db_conn = None
is_connected = False

def connect_db():
    global db_conn, is_connected

    if not is_connected:
        db_server = os.getenv("MYSQL_DB_SERVER")
        db_port = int(os.getenv("MYSQL_DB_PORT"))
        db_name = os.getenv("MYSQL_DB_NAME")
        db_username = os.getenv("MYSQL_DB_USERNAME")
        db_password = os.getenv("MYSQL_DB_PASSWORD")
        db_conn = pymysql.connect(host=db_server, port=db_port,
                               user=db_username, passwd=db_password,
                               db=db_name, autocommit=True)
        is_connected = True


def disconnect_db():
    global db_conn, is_connected
    db_conn.close()
    is_connected = False


def read_score_from_db():
    global db_conn
    with db_conn.cursor() as cursor:
        cursor.execute("select score from users_scores")
        for score_row in cursor:
            return score_row[0]


def save_score_to_db(score):
    global db_conn
    with db_conn.cursor() as cursor:
        cursor.execute(f"update users_scores set score = {score}")


def add_score(difficulty):
    score = read_score_from_db()
    new_score = score + (difficulty * 3) + 5
    save_score_to_db(new_score)

def test():
    global is_connected, db_conn
    print(f"db server = {os.getenv('MYSQL_DB_SERVER')}")
    print(f"db port = {os.getenv('MYSQL_DB_PORT')}")
    print(f"db name = {os.getenv('MYSQL_DB_NAME')}")
    print(f"db user = {os.getenv('MYSQL_DB_USERNAME')}")
    print(f"db pass = {os.getenv('MYSQL_DB_PASSWORD')}")
    print(f"is connected = {is_connected}")
    connect_db()
    print(f"is connected = {is_connected}")
    print(f"score = {read_score_from_db()}")
    disconnect_db()

if __name__ == '__main__':
    test()
"""def read_score_from_file():
    score = None
    try:
        with open(SCORES_FILE_NAME, "r") as file:
            score = int(file.readline())
    except:
        score = 0
    return score

def save_score_to_file(score):
    with open(SCORES_FILE_NAME, "w") as file:
        file.write(str(score))

def add_score(difficulty):
    score = read_score_from_file()
    new_score = score + (difficulty * 3) + 5
    save_score_to_file(new_score)
"""



