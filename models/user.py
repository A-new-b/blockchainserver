from conn.connection import connect


def get_user_by_device_id(device_id) -> dict:
    try:
        db = connect()
        cursor = db.cursor()
        sql = "select user_name as 'username', user_password as 'password', device_id " \
              "from users where device_id = %s"
        cursor.execute(sql, device_id)
        res = cursor.fetchone()
        return res
    except:
        return {}
