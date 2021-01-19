from flaskapp import socket_io, app

socket_io.run(app, debug=True)
