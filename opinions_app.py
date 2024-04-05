import random
import json
from flask import Flask, render_template, redirect, url_for, flash, abort
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


# class to work with ORM
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SECRET_KEY"] = "MY_SECRET_KEY"

db = SQLAlchemy(app)


class OpinionForm(FlaskForm):
    title = StringField(
        "Enter movie name",
        validators=[DataRequired(message="Required"), Length(1, 128)],
    )
    text = TextAreaField(
        "Enter your opinion", validators=[DataRequired(message="Required")]
    )
    source = URLField("Enter a link", validators=[Length(1, 256), Optional()])
    submit = SubmitField("Enter")


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(error):
    db.session.rollback()
    return render_template("500.html"), 500


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)


@app.route("/")
def index_view():
    count = Opinion.query.count()

    if not count:
        abort(404)

    offset_value = random.randrange(count)

    opinion = Opinion.query.offset(offset_value).first()

    return render_template("opinion.html", opinion=opinion)


@app.route("/opinion/<int:id>")
def opinion_view(id):

    opinion = Opinion.query.get_or_404(id)

    return render_template("opinion.html", opinion=opinion)


@app.route("/add", methods=["GET", "POST"])
def add_opinion_view():
    form = OpinionForm()

    if form.validate_on_submit():
        text = form.text.data

        if Opinion.query.filter_by(text=text).first() is not None:
            flash("Such opinion already exists")

            return render_template("add_opinion.html", form=form)

        opinion = Opinion(
            title=form.title.data, text=form.text.data, source=form.source.data
        )

        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for("opinion_view", id=opinion.id))

    return render_template("add_opinion.html", form=form)


if __name__ == "__main__":
    app.run()
