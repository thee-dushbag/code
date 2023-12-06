import psycopg2
from flask import Flask, jsonify
from __init__ import cred

app = Flask(__name__)
conn_info = "dbname={database} user={user} password={password} host={host} port={port}".format(**cred)
db = psycopg2.connect(conn_info)


@app.route("/brands")
async def brands():
    cur = db.cursor()
    cur.execute("SELECT brand_id, brand_name FROM brand")
    rows = cur.fetchall()
    cur.close()
    return jsonify([{"brand_id": row[0], "brand_name": row[1]} for row in rows])
