from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with, abort, url_for
import models
from auth import auth
from common.helpers import error_response

course_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "url": fields.String,
    "reviews": fields.List(fields.String)
}


def add_reviews(course):
    course.reviews = [url_for("reviews.review", id=review.id)
                      for review in course.review_set]
    return course


def course_or_404(course_id):
    try:
        course = models.Course.get(models.Course.id == course_id)
    except models.Course.DoesNotExist:
        abort(404, message="Course with id {} does not exist".format(course_id))
    else:
        return course


class CourseList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            "title",
            required=True,
            help="No course title provided",
            location=["form", "json"]
        )
        self.reqparse.add_argument(
            "url",
            required=True,
            help="No course URL provided",
            location=["form", "json"],
            type=inputs.url
        )
        super().__init__()

    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        try:
            course = models.Course.create(**args)
            return (add_reviews(course),201, {"Location": url_for("courses.course", id=course.id)})
        except Exception as ex:
            return error_response(400, ex.args[0])

    def get(self):
        courses = [marshal(add_reviews(course), course_fields) for course in models.Course.select()]
        return {"courses": courses}


class Course(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "title",
            required=True,
            help="No course title provided",
            location=["form", "json"]
        )
        self.reqparse.add_argument(
            "url",
            required=True,
            help="No course URL provided",
            location=["form", "json"]
        )
        super().__init__()

    @marshal_with(course_fields)
    def get(self, id):
        return add_reviews(course_or_404(id))

    @marshal_with(course_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Course.update(**args).where(models.Course.id == id)
        query.execute()
        return (add_reviews(models.Course.get(models.Course.id == id)), 200,
            {"Location": url_for("courses.course", id=id)})

    @auth.login_required
    def delete(self, id):
        query = models.Course.delete().where(models.Course.id == id)
        query.execute()
        return ("", 204, {"Location": url_for("courses.courses")})


courses_api = Blueprint('courses', __name__)
api = Api(courses_api)
api.add_resource(CourseList,
                 '/api/v1/courses',
                 endpoint='courses'
                 )
api.add_resource(Course,
                 '/api/v1/courses/<int:id>',
                 endpoint='course'
                 )
