from flaskapp import socket_io, app, db
from flaskapp.models import ClusterWorld

db.drop_all()
db.create_all()
world = ClusterWorld(id='Tech')
db.session.add(world)
db.session.commit()
socket_io.run(app, debug=True)
