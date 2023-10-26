from typing import TypedDict, Callable
from os import getenv
import pymysql as sql
from pymysql.cursors import Cursor
from faker import Faker
from random import choice, randint

DATABASE = getenv("SQL_DATABASE")
PASSWORD = getenv("SQL_PASSWORD")

assert DATABASE and PASSWORD, "SQL_DATABASE or SQL_PASSWORD was not set."


class DBCred(TypedDict):
    user: str
    password: str
    database: str
    host: str
    port: int


cred = DBCred(
    user="simon", host="localhost", database=DATABASE, password=PASSWORD, port=3306
)

fake = Faker()
EMAIL_PROVIDERS = ["@gmail.com", "@yahoo.mail", "@outlook.com", "@hotmail.com"]

genemail: Callable[[str], str] = lambda name: name.replace(" ", "").lower() + choice(
    EMAIL_PROVIDERS
)


def insert_users(cur: Cursor):
    users = (dict(name=(n := fake.name()), email=genemail(n)) for _ in range(20))
    sqlexec = "INSERT INTO users VALUES (default, %(name)s, %(email)s)"
    cur.executemany(sqlexec, users)


def insert_students(cur: Cursor, count: int = 10):
    sqlexec = "INSERT INTO students VALUES (default, %(name)s);"
    student_names = (dict(name=fake.name()) for _ in range(count))
    cur.executemany(sqlexec, student_names)


def insert_grades(cur: Cursor):
    sidsql = "SELECT sid FROM students;"
    cur.execute(sidsql)
    grades = (dict(sid=sid, score=randint(10, 90)) for sid, in cur.fetchall())
    # print(list(grades))
    cur.executemany("INSERT INTO grades VALUES (default, %(sid)s, %(score)s)", grades)


def main():
    with sql.connect(**cred, autocommit=True) as conn:
        with conn.cursor() as cur:
            # insert_users(cur)
            # insert_students(cur, 20)
            insert_grades(cur)


if __name__ == "__main__":
    main()
