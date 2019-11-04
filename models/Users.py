from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username=username
        self.password=password
        self.created_at = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'created_at': x.created_at.strftime('%d/%m/%Y %H:%M:%S')
            }
        return list(map(lambda x: to_json(x), UserModel.query.all()))