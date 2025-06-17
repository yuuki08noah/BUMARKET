import pymysql
import redis
from pymysql import Connection
from typing import Optional

from pymysql.cursors import Cursor

con: Optional[Connection] = None
cur: Optional[Cursor] = None

def get_db_connection() -> Connection:
    return pymysql.connect(
        host="localhost",
        port=7777,
        user="root",
        password="1234",
        db="bumarket",
        charset="utf8"
    )

con = get_db_connection()
cur = con.cursor()
