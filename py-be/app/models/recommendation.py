#Import Libraries
import json
import ast
import bcrypt
from datetime import datetime, timezone
import uuid

#import dependencies
from app import db

# ALWAYS RECHECK IF THE DATASTRUCTURE IS RIGHT
class Recommendation(db.Model):
    recommendation_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    recommendation_titles = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(36), nullable=True)
    recommendation_date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        try:
            recommendation_titles = json.loads(self.recommendation_titles)
        except (ValueError, SyntaxError, json.JSONDecodeError):
            recommendation_titles = []

        return {
            'recommendation_id' : self.recommendation_id,
            'recommendation_titles' : recommendation_titles,
            'user_id' : self.user_id,
            'recommendation_date_added' : self.recommendation_date_added
        }