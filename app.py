from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import json
from flask_sqlalchemy import SQLAlchemy
import os
from cook import main as run_cook_logic  # Import the main function from cook.py

app = Flask(__name__)
app.secret_key = 'uw_dsc_speed_dating' 

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.txt')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    discord_handle = db.Column(db.String(80), nullable=False)
    mbti = db.Column(db.String(4), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    preferred_gender = db.Column(db.String(10), nullable=False)
    communication_style = db.Column(db.String(20), nullable=False)
    weekend_activity = db.Column(db.String(20), nullable=False)
    preference = db.Column(db.String(10), nullable=False)
    movie_genres = db.Column(db.String(100), nullable=False)
    party_frequency = db.Column(db.String(10), nullable=False)
    relationship_components = db.Column(db.String(100), nullable=False)
    fate_belief = db.Column(db.String(20), nullable=False)

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    score = db.Column(db.Float, nullable=False)
    round_type = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        user = User(
            name=request.form.get('name'),
            discord_handle=request.form.get('discord'),
            mbti=request.form.get('mbti'),
            gender=request.form.get('gender'),
            preferred_gender=request.form.get('preferred_gender'),
            communication_style=request.form.get('communication_style'),
            weekend_activity=request.form.get('weekend_activity'),
            preference=request.form.get('preference'),
            movie_genres=','.join(request.form.getlist('movie_genres')),
            party_frequency=request.form.get('party_frequency'),
            relationship_components=','.join(request.form.getlist('relationship_components')),
            fate_belief=request.form.get('fate_belief')
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('waiting'))
    return render_template('join.html')

@app.route('/friendship-quiz', methods=['GET', 'POST'])
def friendship_quiz():
    if request.method == 'POST':
        name = session.get('name')
        discord = session.get('discord')
        
        user_data = {
            'name': name,
            'discord_handle': discord,
            'mbti': request.form.get('mbti'),
            'gender': request.form.get('gender'),
            'preferred_gender': request.form.getlist('preferred-gender'),
            'other_gender': request.form.get('other-gender-input'),
            'communication_style': request.form.get('communication-style'),
            'weekend_activity': request.form.get('weekend-activity'),
            'preference': request.form.get('preference'),
            'movie_genres': request.form.getlist('movie-genres'),
            'party_frequency': request.form.get('party-frequency'),
            'relationship_components': request.form.getlist('relationship-components'),
            'fate_belief': request.form.get('fate')
        }

        print("User Data:", user_data)  # Debugging line

        # Append user data to data.txt
        try:
            with open(DATA_FILE, 'a') as f:
                f.write(json.dumps(user_data) + '\n')
                print("Data written to file")  # Debugging line
        except Exception as e:
            print("Error writing to file:", e)  # Debugging line

        return redirect(url_for('waiting'))
    return render_template('friendship-quiz.html')

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

def pre_result():
    # Check if matches exist in the database
    matches_exist = MatchResult.query.first() is not None
    return render_template('pre_result.html', matches_exist=matches_exist)

@app.route('/check_result')
def check_result():
    result_file = 'result.txt'
    
    # Check if the file exists and has content
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        return jsonify(hasResult=True)
    else:
        return jsonify(hasResult=False)

@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/result')
def result():
    # Get name from query parameter
    name = request.args.get('name')
    if not name:
        return redirect(url_for('pre_result'))

    # Check if the user exists
    user = User.query.filter_by(name=name).first()
    if not user:
        return render_template('pre_result.html', error="Name not found. Please re-enter your name.", matches_exist=True)

    # Get the match result for the user
    match_result = MatchResult.query.filter_by(user1_id=user.id).first()
    if not match_result:
        return render_template('result.html', match_name=False, names=get_all_names())

    # Get the matched user's details
    matched_user = User.query.get(match_result.user2_id) if match_result.user2_id else None

    return render_template('result.html',
                           match_name=matched_user.name if matched_user else None,
                           match_discord=matched_user.discord_handle if matched_user else None,
                           round_2_message="We're sorry that some of your preferences might not be satisfied due to gender ratio" if match_result.round_type == "Round 2" else None,
                           names=get_all_names())

def get_all_names():
    # Get all user names for the floating animation
    return [user.name for user in User.query.all()]

@app.route('/run-cook')
def run_cook():
    run_cook_logic()  # Call the main function from cook.py
    return "cook.py logic executed!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
