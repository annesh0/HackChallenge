from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    username = db.Column(db.String, nullable=False)
    tags = db.Column(db.String)
    name = db.Column(db.String, nullable = False)
    song1 = db.Column(db.String, nullable=False)
    song2 = db.Column(db.String, nullable=False)
    song3 = db.Column(db.String, nullable=False)
    song4 = db.Column(db.String, nullable=False)
    song5 = db.Column(db.String, nullable=False)
    artist1 = db.Column(db.String, nullable=False)
    artist2 = db.Column(db.String, nullable=False)
    artist3 = db.Column(db.String, nullable=False)
    artist4 = db.Column(db.String, nullable=False)
    artist5 = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.tags =  kwargs.get("tags")
        self.user_id = kwargs.get("user_id")
        self.name = kwargs.get("name")
        self.song1 = kwargs.get("song1")
        self.song2 = kwargs.get("song2")
        self.song3 = kwargs.get("song3")
        self.song4 = kwargs.get("song4")
        self.song5 = kwargs.get("song5")
        self.artist1 = kwargs.get("artist1")
        self.artist2 = kwargs.get("artist2")
        self.artist3 = kwargs.get("artist3")
        self.artist4 = kwargs.get("artist4")
        self.artist5 = kwargs.get("artist5")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "tags": self.tags,
            "name": self.name,
            "song1": self.song1,
            "song2": self.song2,
            "song3": self.song3,
            "song4": self.song4,
            "song5": self.song5,
            "artist1": self.artist1,
            "artist2": self.artist2,
            "artist3": self.artist3,
            "artist4": self.artist4,
            "artist5": self.artist5,
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
        self.email = kwargs.get("email")

    def serialize(self):
        list = []
        for i in self.playlists:
            list.append(i.serialize())

        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "playlists": list
        }
