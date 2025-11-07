from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, unique=True)
    count = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)
    tier = db.Column(db.String(32), default="free")  # e.g., 'free', 'pro', 'admin'

    def __repr__(self):
        return f"<Usage user_id={self.user_id} count={self.count} tier={self.tier}>"
