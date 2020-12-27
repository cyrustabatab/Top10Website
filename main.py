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

API_KEY ='8ef7047d1bb9df6aa4c5472037ed36a4'
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(500),nullable=False)
    rating = db.Column(db.Float,nullable=True)
    review = db.Column(db.String(250),nullable=True)
    ranking = db.Column(db.String(250),nullable=True)
    img_url = db.Column(db.String(250),nullable=False)


    def __repr__(self):
        return f"Movie({self.title},{self.rating},{self.ranking})"
    
class EditForm(FlaskForm):
    new_rating = StringField("Your rating out of 10")
    new_review = StringField("Your review")
    submit = SubmitField("Update")


class AddForm(FlaskForm):

    movie_name = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField("Add Movie")






@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating).all()
    print(movies)

    for i in range(len(movies) - 1,-1,-1):
        movie = movies[len(movies) -1- i]
        movie.ranking = i + 1
    db.session.commit()
    return render_template("index.html",movies=movies)


@app.route("/edit/<int:movie_id>",methods=['GET','POST'])
def edit(movie_id):
    
    form = EditForm()
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():

        new_rating = form.new_rating.data
        new_review = form.new_review.data

        movie.rating = new_rating
        movie.review = new_review

        db.session.commit()

        return redirect(url_for('home'))





    return render_template("edit.html",movie=movie,form=form)




@app.route('/add',methods=['GET','POST'])
def add():
    
    form = AddForm()
    if form.validate_on_submit():

        title = form.movie_name.data

        params = {'query': title,'api_key': API_KEY,'language': 'en-US'}
        search_url = "https://api.themoviedb.org/3/search/movie"
        response = requests.get(search_url,params=params)
        
        movies = response.json()
        movies = movies['results']
        
        
        return render_template('select.html',movies=movies)
        






    return render_template("add.html",form=form)



@app.route("/delete/<int:movie_id>")
def delete(movie_id):


    movie = Movie.query.get(movie_id)

    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/details/<int:movie_id>')
def get_movie_details_and_add(movie_id):
    
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {'api_key': API_KEY,'language': 'en-US'}

    response = requests.get(details_url,params=params)
    
    movie = response.json()
    poster_path = f"https://image.tmdb.org/t/p/original{movie['poster_path']}"

    title = movie['original_title']
    description = movie['overview']
    year = movie['release_date'].split('-')[0]

    new_movie = Movie(title=title,description=description,year=year,img_url=poster_path)
    
    db.session.add(new_movie)

    db.session.commit()


    return redirect(url_for('edit',movie_id=new_movie.id))















if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
