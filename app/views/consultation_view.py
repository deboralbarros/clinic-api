from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, decode_token
from datetime import timedelta

from app.models.consultation_model import ConsultationModel
from app.serializers.consultation_serializer import ConsultationSerializer

bp_consultation = Blueprint('bp_consultation', __name__, url_prefix='/consultations')


@jwt_required()
@bp_consultation.route('', methods=['POST'])
def create_consultation():
    authorization = request.headers.get('Authorization')

    if not authorization:
        return {'message': 'Required token'}, HTTPStatus.FORBIDDEN

    token = authorization.split()[1]

    try:
        patient_id = decode_token(token)['sub']

        session = current_app.db.session
        body = request.get_json()

        new_consultation = ConsultationModel(doctor_id=body['doctor_id'], patient_id=patient_id, date=body['date'])

        session.add(new_consultation)
        session.commit()

        serialized = ConsultationSerializer().dump(new_consultation)

        return serialized, HTTPStatus.CREATED

    except:
        return {'message': 'Invalid token'}, HTTPStatus.BAD_REQUEST


@jwt_required()
@bp_consultation.route('/<consultation_id>/status', methods=['PATCH'])
def update_status(consultation_id):
    session = current_app.db.session
    body = request.get_json()

    authorization = request.headers.get('Authorization')

    if not authorization:
        return {'message': 'Required token'}, HTTPStatus.FORBIDDEN

    token = authorization.split()[1]

    try:
        doctor_id = decode_token(token)['sub']

        found_consultation: ConsultationModel = ConsultationModel.query.get(consultation_id)

        if doctor_id != str(found_consultation.doctor_id):
            return {'message': 'Not authorized'}, HTTPStatus.FORBIDDEN

        found_consultation.status = body['new_status']

        session.add(found_consultation)
        session.commit()

        serialized = ConsultationSerializer().dump(found_consultation)

        return serialized, HTTPStatus.OK

    except:
        return {'message': 'Invalid token'}, HTTPStatus.BAD_REQUEST
