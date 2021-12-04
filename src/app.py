from db import db
from db import Playlist
from db import User

from flask import Flask
from flask import request

import json
import os

app = Flask(__name__)
db_filename = "songs.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/api/playlists/")
def get_playlists():
    return success_response({"playlists": [p.serialize() for p in Playlist.query.all()]})

@app.route("/api/users/")
def get_all_users():
    return success_response({"users": [u.serialize() for u in User.query.all()]})

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    if not body.get("name") or not body.get("username"):
        return failure_response("missing arguments", 400)
    elif body.get("password") and len(body.get("password"))<8:
        return failure_response("Password must be at least 8 characters long", 400)
    new_user = User(name=body.get("name"), username=body.get("username"), password=body.get("password"), email=body.get("email"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/playlist/add/<int:user_id>/<int:playlist_id>/", methods=["POST"])
def add_song(user_id,playlist_id):
    body = json.loads(request.data)
    if not body:
        return failure_response("Enter a song",400)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not playlist:
        return failure_response("playlist not found")
    if body.get("song1") and body.get("artist1"):
        playlist.song1=body.get("song1")
        playlist.artist1=body.get("artist1")
    if body.get("song2") and body.get("artist2"):
        playlist.song2 = body.get("song2")
        playlist.artist2 = body.get("artist2")
    if body.get("song3") and body.get("artist3"):
        playlist.song3 = body.get("song3")
        playlist.artist3 = body.get("artist3")
    if body.get("song4") and body.get("artist4"):
        playlist.song4 = body.get("song4")
        playlist.artist4 = body.get("artist4")
    if body.get("song5") and body.get("artist5"):
        playlist.song5 = body.get("song5")
        playlist.artist5 = body.get("artist5")
    return success_response(playlist.serialize())

@app.route("/api/playlist/remove/<int:user_id>/<int:playlist_id>/<int:remove_id>/", methods=["DELETE"])
def remove_song(user_id,playlist_id,remove_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not remove_id>0 and not remove_id<6:
        return failure_response("Enter a valid song to remove",400)
    if not playlist:
        return failure_response("playlist not found")
    if remove_id==1:
        playlist.song1=""
        playlist.artist1 = ""
    if remove_id==2:
        playlist.song2=""
        playlist.artist2=""
    if remove_id==3:
        playlist.song3=""
        playlist.artist3 = ""
    if remove_id==4:
        playlist.song4=""
        playlist.artist24= ""
    if remove_id==5:
        playlist.song5=""
        playlist.artist5 = ""
    return success_response(playlist.serialize())

@app.route("/api/playlist/<int:user_id>/", methods=["POST"])
def create_playlist(user_id):
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    if not body.get("name") or not body.get("song1") or not body.get("song2") or not body.get("song2") \
            or not body.get("song3") or not body.get("song4") or not body.get("song5") or not body.get("artist1") \
            or not body.get("artist2") or not body.get("artist3") or not body.get("artist4") or not body.get("artist5"):
        return failure_response("missing arguments", 400)
    new_playlist = Playlist(user_id = user_id, name=body.get("name"), tags = "", username = user.serialize().get("username"), song1=body.get("song1"), song2=body.get("song2"),
                            song3=body.get("song3"), song4=body.get("song4"), song5=body.get("song5"), artist1=body.get("artist1"), artist2=body.get("artist2"),
                            artist3=body.get("artist3"), artist4=body.get("artist4"), artist5=body.get("artist5"))
    db.session.add(new_playlist)
    db.session.commit()
    return success_response(new_playlist.serialize(), 201)

@app.route("/api/users/<playlist_name>/")
def get_playlist(playlist_name):
    playlist_name = str(playlist_name)
    playlist = Playlist.query.filter(Playlist.name.contains(playlist_name))
    if playlist is None:
        return failure_response("playlist not found")
    return success_response({"playlist": [p.serialize() for p in playlist]})

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found")

    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/<int:playlist_id>/", methods=["POST"])
def add_tag(user_id, playlist_id):
    body = json.loads(request.data)
    if not body or not body.get("tags"):
        return failure_response("missing arguments", 400)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not playlist:
        return failure_response("playlist not found")
    tagList = ""
    for tag in body.get("tags"):
        tagList = tagList + tag
        tagList = tagList + "|"
    playlist.tags = str(playlist.tags) + tagList
    db.session.commit()
    return success_response(playlist.serialize(), 201)

@app.route("/api/users/<int:user_id>/<int:playlist_id>/", methods=["DELETE"])
def remove_tag(user_id, playlist_id):
    body = json.loads(request.data)
    if not body or not body.get("tags"):
        return failure_response("missing arguments", 400)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not playlist:
        return failure_response("playlist not found")
    playlist.tags = ""
    db.session.commit()
    return success_response(playlist.serialize(), 201)

@app.route("/api/tags/<string:tag_name>/")
def get_playlists_by_tag(tag_name):
    return success_response({"playlists": [p.serialize() for p in Playlist.query.filter(Playlist.tags.contains(tag_name))]})

@app.route("/api/<string:username>/")
def get_user_by_username(username):
    query = Playlist.query.filter_by(username=username)
    return success_response({"users": [u.serialize() for u in query]})

@app.route("/api/clear/", methods=["POST"])
def drop_tables():
    User.__table__.drop(db.engine)
    Playlist.__table__.drop(db.engine)
    return success_response("cleared tables")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)