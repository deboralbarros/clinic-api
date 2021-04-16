from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import decode_token, create_access_token, create_refresh_token
from datetime import timedelta

from app.models.doctor_model import DoctorModel
from app.models.speciality_model import SpecialityModel
from app.serializers.doctor_serializer import DoctorSerializer
from app.serializers.speciality_serializer import SpecialitySerializer

bp_doctor = Blueprint('bp_doctor', __name__, url_prefix='/doctors')


@bp_doctor.route('/', methods=['POST'])
def create_doctor():
    session = current_app.db.session
    body = request.get_json()

    found_speciality: SpecialityModel = SpecialityModel.query.get(body['speciality_id'])

    new_doctor = DoctorModel(**body)

    session.add(new_doctor)
    session.commit()

    serialized = DoctorSerializer().dump(new_doctor)

    access_token = create_access_token(identity=new_doctor.id, expires_delta=timedelta(days=7))
    fresh_token = create_refresh_token(identity=new_doctor.id, expires_delta=timedelta(days=14))

    return {
        'doctor': serialized,
        'access_token': access_token,
        'fresh_token': fresh_token
    }, HTTPStatus.CREATED


@bp_doctor.route('/login/', methods=['POST'])
def login():
    body = request.get_json()

    found_doctor: DoctorModel = DoctorModel.query.filter_by(email=body['email']).first()

    if not found_doctor or not found_doctor.check_password(body['password']):
        return {'message': 'Invalid credentials'}, HTTPStatus.BAD_REQUEST

    access_token = create_access_token(identity=found_doctor.id, expires_delta=timedelta(days=7))
    fresh_token = create_refresh_token(identity=found_doctor.id, expires_delta=timedelta(days=14))

    return {
        'access_token': access_token,
        'fresh_token': fresh_token
    }, HTTPStatus.OK


@bp_doctor.route('/')
def get_all_doctors():
    all_doctors = DoctorModel.query.all()

    serialized = DoctorSerializer(many=True).dump(all_doctors)

    return jsonify(serialized), HTTPStatus.OK
