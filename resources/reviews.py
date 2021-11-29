import json

from flask import jsonify, Blueprint, g, make_response
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, abort, marshal_with, url_for
import models
from auth import auth

review_fields = {
    "id": fields.Integer,
    "for_course": fields.String,
    "rating": fields.Integer,
    "comment": fields.String,
    "rated_at": fields.DateTime
}


def review_or_404(review_id):
    try:
        review = models.Review.get(models.Review.id == review_id)
    except models.Review.DoesNotExist:
        abort(404, message="Review with id {} does not exist".format(review_id))
    else:
        return review


def add_course(review):
    review.for_course = url_for("courses.course", id=review.course.id)
    return review

def validate_editor(review_id):
    try:
        models.Review.select().where(
            models.Review.created_by == g.user,
            models.Review.id == review_id
        )
    except models.Review.DoesNotExist:
        return make_response(json.dumps(
            {"error": "That review does not exist or is not editable"}
        ), 403)

class ReviewList(Resource):
    def __init__(self):
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument(
            "course",
            required=True,
            type=inputs.positive,
            help="No course provided",
            location=["form", "json"]
        )
        self.regparse.add_argument(
            "rating",
            required=True,
            type=inputs.int_range(1, 5),
            help="No rating provided",
            location=["form", "json"]
        )
        self.regparse.add_argument(
            "comment",
            required=False,
            nullable=True,
            default="",
            location=["form", "json"]
        )
        super().__init__()

    def get(self):
        reviews = [marshal(add_course(review), review_fields) for review in models.Review.select()]
        return {"reviews": reviews}

    @marshal_with(review_fields)
    @auth.login_required
    def post(self):
        args = self.regparse.parse_args()
        review = models.Review.create(created_by=g.user, **args)
        return (add_course(review), 200, {"Location": url_for("reviews.review", id=review.id)})


class Review(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "course",
            required=True,
            type=inputs.positive,
            help="No course provided",
            location=["form", "json"]
        )
        self.reqparse.add_argument(
            "rating",
            required=True,
            type=inputs.int_range(1, 5),
            help="No rating provided",
            location=["form", "json"]
        )
        self.reqparse.add_argument(
            "comment",
            required=False,
            nullable=True,
            default="",
            location=["form", "json"]
        )
        super().__init__()

    @marshal_with(review_fields)
    def get(self, id):
        return add_course(review_or_404(id))

    @marshal_with(review_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        validate_editor(id)

        query = models.Review.update(**args).where(models.Review.id == id)
        query.execute()
        return (add_course(models.Review.get(models.Review.id == id)), 200,
                {"Location": url_for("reviews.review", id=id)})

    @auth.login_required
    def delete(self, id):
        validate_editor(id)
        query = models.Review.delete().where(models.Review.id == id)
        query.execute()
        return ("", 204, {"Location": url_for("reviews.reviews")})


reviews_api = Blueprint('reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    ReviewList,
    '/reviews',
    endpoint='reviews'
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint='review'
)
