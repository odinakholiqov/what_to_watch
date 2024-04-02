import random
import json
from flask import Flask
from datetime import datetime

# class to work with ORM
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"


db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)


@app.route("/")
def root():
    count = Opinion.query.count()

    if not count:
        return "No movies in DB"

    offset_value = random.randrange(count)

    opinion = Opinion.query.offset(offset_value).first()

    return opinion.text


if __name__ == "__main__":
    app.run()