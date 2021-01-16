from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import redis
from rq import Queue
from rq_scheduler import Scheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
'''
redis = redis.Redis()
queue = Queue(connection=redis)
scheduler = Scheduler(queue=queue, connection=redis)
'''
db = SQLAlchemy(app)
socket_io = SocketIO(app, cors_allowed_origins='*')

from flaskapp import routes
from flaskapp import sockets
