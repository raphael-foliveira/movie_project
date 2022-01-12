from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    ranking = StringField("Ranking", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField()


class EditRatingForm(FlaskForm):
    new_rating = StringField("New Rating", validators=[DataRequired()])
    new_review = StringField("New Review", validators=[DataRequired()])
    submit = SubmitField()