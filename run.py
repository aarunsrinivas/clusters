from flaskapp import socket_io, app, db


socket_io.run(app, debug=True)

