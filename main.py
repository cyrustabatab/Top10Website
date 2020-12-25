from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top_movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(500),nullable=False)
    rating = db.Column(db.Float,nullable=False)
    ranking = db.Column(db.Integer,nullable=False)
    review = db.Column(db.String(250),nullable=False)
    img_url = db.Column(db.String(250),nullable=False)
    
class EditForm(FlaskForm):
    new_rating = StringField("Your rating out of 10")
    new_review = StringField("Your review")
    submit = SubmitField("Update")










@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html",movies=movies)


@app.route("/edit/<int:movie_id>",methods=['GET','POST'])
def edit(movie_id):
    
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():

        new_rating = form.new_rating.data
        new_review = form.new_review.data

        movie.rating = new_rating
        movie.review = new_review

        db.session.commit()

        return redirect(url_for('home'))




    edit_form = EditForm()


    return render_template("edit.html",movie=movie,form=edit_form)









if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
