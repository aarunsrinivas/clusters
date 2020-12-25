from flaskapp import app, db
from flaskapp.models import Applicant

db.drop_all()
db.create_all()
a = Applicant()
db.session.add(a)
db.session.commit()

app.run(debug=True)