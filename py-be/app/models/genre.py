# Import Lib
import json
import ast
from datetime import datetime, timezone
import uuid

#Import dependencies
from app import db

# ALWAYS RECHECK IF THE DATASTRUCTURE IS RIGHT
class Genre(db.Model) :
    genre_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    genre_titles = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(36), nullable=True)
    genre_date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def to_dict(self) :
        try:
            genre_titles = json.loads(self.genre_titles)
        except (ValueError, SyntaxError, json.JSONDecodeError):
            genre_titles = []

        return {
            'genre_id': self.genre_id,
            'genre_titles': genre_titles,
            'user_id': self.user_id,
            'genre_date_added' : self.genre_date_added.isoformat()
        }
    
    