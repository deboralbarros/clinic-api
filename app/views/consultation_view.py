from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import decode_token
from datetime import timedelta

from app.models.consultation_model import ConsultationModel
from app.serializers.consultation_serializer import ConsultationSerializer

bp_consultation = Blueprint('bp_consultation', __name__, url_prefix='/consultations')


@bp_consultation.route('/', methods=['POST'])
def create_consultation():
    session = current_app.db.session
    body = request.get_json()

    new_consultation = ConsultationModel(**body)

    session.add(new_consultation)
    session.commit()

    serialized = ConsultationSerializer().dump(new_consultation)

    return serialized, HTTPStatus.CREATED
