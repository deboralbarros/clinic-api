from app.models.consultation_model import ConsultationModel
from marshmallow.fields import Nested
from . import ma

class ConsultationSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConsultationModel

    id = ma.auto_field()
    date = ma.auto_field()
    details = ma.auto_field()
    status = ma.auto_field()

    doctor = Nested('DoctorSerializer', exclude=['consultation_list'])
    patient = Nested('PatientSerializer', exclude=['consultation_list'])
