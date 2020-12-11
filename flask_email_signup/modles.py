from flask_email_signup import db

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    locality = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"(id: {self.id}) email: {self.email} --> {self.locality}"

    def return_all_recipients():
        return Recipient.query.all()