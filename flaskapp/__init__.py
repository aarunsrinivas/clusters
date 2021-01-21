from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
import redis
from rq import Queue
from rq_scheduler import Scheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'postgres://dsjxyjwsymcjus:8900c79739b140dec2b343afa8a1f957b8a712c16df1d84' \
	'68cd7d4f038c5a2a3@ec2-3-216-181-219.compute-1.amazonaws.com:5432/d94dpkuqcgqai2'
'''
redis = redis.Redis()
queue = Queue(connection=redis)
scheduler = Scheduler(queue=queue, connection=redis)
'''
db = SQLAlchemy(app)
socket_io = SocketIO(app, cors_allowed_origins='*')
cors = CORS(app)

from flaskapp import routes
from flaskapp import sockets
