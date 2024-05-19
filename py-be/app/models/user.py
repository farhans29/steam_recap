#Import Libraries
import bcrypt
from datetime import datetime, timezone
import uuid

#import dependencies
from app import db

class User(db.Model) :
    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_name = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password_hash = db.Column(db.String(128), nullable=False)
    genre_id = db.Column(db.String(36), nullable=True)
    user_date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def set_password(self, password_input) :
        self.user_password_hash = bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password_input) :
        return bcrypt.checkpw(password_input.encode('utf-8'), self.user_password_hash.encode('utf-8'))

    def to_dict(self) :
        return {
            'user_id' : self.user_id,
            'user_name' : self.user_name,
            'user_email' : self.user_email,
            'user_date_added': self.user_date_added.isoformat()
        }