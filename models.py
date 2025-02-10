from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    discord_handle = db.Column(db.String(100), nullable=False)
    mbti = db.Column(db.String(4), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    preferred_gender = db.Column(db.String(50), nullable=False)
    communication_style = db.Column(db.String(20), nullable=False)
    weekend_activity = db.Column(db.String(20), nullable=False)
    preference = db.Column(db.String(20), nullable=False)
    movie_genres = db.Column(db.String(100), nullable=False)
    party_frequency = db.Column(db.String(20), nullable=False)
    relationship_components = db.Column(db.String(100), nullable=False)
    fate_belief = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    score = db.Column(db.Float, nullable=False)
    round_type = db.Column(db.String(20), nullable=False) 