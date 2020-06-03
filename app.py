import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db,Actor,Movie

ACTORS_PER_PAGE = 10
MOVIES_PER_PAGE = 10

def paginate_actors(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ACTORS_PER_PAGE
    end = start + ACTORS_PER_PAGE

    actors = [actor.format() for actor in selection]
    current_actors = actors[start:end]

    return current_actors
def paginate_movies(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE

    movies = [movie.format() for movie in selection]
    current_movies = movies[start:end]

    return current_movies

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origins', '*')
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #TODO : view movie and its actors
    # view all movies
    @app.route("/movies")
    def get_movies():
        movies = Movie.query.all()
        formatted_movies = {movie.id: movie.type
                                for movie in movies}
        return jsonify({'success': True,
                        'movies': formatted_movies
                        })
    #TODO : view actors and upcoming movie
    # view actors
    @app.route("/actors", methods=['GET'])
    def get_actors():
        selection = Actor.query.all()
        current_actors = paginate_actors(request, selection)
        if len(current_actors) == 0:
            abort(404)

        movies = Movie.query.all()
        # formatted_movies = [actor.format() for actor in selection]
        formatted_movies = []
        for c in movies:
            formatted_movies.append(c.type)
        return jsonify({'success': True,
                        'actors': current_actors,
                        'movies': formatted_movies,
                        'total_actors': len(selection)
                        })

    # TODO: delete actor
    # delete actor
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id)\
                                      .one_or_none()

            if actor is None:
                abort(404)

            actor.delete()
            selection = Actor.query.all()
            current_actors = paginate_actors(request, selection)

            return jsonify({'success': True,
                            'deleted': actor_id,
                            'actors': current_actors,
                            'total_actors': len(selection)})

        except:
            abort(422)

    # TODO : delete movie
    # delete movie
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id)\
                                      .one_or_none()

            if movie is None:
                abort(404)

            movie.delete()
            selection = Movie.query.all()
            current_movies = paginate_movies(request, selection)

            return jsonify({'success': True,
                            'deleted': movie_id,
                            'movies': current_movies,
                            'total_movies': len(selection)})

        except:
            abort(422)

    # TODO: submit + search actor
    # FormView / submitActor + searchActor
    @app.route("/actors", methods=['POST'])
    def create_actor():
        body = request.get_json()
        new_actor = body.get('actor', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_movie = body.get('movie', None)
        search = body.get('searchTerm', None)
        try:
            if search:
                selection = Actor.query.order_by(Actor.id)\
                                          .filter(Actor.actor
                                                          .ilike('%{}%'
                                                          .format(search)))
                current_actors = paginate_actors(request, selection)
                return jsonify({'success': True,
                                'actors': current_actors,
                                'total_actors': len(selection.all())
                                })
            else:
                actor = Actor(actor=new_actor,
                                    answer=new_answer,
                                    movie=new_movie,
                                    difficulty=new_difficulty)
                actor.insert()

                selection = Actor.query.order_by(Actor.id).all()
                current_actors = paginate_actors(request, selection)
                return jsonify({'success': True,
                                'created': actor.id,
                                'actors': current_actors,
                                'total_actors': len(selection)
                                })
        except:
            abort(422)

    # TODO: view detail movie 
    @app.route("/movies/<int:movie_id>/actors")
    def get_actors_by_movie(movie_id):
        try:
            movie_id = movie_id + 1
            selection = Actor.query\
                                .filter(Actor.movie==movie_id) \
                                .all()
            movies = Movie.query.all()
            formatted_movies = []
            for c in movies:
                formatted_movies.append(c.type)
            current_actors = paginate_actors(request, selection)
            return jsonify({
                            'success': True,
                            'actors': current_actors,
                            'movies': formatted_movies,
                            'current_movie': movie_id,
                            'total_actors': len(selection)
                            })
        except BaseException:
            abort(422)

    # TODO: view detail actor . MODIFY ALL
    @app.route("/actors/<int:movie_id>/actors")
    def get_actors_by_movie(movie_id):
        try:
            movie_id = movie_id + 1
            selection = Actor.query\
                                .filter(Actor.movie==movie_id) \
                                .all()
            actors = Movie.query.all()
            formatted_movies = []
            for c in movies:
                formatted_movies.append(c.type)
            current_actors = paginate_actors(request, selection)
            return jsonify({
                            'success': True,
                            'actors': current_actors,
                            'movies': formatted_movies,
                            'current_movie': movie_id,
                            'total_actors': len(selection)
                            })
        except BaseException:
            abort(422)


    #TODO: schedule view many to many + permission + login info
    # Schedule view
    @app.route("/schedule", methods=['GET'])
    def get_schedule():
        body = request.get_json()
        if not body:
            abort(400)
        # select start - end time and actor and movie
        previous_q = body['previous_actors']
        movie_id = body['quiz_movie']['id']
        movie_id = str(int(movie_id))

        # select ALL
        if movie_id == "0":
            if previous_q is not None:
                actors = Actor.query.filter(
                    Actor.id.notin_(previous_q)).all()
            else:
                actors = Actor.query.all()
        else:
            if previous_q is not None:
                actors = Actor.query.filter(
                    Actor.id.notin_(previous_q),
                    Actor.movie == movie_id).all()
            else:
                actors = Actor.query.filter(
                    Actor.movie == movie_id).all()

        if not actors:  # empty list
            next_actor = False
        else:
            next_actor = random.choice(actors).format()

        return jsonify({
            'success': True,
            'actor': next_actor
        })  

    # errors handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)