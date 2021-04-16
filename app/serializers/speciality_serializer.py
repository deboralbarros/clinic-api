from app.models.speciality_model import SpecialityModel
from marshmallow.fields import Nested, List
from . import ma


class SpecialitySerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpecialityModel

    id = ma.auto_field()
    name = ma.auto_field()

    doctors_list = List(Nested('DoctorSerializer', exclude=['speciality']))
