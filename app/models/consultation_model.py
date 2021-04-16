from sqlalchemy import Column, DateTime, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from . import db


class ConsultationModel(db.Model):
    __tablename__ = 'consultations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date = Column(DateTime(), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey('doctors.id'), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'), nullable=False)
    details = Column(Text())
    status = Column(String(), nullable=False, default="Waiting for confirmation from the doctor")

    doctor = relationship('DoctorModel', backref=backref('consultation_list', lazy='joined'), lazy='joined')
    patient = relationship('PatientModel', backref=backref('consultation_list', lazy='joined'), lazy='joined')
