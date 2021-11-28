from flask import jsonify, Blueprint
from flask_restful import Resource, Api
import models


class RevieweList(Resource):
    def get(self):
        return jsonify({"courses": [{"course": 1, "rating": 5}]})


class Review(Resource):
    def get(self: id):
        return jsonify({"course": 1, "rating": 5})

    def put(self: id):
        return jsonify({"course": 1, "rating": 5})

    def delete(self: id):
        return jsonify({"course": 1, "rating": 5})

reviews_api = Blueprint('reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    RevieweList,
    '/reviews',
    endpoint='reviews'
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint='review'
)