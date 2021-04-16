from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.patient_model import PatientModel
    from app.models.doctor_model import DoctorModel
    from app.models.speciality_model import SpecialityModel
    from app.models.consultation_model import ConsultationModel
