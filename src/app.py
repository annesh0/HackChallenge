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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)