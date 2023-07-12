from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

def cleanup():
    sql = text('DELETE FROM article WHERE "pubDate" < NOW() - INTERVAL \'4 days\';')
    result = db.engine.execute(sql)
    print(f'{result.rowcount} rows deleted')

if __name__ == '__main__':
    cleanup()
