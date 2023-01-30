# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.values.get("director_id")
        genre_id = request.values.get("genre_id")


        if director_id and genre_id:
            movies_by_director_genre = db.session.query(Movie).filter(Movie.director_id == director_id , Movie.genre_id == genre_id).all()
            return movies_schema.dump(movies_by_director_genre), 200
        elif genre_id:
            movies_by_genre = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
            return movies_schema.dump(movies_by_genre), 200
        elif director_id:
            movies_by_director = db.session.query(Movie).filter(Movie.director_id == director_id).all()
            return movies_schema.dump(movies_by_director), 200

        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        return movie_schema.dump(movie), 200


@director_ns.route('')
class DirectorsView(Resource):
    def get(self):
        all_derector = Director.query.all()
        return directors_schema.dump(all_derector)


    def post(self):
        req_json = request.json
        director = Director(
            id = req_json.get('id'),
            name = req_json.get('name')
        )
        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director), 201

@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def put(self, did):
        director = Director.query.get(did)
        if not director:
            return "", 404

        req_json = request.json
        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director), 204


    def delete(self, did):
        director = Director.query.get(did)
        if not director:
            return "", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route('')
class  GenresView(Resource):
    def get(self):
        genre = Genre.query.all()
        return genres_schema.dump(genre)

    def post(self):
        req_json = request.json
        genre = Genre(
            id = req_json.get('id'),
            name = req_json.get('name')
        )

        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre), 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def put(self, gid):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        req_json = request.json
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre), 204

    def delete(self, gid):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        db.session.delete(genre)
        db.session.commit()
        return genre_schema.dump(genre), 204




if __name__ == '__main__':
    app.run(debug=True)
