import os
from dotenv import load_dotenv
import psycopg2

conn = psycopg2.connect(
    database=os.getenv('POSTGRE_DB'),
    host=os.getenv('POSTGRE_HOST'),
    port=os.getenv('POSTGRE_PORT'),
    user=os.getenv('POSTGRE_USER'),
    password=os.getenv('POSTGRE_PASSWORD')
)

cursor = conn.cursor()