from app.models.doctor_model import DoctorModel
from marshmallow.fields import Nested
from . import ma

class DoctorSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        exclude = ('password_hash',)
        model = DoctorModel

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()

    speciality = Nested('SpecialitySerializer', exclude=['doctors_list'])
