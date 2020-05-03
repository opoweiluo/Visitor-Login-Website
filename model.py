from app import db

class UserRegister(db.Model):
    __tablename__ = 'UserRegisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    hostname = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return 'username:%s, hostname=%s' % (self.username, self.hostname)