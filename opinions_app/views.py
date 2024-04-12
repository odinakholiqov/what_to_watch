import random
from .models import Opinion
from .forms import OpinionForm
from flask import abort, render_template, redirect, url_for, flash

from . import app, db

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

