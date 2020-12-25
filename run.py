from flaskapp import app, db
from flaskapp.models import Applicant

db.drop_all()
db.create_all()
a = Applicant(name='hey', email='bigguy@gmail.com', password='djhgkjsdhf', features={})
db.session.add(a)
db.session.commit()
app.run(debug=True)
