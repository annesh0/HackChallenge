from db import db
from db import Course
from db import Assignment
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

@app.route("/api/user/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    if not body.get("username") or not body.get("password") or not body.get("email"):
        return failure_response("missing arguments", 400)
    elif len(body.get("password"))<8:
        return failure_response("Password must be at least 8 characters long", 400)
    new_user = User(username=body.get("username"), password=body.get("password"), email=body.get("email"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize,201)

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
    if body.get("song1"):
        playlist.song1=body.get("song1")
    if body.get("song2"):
            playlist.song1 = body.get("song2")
    if body.get("song3"):
            playlist.song1 = body.get("song3")
    if body.get("song4"):
            playlist.song1 = body.get("song4")
    if body.get("song5"):
            playlist.song1 = body.get("song5")
    return success_response(playlist)

@app.route("/api/playlist/add/<int:user_id>/<int:playlist_id>/<int:remove_id>/", methods=["REMOVE"])
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
    if remove_id==2:
        playlist.song2=""
    if remove_id==3:
        playlist.song3=""
    if remove_id==4:
        playlist.song4=""
    if remove_id==5:
        playlist.song5=""
    return success_response(playlist)

@app.route("/api/playlist/", methods=["POST"])
def create_playlist():
    body = json.loads(request.data)
    if not body.get("username") or not body.get("song1") or not body.get("song2") or not body.get("song2") \
            or not body.get("song3") or not body.get("song4") or not body.get("song5"):
        return failure_response("missing arguments", 400)
    new_playlist = Playlist(username=body.get("username"), song1=body.get("song1"), song2=body.get("song2"),
                            song3=body.get("song3"), song4=body.get("song4"), song5=body.get("song5"))
    db.session.add(new_playlist)
    db.session.commit()
    return success_response(new_playlist.serialize(), 201)

@app.route("/api/users/<str:playlist_name>/")
def get_playlist(playlist_name):
    playlist = Playlist.query.filter(Playlist.name.contains(playlist_name))
    if playlist is None:
        return failure_response("playlist not found")
    return success_response({"playlist": [p.serialize for p in playlist]})

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found")

    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/<int:playlist_id>/", methods=["POST"])
def add_tag(user_id, playlist_id):
    body = json.loads(request.data)
    if not body or body.get("tags"):
        return failure_response("missing arguments", 400)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not playlist:
        return failure_response("playlist not found")
    tagList = ""
    for tag in body.get("tags"):
        tagList += tag
        tagList += "|"
    playlist.tags += taglist
    db.session.commit()
    return succes_response(playlist.serialize(), 201)

@app.route("/api/users/<int:user_id>/<int:playlist_id>/", methods=["REMOVE"])
def remove_tag(user_id, playlist_id):
    body = json.loads(request.data)
    if not body or body.get("tags"):
        return failure_response("missing arguments", 400)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return failure_response("user not found")
    playlist = Playlist.query.filter_by(id=playlist_id).filter_by(user_id=user_id).first()
    if not playlist:
        return failure_response("playlist not found")
    playlist.tags = ""
    db.session.commit()
    return succes_response(playlist.serialize(), 201)

@app.route("/api/tags/<str:tag_name>/")
def get_playlists_by_tag(tag_name):
    return success_response({"playlists": [p.serialize() for p in Playlist.query.filter(Playlist.tags.contains(tag_name))]})

@app.route("/api/<str:username>/")
def get_user_by_username(username):
    query = Playlist.query.filter_by(username=username)
    return success_response({"users": [u.serialize() for u in query]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)