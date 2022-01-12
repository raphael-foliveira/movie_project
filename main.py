from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy import Integer, Column, String
from flask_sqlalchemy import SQLAlchemy
from tmdb_requests import find_movie
from forms import MovieForm, EditRatingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie_database.db"
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(length=200))
    year = Column(String(length=200))
    description = Column(String(length=400))
    rating = Column(String(length=200))
    ranking = Column(String(length=200))
    review = Column(String(length=200))
    img_url = Column(String(length=200))


@app.route("/")
def home():
    all_movies = [movie for movie in db.session.query(Movie).all()]
    movie_rankings = [movie.ranking for movie in db.session.query(Movie).all()]
    movie_rankings.sort()
    sorted_movies = []
    for ranking in movie_rankings:
        for movie in all_movies:
            if movie.ranking == ranking:
                sorted_movies.append(movie)
    return render_template("index.html", movies=sorted_movies)


@app.route("/add", methods=["get", "post"])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        movie_info = find_movie(form.title.data)
        new_movie = Movie(
            title=movie_info[0],
            year=movie_info[1],
            description=movie_info[2],
            rating=movie_info[3],
            img_url=movie_info[4],
            ranking=form.ranking.data,
            review=form.review.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route("/edit/<movie_title>", methods=["get", "post"])
def edit(movie_title):
    form = EditRatingForm()
    if form.validate_on_submit():
        movie_to_edit = db.session.query(Movie).filter_by(title=movie_title).first()
        movie_to_edit.rating = form.new_rating.data
        movie_to_edit.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie_title)


@app.route("/select")
def select():
    return render_template("select.html")


@app.route("/delete/<movie_title>")
def delete(movie_title):
    movie_to_delete = db.session.query(Movie).filter_by(title=movie_title).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
