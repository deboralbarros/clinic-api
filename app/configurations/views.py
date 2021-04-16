from flask import Flask


def init_app(app: Flask):
    from app.views.patient_view import bp_patient
    app.register_blueprint(bp_patient)

    from app.views.doctor_view import bp_doctor
    app.register_blueprint(bp_doctor)

    from app.views.specialities_view import bp_speciality
    app.register_blueprint(bp_speciality)

    from app.views.consultation_view import bp_consultation
    app.register_blueprint(bp_consultation)
