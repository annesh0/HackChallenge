from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.String, nullable=False)
    tags = db.Column(db.String)
    song1 = db.Column(db.String, nullable=False)
    song2 = db.Column(db.String, nullable=False)
    song3 = db.Column(db.String, nullable=False)
    song4 = db.Column(db.String, nullable=False)
    song5 = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.tags =  kwargs.get("tags")
        self.song1 = kwargs.get("song1")
        self.song2 = kwargs.get("song2")
        self.song3 = kwargs.get("song3")
        self.song4 = kwargs.get("song4")
        self.song5 = kwargs.get("song5")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "song1": self.song1,
            "song2": self.song2,
            "song3": self.song3,
            "song4": self.song4,
            "song5": self.song5,
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable=False)
    playlists = db.relationship("Playlist", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwarg.get("email")

    def serialize(self):
        list = []
        for i in self.playlists:
            list.append(i.seralize())

        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "playlists": list
        }
