from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from . import db


class PatientModel(db.Model):
    __tablename__ = 'patients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    age = Column(Integer(), nullable=False)
    weight = Column(Float(), nullable=False)
    height = Column(Float(), nullable=False)
    password_hash = Column(String())

    @property
    def password(self):
        return 'Password can not be accessed'

    @password.setter
    def password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    def check_password(self, password_to_comparate):
        return check_password_hash(self.password_hash, password_to_comparate)
