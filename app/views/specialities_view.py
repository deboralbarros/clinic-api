from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus

from app.models.speciality_model import SpecialityModel
from app.serializers.speciality_serializer import SpecialitySerializer

bp_speciality = Blueprint('bp_speciality', __name__, url_prefix='/specialities')


@bp_speciality.route('', methods=['POST'])
def create_speciality():
    session = current_app.db.session
    body = request.get_json()

    found_speciality = SpecialityModel.query.filter(SpecialityModel.name.like(f"%{body['name']}%")).first()

    if found_speciality:
        return {'message': 'Speciality already exists'}, HTTPStatus.BAD_REQUEST

    new_speciality = SpecialityModel(**body)

    session.add(new_speciality)
    session.commit()

    serialized = SpecialitySerializer().dump(new_speciality)

    return serialized, HTTPStatus.CREATED


@bp_speciality.route('')
def get_all_specialities():
    speciality_name = request.args.get('speciality')

    if speciality_name:
        all_specialities = SpecialityModel.query.filter(SpecialityModel.name.like(speciality_name))
    else:
        all_specialities = SpecialityModel.query.all()

    serialized = SpecialitySerializer(many=True).dump(all_specialities)

    return jsonify(serialized)
