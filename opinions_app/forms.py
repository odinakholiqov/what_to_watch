from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


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
