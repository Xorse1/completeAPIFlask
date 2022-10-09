from flask import Flask, redirect, jsonify
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.database import Bookmark
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config

db = SQLAlchemy()
DB_NAME = "bookmarks.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6657HGFGFGHHDHDHFGG'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'
    SWAGGER={
        'title':"Bookmarks API",
        'uiversion': 3
    }
    db.init_app(app)

    #This for user management
    JWTManager(app)

    from .auth import auth
    from .bookmarks import bookmarks
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)


    @app.route('/<short_url>', methods=['GET'])
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits=bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)


    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error':'Not Found'}), HTTP_404_NOT_FOUND


    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error':'SOmething went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR



    return app









