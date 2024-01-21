from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from marshmallow import Schema, fields, validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
api = Api(app)
db = SQLAlchemy(app)


class Feedback(Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(150), nullable=False)
    user_phone = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=False)


class FeedbackSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(max=200))
    user_email = fields.Str(required=True, validate=[
        validate.Length(max=150),
        validate.Email(error="Invalid Email")
    ])
    user_phone = fields.Str(required=False, validate=[validate.Regexp(r'^\+\d{1,3}\d{1,14}(\s\d{1,13})?$')])
    message = fields.Str(required=True, validate=[validate.Length(min=10, max=1000)])


class FeedbackResource(Resource):
    def post(self):
        feedback_schema = FeedbackSchema()
        errors = feedback_schema.validate(request.json)

        if errors:
            return errors, 400

        feedback = Feedback(
            user_name=request.json['user_name'],
            user_email=request.json['user_email'],
            user_phone=request.json['user_phone'],
            message=request.json['message'],
        )

        db.session.add(feedback)
        db.session.commit()

        return {"msg": "Feedback collected!"}


if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader=True)
