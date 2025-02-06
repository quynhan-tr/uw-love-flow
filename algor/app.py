from flask import Flask, request, render_template, redirect, url_for
import json
import os
import random
import string

app = Flask(__name__)

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form.get('name')
        discord = request.form.get('discord')
        return redirect(url_for('friendship_quiz', name=name, discord=discord))
    return render_template('join.html')

@app.route('/friendship-quiz', methods=['GET', 'POST'])
def friendship_quiz():
    if request.method == 'POST':
        name = request.args.get('name')
        discord = request.args.get('discord')
        
        user_data = {
            'name': name,
            'discord_handle': discord,
            'mbti': request.form.get('mbti'),
            'preferred_gender': request.form.get('preferred-gender'),
            'other_gender': request.form.get('other-gender-input'),
            'communication_style': request.form.get('communication-style'),
            'weekend_activity': request.form.get('weekend-activity'),
            'preference': request.form.get('preference'),
            'movie_genres': request.form.getlist('movie-genres'),
            'party_frequency': request.form.get('party-frequency'),
            'relationship_components': request.form.getlist('relationship-components'),
            'unicorn_belief': request.form.get('unicorn')
        }

        # Generate a random Discord name
        random_discord_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Save the user data
        filename = os.path.join(DATA_DIR, f"{name}_{discord}.json")
        with open(filename, 'w') as f:
            json.dump(user_data, f, indent=4)

        # Pass the random Discord name to the result route
        return redirect(url_for('result', random_discord=random_discord_name))
    return render_template('friendship-quiz.html')

@app.route('/result')
def result():
    random_discord = request.args.get('random_discord')
    return render_template('result.html', random_discord=random_discord)

if __name__ == '__main__':
    app.run(debug=True) 