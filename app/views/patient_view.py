from flask import Blueprint, request, current_app
from http import HTTPStatus
from flask_jwt_extended import decode_token, create_access_token, create_refresh_token
from datetime import timedelta

from app.models.patient_model import PatientModel
from app.serializers.patient_serializer import PatientSerializer

bp_patient = Blueprint('bp_patient', __name__, url_prefix='/patients')

@bp_patient.route('', methods=['POST'])
def create_patient():
    session = current_app.db.session
    body = request.get_json()

    found_patient = PatientModel.query.filter_by(email=body['email']).first()

    if found_patient:
        return {'message': 'Patient already exists'}, HTTPStatus.BAD_GATEWAY

    new_patient = PatientModel(**body)

    session.add(new_patient)
    session.commit()

    serialized = PatientSerializer().dump(new_patient)

    access_token = create_access_token(identity=new_patient.id, expires_delta=timedelta(days=7))
    fresh_token = create_refresh_token(identity=new_patient.id, expires_delta=timedelta(days=14))

    return {
        'patient': serialized,
        'access_token': access_token,
        'fresh_token': fresh_token
    }, HTTPStatus.CREATED


@bp_patient.route('/login', methods=['POST'])
def login():
    body = request.get_json()

    found_patient: PatientModel = PatientModel.query.filter_by(email=body['email']).first()

    if not found_patient or not found_patient.check_password(body['password']):
        return {'message': 'Invalid credentials'}, HTTPStatus.BAD_REQUEST

    access_token = create_access_token(identity=found_patient.id, expires_delta=timedelta(days=7))
    fresh_token = create_refresh_token(identity=found_patient.id, expires_delta=timedelta(days=14))

    return {
        'access_token': access_token,
        'fresh_token': fresh_token
    }, HTTPStatus.OK
