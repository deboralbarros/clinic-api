from flask import Flask


def init_app(app: Flask):
    from app.views.patient_view import bp_patient
    app.register_blueprint(bp_patient)
