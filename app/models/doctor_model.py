from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from uuid import uuid4

from . import db


class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    password_hash = Column(String())
    speciality_id = Column(UUID(as_uuid=True), ForeignKey('specialities.id'), nullable=False)

    speciality = relationship('SpecialityModel', backref=backref('doctors_list', lazy='joined'), lazy='joined')

    @property
    def password(self):
        return 'Password can not be accessed'

    @password.setter
    def password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    def check_password(self, password_to_comparate):
        return check_password_hash(self.password_hash, password_to_comparate)
