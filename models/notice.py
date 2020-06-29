from conn.connection import connect


def get_notices() -> dict:
    try:
        db = connect()
        cursor = db.cursor()
        sql = "select id, title, content, unix_timestamp(create_time) as create_time " \
              "from notices"
        cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except:
        return {}
