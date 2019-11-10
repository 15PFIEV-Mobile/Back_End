from run import db

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_token'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)