from application import db

class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(150), nullable=True)
    done = db.Column(db.Boolean, nullable=False,default=False)
