from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/site.db"
api = Api(app)
db = SQLAlchemy(app)
CORS(app)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(150), nullable=False)
    user_phone = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=False)


class FeedbackSchema(Schema):
    user_name = fields.Str(required=True, validate=[
        validate.Length(min=1, error="Поле не может быть пустым"),
        validate.Length(max=200, error="Максимальная длина имени 200 символов")
    ])
    user_email = fields.Str(required=True, validate=[
        validate.Length(min=1, error="Поле не может быть пустым"),
        validate.Length(max=150),
        validate.Email(error="Неверный формат Email")
    ])
    user_phone = fields.Str(
        required=False,
        validate=[validate.Regexp(
            r'^$|\+[1-9][0-9]{6,14}$',
            error="Телефон должен быть в международном формате"
        )])
    message = fields.Str(required=True, validate=[
        validate.Length(min=3, max=1000, error="Сообщене должно быть длиной от 3 до 1000 символов")
    ])


class FeedbackResource(Resource):
    def post(self):
        data = request.get_json()
        feedback_schema = FeedbackSchema()
        errors = feedback_schema.validate(request.json)

        if errors:
            return errors, 400

        feedback = Feedback(
            user_name=data.get('user_name'),
            user_email=data.get('user_email'),
            user_phone=data.get('user_phone', None),
            message=data.get('message'),
        )

        db.session.add(feedback)
        db.session.commit()

        return {"message": "Ваше сообщение успешно отправлено!"}


api.add_resource(FeedbackResource, '/feedback')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(use_reloader=True, host="0.0.0.0")
