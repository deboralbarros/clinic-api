from app.models.patient_model import PatientModel
from marshmallow.fields import List, Nested
from . import ma


class PatientSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        exclude = ('password_hash',)
        model = PatientModel

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    age = ma.auto_field()
    weight = ma.auto_field()
    height = ma.auto_field()

    consultation_list = List(Nested('ConsultationSerializer', exclude=['patient']))
