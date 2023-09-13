import os
password = os.getenv('PASSWORD')

cred = {
    'host': 'localhost',
    'port': 5432,
    'user': 'simon',
    'password': password,
    'database': '',
}