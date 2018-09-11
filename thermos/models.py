from datetime import datetime
from thermos.views import db
from sqlalchemy import desc


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Bookmark {} : {}".format(self.description, self.url)

    @staticmethod
    def new_bookmarks(user, num):
        return Bookmark.query.filter_by(user_id=user.get('id')).order_by(desc(Bookmark.date)).limit(num)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), nullable=False, unique=False)
    email = db.Column(db.String(30), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    @staticmethod
    def valid_user(username, password):
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return True, user
        return False, None

    def to_json(self):
        return {'username': self.username, 'id': self.id}

    def __repr__(self):
        return "User {}".format(self.username)